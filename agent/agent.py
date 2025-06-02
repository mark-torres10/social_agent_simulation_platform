from typing import Optional

from agent.components.persistent.profile import AgentProfile


class Agent:
    def __init__(self, profile: AgentProfile, agent_id: Optional[str] = None):
        self.profile = profile
        self.agent_id = agent_id

    def __str__(self):
        return f"Agent(id={self.agent_id})\n{str(self.profile)}"

    def __repr__(self):
        return self.__str__()

    def update_beliefs(self, updated_beliefs: str):
        print(f"Updating beliefs for agent {self.agent_id}")
        self.profile.update_profile({"beliefs": updated_beliefs})
        print(f"Updated beliefs: {updated_beliefs}")
