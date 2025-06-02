from typing import List, Dict, Optional, Iterator
from agent.models import Agent
from agent.initialize_agents import initialize_agents


class AgentManager:
    def __init__(self, agents: Optional[List[Agent]] = None):
        if not agents:
            self.init_agents()
        else:
            self.agents = agents

    def init_agents(
        self,
        num_agents: int = 1,
        traits_list: Optional[List[Dict[str, str]]] = None,
        agent_ids: Optional[List[str]] = None,
    ):
        agents: List[Agent] = initialize_agents(
            num_agents=num_agents, traits_list=traits_list, agent_ids=agent_ids
        )
        self.agents = agents

    def get_agent(self, index: int) -> Agent:
        return self.agents[index]

    def get_agents(self) -> List[Agent]:
        return self.agents

    def update_agent_profile(
        self, index: int, trait_to_description: Dict[str, str]
    ) -> None:
        self.agents[index].profile.update_profile(trait_to_description)

    def __iter__(self) -> Iterator[Agent]:
        return iter(self.agents)

    def __len__(self) -> int:
        return len(self.agents)

    def __getitem__(self, index: int) -> Agent:
        return self.agents[index]
