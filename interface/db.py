# interface/db.py

import json
import os
from threading import Lock

BASE_DIR = os.path.dirname(__file__)
DB_PATH  = os.path.join(BASE_DIR, "data", "campaigns.json")
_lock    = Lock()

def read_campaigns():
    with _lock:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

def write_campaigns(campaigns):
    with _lock:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(campaigns, f, indent=2,default=str)