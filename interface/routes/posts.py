# interface/routes/campaigns.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from db import read_campaigns, write_campaigns

router = APIRouter(tags=["campaigns"])

class CampaignPost(BaseModel):
    id: int = Field(..., description="Unique campaign ID")
    brand_name: str
    caption: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

@router.post("/campaigns/", response_model=CampaignPost)
def create_campaign(post: CampaignPost):
    campaigns = read_campaigns()
    # ensure unique ID
    if any(c["id"] == post.id for c in campaigns):
        raise HTTPException(400, "Campaign ID already exists")
    campaigns.append(post.dict())
    write_campaigns(campaigns)
    return post

@router.get("/campaigns/", response_model=List[CampaignPost])
def list_campaigns():
    return read_campaigns()