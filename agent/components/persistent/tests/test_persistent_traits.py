import pytest
from unittest.mock import patch

from agent.components.persistent.beliefs import AgentBeliefs
from agent.components.persistent.personality import AgentPersonality
from agent.components.persistent.political_views import AgentPoliticalViews
from agent.components.persistent.worldview import AgentWorldview
from agent.components.persistent.history import AgentHistory
from agent.components.persistent.engagement_preferences import AgentEngagementPreferences

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

# --- AgentHistory ---
def test_agent_history_init_with_description():
    expected_result = "custom history"
    history = AgentHistory(description=expected_result)
    assert history.get_description() == expected_result
    assert history.get_trait_type() == "history"
    assert history.get_history() == []

def test_agent_history_init_with_default():
    expected_result = "mocked default history"
    with patch("agent.components.persistent.history.select_default_trait", return_value=expected_result):
        history = AgentHistory()
        assert history.get_description() == expected_result
        assert history.get_trait_type() == "history"
        assert history.get_history() == []

def test_agent_history_update_with_description():
    history = AgentHistory(description="old")
    expected_result = "new history"
    history.update(expected_result)
    assert history.get_description() == expected_result

def test_agent_history_update_with_default():
    history = AgentHistory(description="old")
    expected_result = "mocked default history update"
    with patch("agent.components.persistent.history.select_default_trait", return_value=expected_result):
        history.update()
        assert history.get_description() == expected_result

def test_agent_history_add_entry():
    history = AgentHistory()
    entry_type = "test_entry"
    description = "test description"
    metadata = {"key": "value"}
    
    history.add_entry(entry_type, description, metadata)
    entries = history.get_history()
    
    assert len(entries) == 1
    assert entries[0]["type"] == entry_type
    assert entries[0]["description"] == description
    assert entries[0]["metadata"] == metadata
    assert "timestamp" in entries[0]

def test_agent_history_get_recent_history():
    history = AgentHistory()
    for i in range(15):
        history.add_entry("test", f"entry {i}")
    
    recent = history.get_recent_history(5)
    assert len(recent) == 5
    assert recent[-1]["description"] == "entry 14"

def test_agent_history_get_history_by_type():
    history = AgentHistory()
    history.add_entry("type1", "entry1")
    history.add_entry("type2", "entry2")
    history.add_entry("type1", "entry3")
    
    type1_entries = history.get_history_by_type("type1")
    assert len(type1_entries) == 2
    assert type1_entries[0]["description"] == "entry1"
    assert type1_entries[1]["description"] == "entry3"

# --- AgentEngagementPreferences ---
def test_agent_engagement_preferences_init_with_description():
    expected_result = "custom engagement preferences"
    ep = AgentEngagementPreferences(description=expected_result)
    assert ep.get_description() == expected_result
    assert ep.get_trait_type() == "engagement_preferences"
    assert ep.preferences_by_engagement_type == {"post": 0.5, "comment": 0.5, "like": 0.5}
    assert ep.topics_more_likely_to_engage_with == []
    assert ep.accounts_more_likely_to_engage_with == []
    assert ep.other_engagement_preferences == []

def test_agent_engagement_preferences_init_with_default():
    expected_result = "mocked default engagement preferences"
    with patch("agent.components.persistent.engagement_preferences.select_default_trait", return_value=expected_result):
        ep = AgentEngagementPreferences()
        assert ep.get_description() == expected_result
        assert ep.get_trait_type() == "engagement_preferences"

def test_agent_engagement_preferences_update_with_description():
    ep = AgentEngagementPreferences(description="old")
    expected_result = "new engagement preferences"
    ep.update(description=expected_result)
    assert ep.get_description() == expected_result

def test_agent_engagement_preferences_update_with_default():
    ep = AgentEngagementPreferences(description="old")
    expected_result = "mocked default engagement preferences update"
    with patch("agent.components.persistent.engagement_preferences.select_default_trait", return_value=expected_result):
        ep.update()
        assert ep.get_description() == expected_result
