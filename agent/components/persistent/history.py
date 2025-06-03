from typing import Optional, List, Dict
from datetime import datetime

from agent.components.persistent.defaults import select_default_trait


class AgentHistory:
    def __init__(
        self,
        description: Optional[str] = None,
        trait_type: str = "history",
    ):
        if not description:
            description = select_default_trait(trait_type)
        self.description = description
        self.trait_type = trait_type
        self.history_entries: List[Dict] = []

    def add_entry(
        self, entry_type: str, description: str, metadata: Optional[Dict] = None
    ):
        """Add a new entry to the agent's history.

        Args:
            entry_type: Type of entry (e.g., 'belief_change', 'action', 'interaction')
            description: Description of what happened
            metadata: Optional additional metadata about the entry
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": entry_type,
            "description": description,
            "metadata": metadata or {},
        }
        self.history_entries.append(entry)

    def get_history(self) -> List[Dict]:
        """Get the full history of entries."""
        return self.history_entries

    def get_recent_history(self, n_entries: int = 10) -> List[Dict]:
        """Get the n most recent history entries."""
        return self.history_entries[-n_entries:]

    def get_history_by_type(self, entry_type: str) -> List[Dict]:
        """Get all history entries of a specific type."""
        return [entry for entry in self.history_entries if entry["type"] == entry_type]

    def update(self, description: Optional[str] = None):
        """Update the base description of the history component."""
        if not description:
            description = select_default_trait(self.trait_type)
        self.description = description

    def get_description(self) -> str:
        return self.description

    def get_trait_type(self) -> str:
        return self.trait_type
