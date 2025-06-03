from agent.components.persistent.engagement_preferences import (
    AgentEngagementPreferences,
)
from agent.components.persistent.history import AgentHistory
from agent.components.persistent.personality import AgentPersonality
from agent.components.persistent.beliefs import AgentBeliefs
from agent.components.persistent.political_views import AgentPoliticalViews
from agent.components.persistent.worldview import AgentWorldview


class AgentProfile:
    def __init__(self, trait_to_description: dict = None):
        trait_to_description = trait_to_description or {}
        self.personality = AgentPersonality(
            description=trait_to_description.get("personality")
        )
        self.beliefs = AgentBeliefs(description=trait_to_description.get("beliefs"))
        self.political_views = AgentPoliticalViews(
            description=trait_to_description.get("political_views")
        )
        self.worldviews = AgentWorldview(
            description=trait_to_description.get("worldviews")
        )
        self.engagement_preferences = AgentEngagementPreferences(
            description=trait_to_description.get("engagement_preferences")
        )
        self.history = AgentHistory(description=trait_to_description.get("history"))

    def get_profile(self) -> dict:
        return {
            "personality": self.personality.get_description(),
            "beliefs": self.beliefs.get_description(),
            "political_views": self.political_views.get_description(),
            "worldviews": self.worldviews.get_description(),
            "engagement_preferences": self.engagement_preferences.get_description(),
            "history": self.history.get_description(),
        }

    def update_profile(self, trait_to_description: dict):
        """Update the profile with new descriptions for each trait, where
        relevant traits are updated and others are left unchanged."""
        self.personality.update(trait_to_description.get("personality"))
        self.beliefs.update(trait_to_description.get("beliefs"))
        self.political_views.update(trait_to_description.get("political_views"))
        self.worldviews.update(trait_to_description.get("worldviews"))
        self.engagement_preferences.update(
            trait_to_description.get("engagement_preferences")
        )
        self.history.update(trait_to_description.get("history"))

    def get_profile_description(self) -> str:
        """Get a description of the profile."""
        profile = self.get_profile()
        description = ["The profile has the following characteristics:\n"]
        for trait, value in profile.items():
            trait_label = f"[{trait.replace('_', ' ').upper()}]"
            description.append(f"{trait_label}\n{value}\n")
        return "\n".join(description)

    def __str__(self) -> str:
        return self.get_profile_description()
