from typing import List, Dict, Optional, Iterator
from agent.initialize_agents import Agent, initialize_agents


class AgentManager:
    def __init__(self, agents: Optional[List[Agent]] = None):
        self._agents = agents or []

    @classmethod
    def from_initialization(
        cls,
        num_agents: int = 1,
        traits_list: Optional[List[Dict[str, str]]] = None,
        agent_ids: Optional[List[str]] = None,
    ) -> "AgentManager":
        agents = initialize_agents(
            num_agents=num_agents, traits_list=traits_list, agent_ids=agent_ids
        )
        return cls(agents)

    def get_agent(self, index: int) -> Agent:
        return self._agents[index]

    def get_agents(self) -> List[Agent]:
        return self._agents

    def update_agent_profile(
        self, index: int, trait_to_description: Dict[str, str]
    ) -> None:
        self._agents[index].profile.update_profile(trait_to_description)

    def __iter__(self) -> Iterator[Agent]:
        return iter(self._agents)

    def __len__(self) -> int:
        return len(self._agents)

    def __getitem__(self, index: int) -> Agent:
        return self._agents[index]
