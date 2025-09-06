# interface/main.py

import os
import xml.etree.ElementTree as ET
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/campaigns")
@app.get("/campaigns/")
def get_campaigns():
    # 1) Load campaigns from brand_responses
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../agents/brand_responses"))
    campaigns = []
    if os.path.isdir(base):
        for brand in os.listdir(base):
            brand_dir = os.path.join(base, brand)
            if not os.path.isdir(brand_dir):
                continue
            for fname in os.listdir(brand_dir):
                if not fname.endswith(".xml"):
                    continue
                path = os.path.join(brand_dir, fname)
                try:
                    root = ET.parse(path).getroot()
                    data = {c.tag: c.text for c in root}
                    data["brand_name"] = brand
                    data["id"] = int(data.get("id", 0))
                    data["usp"] = data.get("usp", "")
                    data["caption"] = data.get("caption", "")
                    data["timestamp"] = data.get("timestamp", "")
                    campaigns.append(data)
                except ET.ParseError:
                    continue

    # 2) Load reactions from consumer_responses
    reactions_map = defaultdict(list)
    resp_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../agents/consumer_responses"))
    if os.path.isdir(resp_base):
        for consumer_id in os.listdir(resp_base):
            cdir = os.path.join(resp_base, consumer_id)
            if not os.path.isdir(cdir):
                continue
            for fname in os.listdir(cdir):
                if not fname.endswith(".xml"):
                    continue
                path = os.path.join(cdir, fname)
                try:
                    root = ET.parse(path).getroot()
                    rid = int(root.findtext("post_id", default="0"))
                    action = root.findtext("action", default="IGNORE")
                    thought = root.findtext("thought", default="")
                    reactions_map[rid].append({
                        "consumer_id": consumer_id,
                        "action": action,
                        "thought": thought
                    })
                except ET.ParseError:
                    continue

    # 3) Attach stats & reactions, sort newest first
    for camp in campaigns:
        rid = camp["id"]
        reacts = reactions_map.get(rid, [])
        likes  = sum(1 for r in reacts if r["action"]=="LIKE")
        shares = sum(1 for r in reacts if r["action"]=="SHARE")
        camp["stats"]     = {"likes": likes, "shares": shares}
        camp["reactions"] = reacts

    campaigns.sort(key=lambda c: c["id"], reverse=True)
    return campaigns