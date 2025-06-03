from typing import Optional, Dict, List

from agent.components.persistent.defaults import select_default_trait


class AgentEngagementPreferences:
    def __init__(
        self,
        description: Optional[str] = None,
        trait_type: str = "engagement_preferences",
        preferences_by_engagement_type: Optional[Dict[str, float]] = None,
        topics_more_likely_to_engage_with: Optional[List[str]] = None,
        accounts_more_likely_to_engage_with: Optional[List[str]] = None,
        other_engagement_preferences: Optional[List[str]] = None,
    ):
        if not description:
            description = select_default_trait(trait_type)
        self.description = description
        self.trait_type = trait_type

        # Initialize engagement preferences with defaults if not provided
        self.preferences_by_engagement_type = preferences_by_engagement_type or {
            "post": 0.5,
            "comment": 0.5,
            "like": 0.5,
        }
        self.topics_more_likely_to_engage_with = topics_more_likely_to_engage_with or []
        self.accounts_more_likely_to_engage_with = (
            accounts_more_likely_to_engage_with or []
        )
        self.other_engagement_preferences = other_engagement_preferences or []

    def update(
        self,
        description: Optional[str] = None,
        preferences_by_engagement_type: Optional[Dict[str, float]] = None,
        topics_more_likely_to_engage_with: Optional[List[str]] = None,
        accounts_more_likely_to_engage_with: Optional[List[str]] = None,
        other_engagement_preferences: Optional[List[str]] = None,
    ):
        """Update engagement preferences with new values."""
        if not description:
            description = select_default_trait(self.trait_type)
        self.description = description

        if preferences_by_engagement_type:
            self.preferences_by_engagement_type.update(preferences_by_engagement_type)
        if topics_more_likely_to_engage_with:
            self.topics_more_likely_to_engage_with = topics_more_likely_to_engage_with
        if accounts_more_likely_to_engage_with:
            self.accounts_more_likely_to_engage_with = (
                accounts_more_likely_to_engage_with
            )
        if other_engagement_preferences:
            self.other_engagement_preferences = other_engagement_preferences

    def get_description(self) -> str:
        return self.description

    def get_trait_type(self) -> str:
        return self.trait_type

    def get_engagement_preferences(self) -> Dict:
        """Get all engagement preferences as a dictionary."""
        return {
            "preferences_by_engagement_type": self.preferences_by_engagement_type,
            "topics_more_likely_to_engage_with": self.topics_more_likely_to_engage_with,
            "accounts_more_likely_to_engage_with": self.accounts_more_likely_to_engage_with,
            "other_engagement_preferences": self.other_engagement_preferences,
        }
