# test_run_consumeragent.py
import requests
from agents.consumer_agent import load_consumer_profiles, ConsumerAgent

def test_run_consumeragent():
    # 1) Load all consumer profiles from agents/consumer_profiles/
    profiles = load_consumer_profiles()
    if not profiles:
        print("❌ No consumer profiles found in agents/consumer_profiles/")
        return

    # Pick one consumer (e.g. Alice)
    cid, profile = next(iter(profiles.items()))
    consumer = ConsumerAgent(profile=profile)

    # 2) Fetch live campaigns from your backend
    resp = requests.get("http://localhost:8000/campaigns/")
    if not resp.ok:
        print(f"❌ Failed to fetch campaigns: {resp.status_code}")
        return
    posts = resp.json()
    if not posts:
        print("⚠️ No campaigns available to evaluate.")
        return

    # 3) Let the consumer evaluate each post
    print(f"\n🧠 Running evaluations for consumer '{consumer.name}' ({consumer.id}):\n")
    reactions = consumer.batch_evaluate(posts)

    # 4) Print out the results
    for r in reactions:
        print(f"Post {r['post_id']}: {r['action']}")
        print(f"  Thought: {r['thought']}\n")

    print("✅ XML files should now be in agents/consumer_responses/{consumer.id}/")

if __name__ == "__main__":
    test_run_consumeragent()