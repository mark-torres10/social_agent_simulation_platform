import pytest
from agent.agent_manager import AgentManager

class DummyAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.profile = DummyProfile()

class DummyProfile:
    def __init__(self):
        self.updated = False
    def update_profile(self, trait_to_description):
        self.updated = True
        self.last_update = trait_to_description

def test_agent_manager_init_and_get():
    agents = [DummyAgent(f"A{i}") for i in range(3)]
    manager = AgentManager(agents=agents)
    assert len(manager) == 3
    assert manager.get_agent(1).agent_id == "A1"
    assert manager[2].agent_id == "A2"

def test_update_agent_profile():
    agents = [DummyAgent(f"A{i}") for i in range(2)]
    manager = AgentManager(agents=agents)
    manager.update_agent_profile(0, {"beliefs": "new"})
    assert agents[0].profile.updated
    assert agents[0].profile.last_update == {"beliefs": "new"} 
