# simulation/run_simulation.py
from agents.brand_agent import BrandAgent
from agents.brand_profiles import load_profile
import time

def run_multibrand(rounds=6, pause=2):
    # load both profiles
    e_profile = load_profile("endurastride.json")
    s_profile = load_profile("sprintstyle.json")

    endura = BrandAgent(profile=e_profile)
    sprint = BrandAgent(profile=s_profile)

    for i in range(rounds):
        print(f"\n--- Round {i+1} ---")
        # EnduraStride posts
        print("🧢 EnduraStride →", endura.generate_campaign())
        # SprintStyle posts
        print("🏃‍♂️ SprintStyle  →", sprint.generate_campaign())

        # every 2 posts, rotate their USPs
        if (i+1) % 2 == 0:
            endura.cycle_usp()
            sprint.cycle_usp()

        time.sleep(pause)

    print("\n📝 Final Summaries:")
    print("EnduraStride:", endura.summary())
    print("SprintStyle: ", sprint.summary())

if __name__ == "__main__":
    run_multibrand()