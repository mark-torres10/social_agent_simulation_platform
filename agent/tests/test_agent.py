import pytest
from agent.agent import Agent

class DummyProfile:
    def __init__(self):
        self.beliefs = DummyBeliefs()
        self.update_profile_called = False
    def update_profile(self, trait_to_description):
        self.update_profile_called = True
        self.last_update = trait_to_description
    def __str__(self):
        return "DummyProfile"

class DummyBeliefs:
    def get_description(self):
        return "dummy beliefs"

def test_agent_init():
    profile = DummyProfile()
    agent = Agent(profile, agent_id="A1")
    assert agent.profile == profile
    assert agent.agent_id == "A1"

def test_agent_str_repr():
    profile = DummyProfile()
    agent = Agent(profile, agent_id="A2")
    s = str(agent)
    r = repr(agent)
    assert "Agent(id=A2)" in s
    assert "Agent(id=A2)" in r

def test_update_beliefs():
    profile = DummyProfile()
    agent = Agent(profile, agent_id="A3")
    agent.update_beliefs("new beliefs")
    assert profile.update_profile_called
    assert profile.last_update == {"beliefs": "new beliefs"}
