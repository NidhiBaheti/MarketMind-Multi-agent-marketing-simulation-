# agents/brand_agent.py

import re
import random
import requests
import difflib
import os
from datetime import datetime
from xml.etree import ElementTree as ET
from xml.dom import minidom
from collections import deque
from llm.local_inference import UIUCChatLLM

_WORD_RE = re.compile(r"[A-Za-z']+")

def _tokens(text: str):
    return _WORD_RE.findall(text.lower())

def _trigrams(tokens):
    return [" ".join(tokens[i:i+3]) for i in range(len(tokens) - 2)]

# --- New: Softer, dynamic prompt template ---
_PROMPT_TEMPLATE = """
You are crafting fresh social captions for the sports-footwear brand {brand_name}.

Brand essence snapshot:
Vision: {vision_short}
Mission: {mission_short}
Core values: {core_vals_short}
Current USP focus: {usp}

Avoid echoing these recent openers:
{recent_openers}

Avoid reusing these recent hashtags:
{recent_hashtags}

Creative lens for this round:
- {lens_line}

Produce TWO distinct Instagram captions, marked as:
<<A>> caption text
<<B>> caption text

Soft guidelines (we’ll post-process):
- 140–200 characters ideally
- 1 relevant emoji (not at very start)
- 1 call-to-action (vary verbs over time)
- 2 on-brand hashtags (no spam)
- Do not start with same first 2–3 words as any recent opener
- No quotation marks around the entire caption
Nothing else.
""".strip()

class BrandAgent:
    """
    BrandAgent with dynamic prompts, n-gram & fuzzy dedupe,
    posts campaigns via API, and writes XML.
    """

    def __init__(
        self,
        profile: dict,
        llm: UIUCChatLLM = None,
        similarity_threshold: float = 0.75,
        trigram_overlap_threshold: float = 0.35,
        trigram_memory_size: int = 60
    ):
        self.profile  = profile
        self.name     = profile.get("name", "UnknownBrand")
        self.llm      = llm or UIUCChatLLM()
        self.similarity_threshold      = similarity_threshold
        self.trigram_overlap_threshold = trigram_overlap_threshold
        self.history  = []  # List of {"id","caption","usp","timestamp"}

        # memory for diversity
        self.recent_captions = deque(maxlen=trigram_memory_size)
        self.trigram_memory  = set()

    # ——— Diversity Helpers ———

    def _trigram_overlap(self, caption: str) -> float:
        toks = _tokens(caption)
        tgs  = _trigrams(toks)
        if not tgs:
            return 0.0
        hits = sum(1 for tg in tgs if tg in self.trigram_memory)
        return hits / len(tgs)

    def _too_many_trigram_repeats(self, caption: str) -> bool:
        return self._trigram_overlap(caption) > self.trigram_overlap_threshold

    def _update_trigram_memory(self, caption: str):
        self.recent_captions.append(caption)
        toks = _tokens(caption)
        for tg in _trigrams(toks):
            self.trigram_memory.add(tg)

    def _is_too_similar(self, candidate: str) -> bool:
        for record in self.history:
            prev = record["caption"]
            if difflib.SequenceMatcher(None, candidate, prev).ratio() >= self.similarity_threshold:
                return True
        return False

    # ——— Main Generation ———

    def generate_campaign(self, focus_usp: str = None) -> str:
        usps = self.profile.get("usps", [])
        if not usps:
            raise ValueError("Profile must include at least one USP")
        usp = focus_usp if focus_usp in usps else usps[0]

        # build core context
        vision  = self.profile.get("vision", "")
        mission = self.profile.get("mission", "")
        core_vals = "; ".join(f"{k} — {v}" for k, v in self.profile.get("core_values", {}).items())

        # gather recent openers (first 5 words) & hashtags
        recent_openers = []
        for c in list(self.recent_captions)[-5:]:
            words = c.split()
            if words:
                recent_openers.append(" ".join(words[:5]))
        recent_openers_str = "\n".join(f"- {o}" for o in recent_openers) or "- None"

        hashtags = set()
        for rec in self.history[-8:]:
            tags = re.findall(r"#\w+", rec["caption"])
            hashtags.update(tags)
        recent_hashtags_str = "\n".join(f"- {h}" for h in sorted(hashtags)) or "- None"

        # pick a creative lens from profile
        lenses = self.profile.get("creative_lenses", [])
        lens_line = random.choice(lenses) if lenses else "No lens provided"

        # assemble the dynamic prompt
        prompt = _PROMPT_TEMPLATE.format(
            brand_name=self.name,
            vision_short=vision[:90],
            mission_short=mission[:90],
            core_vals_short=core_vals[:120],
            usp=usp,
            recent_openers=recent_openers_str,
            recent_hashtags=recent_hashtags_str,
            lens_line=lens_line
        )

        # ask the LLM
        try:
            raw = self.llm.generate(prompt, temperature=0.7).strip()
        except Exception as e:
            print(f"[Warning] LLM error, falling back: {e}")
            return self._fallback_caption(usp)

        # parse <<A>> / <<B>> lines
        options = []
        for line in raw.splitlines():
            m = re.match(r"<<[AB]>>\s*(.+)", line)
            if m:
                options.append(m.group(1).strip())
        options = list(dict.fromkeys(options))
        if not options:
            return self._fallback_caption(usp)

        # apply filters
        ngram_filtered = [o for o in options if not self._too_many_trigram_repeats(o)]
        fuzzy_filtered = [o for o in ngram_filtered if not self._is_too_similar(o)]
        candidates = fuzzy_filtered or ngram_filtered or options

        # choose & record
        caption     = random.choice(candidates)
        campaign_id = int(datetime.utcnow().timestamp() * 1000)
        timestamp   = datetime.utcnow().isoformat()
        record = {"id": campaign_id, "caption": caption, "usp": usp, "timestamp": timestamp}
        self.history.append(record)
        self._update_trigram_memory(caption)

        # persist & post
        self._post_to_api(record)
        self._write_campaign_xml(record)
        return caption

    # ——— Fallback & Persistence ———

    def _fallback_caption(self, usp: str) -> str:
        tag = "#" + self.name.replace(" ", "")
        caption = f"{self.name} {usp}! 🔥 Step up your game. {tag}"
        cid = int(datetime.utcnow().timestamp() * 1000)
        ts  = datetime.utcnow().isoformat()
        record = {"id": cid, "caption": caption, "usp": usp, "timestamp": ts}
        self.history.append(record)
        self._update_trigram_memory(caption)
        self._post_to_api(record)
        self._write_campaign_xml(record)
        return caption

    def _post_to_api(self, record: dict):
        payload = {"brand_name": self.name, **record}
        try:
            resp = requests.post("http://localhost:8000/campaigns/", json=payload, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"[Warning] Failed to post campaign: {e}")

    def _write_campaign_xml(self, record: dict):
        base_dir = os.path.join(os.path.dirname(__file__), "brand_responses", self.name)
        os.makedirs(base_dir, exist_ok=True)
        root = ET.Element("campaign")
        for k, v in record.items():
            ET.SubElement(root, k).text = str(v)
        ET.SubElement(root, "brand_name").text = self.name
        xml_bytes = ET.tostring(root, encoding="utf-8")
        pretty   = minidom.parseString(xml_bytes).toprettyxml(indent="  ")
        path     = os.path.join(base_dir, f"{record['id']}.xml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(pretty)

    # ——— Utility ———

    def cycle_usp(self):
        usps = self.profile.get("usps", [])
        if usps:
            usps.append(usps.pop(0))
            print(f"[{self.name}] USP rotated to: {usps[0]}")

    def summary(self) -> dict:
        last = self.history[-1]["usp"] if self.history else None
        return {
            "brand_name":    self.name,
            "campaigns_run": len(self.history),
            "last_usp":      last
        }