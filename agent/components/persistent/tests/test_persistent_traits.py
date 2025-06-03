import pytest
from unittest.mock import patch

from agent.components.persistent.beliefs import AgentBeliefs
from agent.components.persistent.personality import AgentPersonality
from agent.components.persistent.political_views import AgentPoliticalViews
from agent.components.persistent.worldview import AgentWorldview

# --- AgentBeliefs ---
def test_agent_beliefs_init_with_description():
    expected_result = "custom beliefs"
    beliefs = AgentBeliefs(description=expected_result)
    assert beliefs.get_description() == expected_result
    assert beliefs.get_trait_type() == "beliefs"

def test_agent_beliefs_init_with_default():
    expected_result = "mocked default beliefs"
    with patch("agent.components.persistent.beliefs.select_default_trait", return_value=expected_result):
        beliefs = AgentBeliefs()
        assert beliefs.get_description() == expected_result
        assert beliefs.get_trait_type() == "beliefs"

def test_agent_beliefs_update_with_description():
    beliefs = AgentBeliefs(description="old")
    expected_result = "new beliefs"
    beliefs.update(expected_result)
    assert beliefs.get_description() == expected_result

def test_agent_beliefs_update_with_default():
    beliefs = AgentBeliefs(description="old")
    expected_result = "mocked default beliefs update"
    with patch("agent.components.persistent.beliefs.select_default_trait", return_value=expected_result):
        beliefs.update()
        assert beliefs.get_description() == expected_result

# --- AgentPersonality ---
def test_agent_personality_init_with_description():
    expected_result = "custom personality"
    personality = AgentPersonality(description=expected_result)
    assert personality.get_description() == expected_result
    assert personality.get_trait_type() == "personality"

def test_agent_personality_init_with_default():
    expected_result = "mocked default personality"
    with patch("agent.components.persistent.personality.select_default_trait", return_value=expected_result):
        personality = AgentPersonality()
        assert personality.get_description() == expected_result
        assert personality.get_trait_type() == "personality"

def test_agent_personality_update_with_description():
    personality = AgentPersonality(description="old")
    expected_result = "new personality"
    personality.update(expected_result)
    assert personality.get_description() == expected_result

def test_agent_personality_update_with_default():
    personality = AgentPersonality(description="old")
    expected_result = "mocked default personality update"
    with patch("agent.components.persistent.personality.select_default_trait", return_value=expected_result):
        personality.update()
        assert personality.get_description() == expected_result

# --- AgentPoliticalViews ---
def test_agent_political_views_init_with_description():
    expected_result = "custom political views"
    pv = AgentPoliticalViews(description=expected_result)
    assert pv.get_description() == expected_result
    assert pv.get_trait_type() == "political_views"

def test_agent_political_views_init_with_default():
    expected_result = "mocked default political views"
    with patch("agent.components.persistent.political_views.select_default_trait", return_value=expected_result):
        pv = AgentPoliticalViews()
        assert pv.get_description() == expected_result
        assert pv.get_trait_type() == "political_views"

def test_agent_political_views_update_with_description():
    pv = AgentPoliticalViews(description="old")
    expected_result = "new political views"
    pv.update(expected_result)
    assert pv.get_description() == expected_result

def test_agent_political_views_update_with_default():
    pv = AgentPoliticalViews(description="old")
    expected_result = "mocked default political views update"
    with patch("agent.components.persistent.political_views.select_default_trait", return_value=expected_result):
        pv.update()
        assert pv.get_description() == expected_result

# --- AgentWorldview ---
def test_agent_worldview_init_with_description():
    expected_result = "custom worldview"
    wv = AgentWorldview(description=expected_result)
    assert wv.get_description() == expected_result
    assert wv.get_trait_type() == "worldviews"

def test_agent_worldview_init_with_default():
    expected_result = "mocked default worldview"
    with patch("agent.components.persistent.worldview.select_default_trait", return_value=expected_result):
        wv = AgentWorldview()
        assert wv.get_description() == expected_result
        assert wv.get_trait_type() == "worldviews"

def test_agent_worldview_update_with_description():
    wv = AgentWorldview(description="old")
    expected_result = "new worldview"
    wv.update(expected_result)
    assert wv.get_description() == expected_result

def test_agent_worldview_update_with_default():
    wv = AgentWorldview(description="old")
    expected_result = "mocked default worldview update"
    with patch("agent.components.persistent.worldview.select_default_trait", return_value=expected_result):
        wv.update()
        assert wv.get_description() == expected_result
