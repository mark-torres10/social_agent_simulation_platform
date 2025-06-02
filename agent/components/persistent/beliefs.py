from typing import Optional

from agent.components.persistent.defaults import select_default_trait


class AgentBeliefs:
    def __init__(
        self,
        description: Optional[str] = None,
        trait_type: str = "beliefs",
    ):
        if not description:
            description = select_default_trait(trait_type)
        self.description = description
        self.trait_type = trait_type

    def update(self, description: Optional[str] = None):
        if not description:
            description = select_default_trait(self.trait_type)
        self.description = description

    def get_description(self) -> str:
        return self.description

    def get_trait_type(self) -> str:
        return self.trait_type
