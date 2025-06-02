from typing import Optional
from agent.components.persistent.profile import AgentProfile

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


class Agent:
    def __init__(self, profile: AgentProfile, agent_id: Optional[str] = None):
        self.profile = profile
        self.agent_id = agent_id

    def __str__(self):
        return f"Agent(id={self.agent_id})\n{str(self.profile)}"

    def __repr__(self):
        return self.__str__()
