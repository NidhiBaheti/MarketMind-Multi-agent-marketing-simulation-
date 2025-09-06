# simulation/run_simulation.py

import os, time, requests
from typing import Dict, Set, List

from agents.brand_agent import BrandAgent
from agents.consumer_agent import ConsumerAgent, load_consumer_profiles
from agents.brand_profiles import load_profile

BACKEND = "http://localhost:8000"

def load_brand_agents(folder: str = "agents/brand_profiles") -> Dict[str, BrandAgent]:
    agents = {}
    if not os.path.isdir(folder):
        print(f"[ERROR] Brand profiles folder missing: {folder}")
        return agents
    for fname in os.listdir(folder):
        if fname.endswith(".json"):
            try:
                profile = load_profile(fname)
                name = profile.get("name")
                if name:
                    agents[name] = BrandAgent(profile=profile)
            except Exception as e:
                print(f"[WARN] Skipping {fname}: {e}")
    return agents

def fetch_campaigns() -> List[dict]:
    try:
        r = requests.get(f"{BACKEND}/campaigns/", timeout=8)
        if r.ok:
            return r.json()
        print(f"[WARN] GET /campaigns status={r.status_code}")
    except Exception as e:
        print(f"[WARN] fetch_campaigns: {e}")
    return []

def run(rounds: int = 3, pause: float = 0.7):
    print(">>> Simulation starting")
    brands = load_brand_agents()
    consumers_profiles = load_consumer_profiles()
    consumers = {cid: ConsumerAgent(p) for cid, p in consumers_profiles.items()}

    if not brands:
        print("❌ No brands loaded – aborting.")
        return
    if not consumers:
        print("❌ No consumers loaded – aborting.")
        return

    print(f"✅ Loaded {len(brands)} brand(s) and {len(consumers)} consumer(s).")

    seen: Dict[str, Set[int]] = {cid: set() for cid in consumers}

    for r_i in range(1, rounds + 1):
        print(f"\n=== ROUND {r_i} ===")
        new_ids: Set[int] = set()

        # Brand phase
        for bname, bagent in brands.items():
            print(f"[Brand] {bname}: generating campaign...")
            caption = bagent.generate_campaign()
            cid = bagent.history[-1]["id"]
            new_ids.add(cid)
            print(f"  → Posted id={cid}: {caption[:90]}{'…' if len(caption)>90 else ''}")

        time.sleep(pause)

        # Consumer phase
        campaign_list = fetch_campaigns()
        new_campaigns = [c for c in campaign_list if c.get("id") in new_ids]

        for cid, cagent in consumers.items():
            print(f"[Consumer] {cagent.name} reacting to {len(new_campaigns)} new post(s)")
            for camp in new_campaigns:
                pid = camp["id"]
                if pid in seen[cid]:
                    continue
                reaction = cagent.evaluate_post(camp)
                seen[cid].add(pid)
                print(f"   - Post {pid} => {reaction['action']}")

        # Rotate USPs
        for bname, bagent in brands.items():
            bagent.cycle_usp()

        time.sleep(pause)

    print("\n=== DONE ===")
    for bname, bagent in brands.items():
        s = bagent.summary()
        print(f"[Summary] {bname}: {s['campaigns_run']} campaigns; last USP = {s['last_usp']}")

if __name__ == "__main__":
    run(rounds=5)