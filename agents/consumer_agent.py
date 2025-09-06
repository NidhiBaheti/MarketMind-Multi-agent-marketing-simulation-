# agents/consumer_agent.py

import json
import glob
import os
from xml.etree import ElementTree as ET
from xml.dom import minidom
from llm.local_inference import UIUCChatLLM

def load_consumer_profiles() -> dict:
    """
    Discover and load all consumer profile JSON files from agents/consumer_profiles.
    Returns a map of consumer_id -> profile dict.
    """
    profiles = {}
    base = os.path.join(os.path.dirname(__file__), "consumer_profiles")
    for filepath in glob.glob(os.path.join(base, "*.json")):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cid = data.get("id")
            if not cid:
                raise ValueError(f"Consumer profile {filepath} missing 'id' field")
            profiles[cid] = data
    return profiles


class ConsumerAgent:
    """
    ConsumerAgent represents an individual consumer with a dynamic personality profile.
    It uses an LLM to generate an internal thought process and an action
    (LIKE, SHARE, or IGNORE) for each campaign post it evaluates, and
    writes each reaction out as an XML file.
    """

    def __init__(self, profile: dict, llm: UIUCChatLLM = None):
        self.id           = profile["id"]
        self.name         = profile.get("name", "UnknownConsumer")
        self.demographics = profile.get("demographics", {})
        self.daily_needs  = profile.get("daily_needs", [])
        self.traits       = profile.get("personality_traits", {})
        self.threshold    = profile.get("decision_threshold", 0.5)
        self.llm          = llm or UIUCChatLLM()
        self.history      = []  # List of dicts: {post_id, thought, action}

    def evaluate_post(self, post: dict) -> dict:
        """
        Evaluate a single campaign post via the LLM.
        Builds a dynamic prompt from the consumer's profile and the post.
        Returns a dict with keys: post_id, thought, action.
        Also writes an XML file under agents/consumer_responses/{consumer_id}/{post_id}.xml
        """
        # Build dynamic prompt
        demo = self.demographics
        needs = "; ".join(self.daily_needs)
        traits = ", ".join(f"{k}={v}" for k, v in self.traits.items())

        prompt = f"""
You are {self.name}, a consumer with this background:
- Age: {demo.get('age')} | Gender: {demo.get('gender', 'N/A')} | Education: {demo.get('education_level', 'N/A')} 
  Occupation: {demo.get('occupation', 'N/A')} | Income: {demo.get('income_range', 'N/A')} | Location: {demo.get('location', 'N/A')}
- Daily needs: {needs}
- Personality traits: {traits}

Here is a brand campaign post:
- Caption: "{post.get('caption')}"
- USP: {post.get('usp')}

Think step-by-step about this post considering your background and needs.
Then decide whether to LIKE, SHARE, or IGNORE it.

Respond in JSON exactly as:
{{"thought": "<one-sentence reasoning>", "action": "LIKE"|"SHARE"|"IGNORE"}}
""".strip()

        # Call LLM
        raw = self.llm.generate(prompt).strip()

        # Parse JSON (fallback to IGNORE)
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            result = {
                "thought": "Could not parse response; defaulting to IGNORE.",
                "action": "IGNORE"
            }

        # Extract & sanitize
        action = result.get("action", "IGNORE").upper()
        if action not in ("LIKE", "SHARE", "IGNORE"):
            action = "IGNORE"
        thought = result.get("thought", "No thought provided.")

        # Build record
        record = {
            "post_id": post.get("id"),
            "thought": thought,
            "action": action
        }

        # Save to history
        self.history.append(record)

        # Write XML side-effect
        self._write_response_xml(record)

        return record

    def batch_evaluate(self, posts: list) -> list:
        """
        Evaluate a list of posts in sequence and return a list of reaction dicts.
        """
        reactions = []
        for post in posts:
            reactions.append(self.evaluate_post(post))
        return reactions

    def _write_response_xml(self, record: dict):
        """
        Given a record {'post_id', 'thought', 'action'}, write it to
        agents/consumer_responses/{consumer_id}/{post_id}.xml
        """
        # Ensure output folder exists
        out_dir = os.path.join(
            os.path.dirname(__file__),
            "consumer_responses",
            self.id
        )
        os.makedirs(out_dir, exist_ok=True)

        # Build XML tree
        root = ET.Element("reaction")
        ET.SubElement(root, "consumer_id").text = self.id
        ET.SubElement(root, "post_id").text     = str(record["post_id"])
        ET.SubElement(root, "thought").text     = record["thought"]
        ET.SubElement(root, "action").text      = record["action"]

        # Pretty-print XML
        xml_bytes = ET.tostring(root, encoding="utf-8")
        pretty = minidom.parseString(xml_bytes).toprettyxml(indent="  ")

        # Write to file named by post_id
        path = os.path.join(out_dir, f"{record['post_id']}.xml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(pretty)