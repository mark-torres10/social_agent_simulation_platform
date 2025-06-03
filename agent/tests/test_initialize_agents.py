import pytest
from unittest.mock import patch
from agent.initialize_agents import initialize_agents, DEFAULT_NUM_AGENTS
from agent.agent import Agent

# --- Helpers ---
MOCKED_DEFAULT = "mocked default trait"

# --- Tests ---
def test_initialize_agents_default():
    with patch("agent.components.persistent.personality.select_default_trait", return_value=MOCKED_DEFAULT), \
         patch("agent.components.persistent.beliefs.select_default_trait", return_value=MOCKED_DEFAULT), \
         patch("agent.components.persistent.political_views.select_default_trait", return_value=MOCKED_DEFAULT), \
         patch("agent.components.persistent.worldview.select_default_trait", return_value=MOCKED_DEFAULT):
        agents = initialize_agents()
    expected_result = DEFAULT_NUM_AGENTS
    assert len(agents) == expected_result
    for i, agent in enumerate(agents):
        assert isinstance(agent, Agent)
        assert agent.agent_id == str(i)
        assert agent.profile.get_profile()["personality"] == MOCKED_DEFAULT
        assert agent.profile.get_profile()["beliefs"] == MOCKED_DEFAULT
        assert agent.profile.get_profile()["political_views"] == MOCKED_DEFAULT
        assert agent.profile.get_profile()["worldviews"] == MOCKED_DEFAULT

def test_initialize_agents_custom_num_agents():
    num_agents = 3
    with patch("agent.components.persistent.defaults.select_default_trait", return_value=MOCKED_DEFAULT):
        agents = initialize_agents(num_agents=num_agents)
    expected_result = num_agents
    assert len(agents) == expected_result
    for i, agent in enumerate(agents):
        assert agent.agent_id == str(i)

def test_initialize_agents_with_traits_list():
    traits_list = [
        {"personality": "p1", "beliefs": "b1", "political_views": "pv1", "worldviews": "w1"},
        {"personality": "p2", "beliefs": "b2", "political_views": "pv2", "worldviews": "w2"},
    ]
    agents = initialize_agents(traits_list=traits_list)
    expected_result = [
        {"personality": "p1", "beliefs": "b1", "political_views": "pv1", "worldviews": "w1"},
        {"personality": "p2", "beliefs": "b2", "political_views": "pv2", "worldviews": "w2"},
    ]
    for agent, expected_profile in zip(agents, expected_result):
        assert agent.profile.get_profile() == expected_profile

def test_initialize_agents_with_agent_ids():
    num_agents = 2
    agent_ids = ["A", "B"]
    with patch("agent.components.persistent.defaults.select_default_trait", return_value=MOCKED_DEFAULT):
        agents = initialize_agents(num_agents=num_agents, agent_ids=agent_ids)
    expected_result = agent_ids
    for agent, expected_id in zip(agents, expected_result):
        assert agent.agent_id == expected_id

def test_initialize_agents_with_traits_list_and_agent_ids():
    traits_list = [
        {"personality": "p1", "beliefs": "b1", "political_views": "pv1", "worldviews": "w1"},
        {"personality": "p2", "beliefs": "b2", "political_views": "pv2", "worldviews": "w2"},
    ]
    agent_ids = ["X", "Y"]
    agents = initialize_agents(traits_list=traits_list, agent_ids=agent_ids)
    expected_result = [
        ("X", {"personality": "p1", "beliefs": "b1", "political_views": "pv1", "worldviews": "w1"}),
        ("Y", {"personality": "p2", "beliefs": "b2", "political_views": "pv2", "worldviews": "w2"}),
    ]
    for agent, (expected_id, expected_profile) in zip(agents, expected_result):
        assert agent.agent_id == expected_id
        assert agent.profile.get_profile() == expected_profile
