from pydantic import BaseModel


class UserAgent(BaseModel):
    user_id: str
    created_timestamp: str
    profile: str
    personality: str
    beleifs: str
    worldview: str
    political_views: str
    engagement_preferences: str
    history: str
