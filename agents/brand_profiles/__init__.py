
import json
import os

def load_profile(filename: str) -> dict:
    """
    Load a brand profile JSON from the agents/profiles directory.

    :param filename: Name of the JSON file (e.g., 'endurastride_profile.json')
    :return: Parsed profile dictionary
    """
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Profile file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)