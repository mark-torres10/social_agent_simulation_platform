from typing import Optional, Iterator
from agent.agent import Agent
from agent.initialize_agents import initialize_agents


class AgentManager:
    def __init__(self, agents: Optional[list[Agent]] = None):
        if not agents:
            self.init_agents()
        else:
            self.agents = agents

    def init_agents(
        self,
        num_agents: int = 1,
        traits_list: Optional[list[dict[str, str]]] = None,
        agent_ids: Optional[list[str]] = None,
    ):
        agents: list[Agent] = initialize_agents(
            num_agents=num_agents, traits_list=traits_list, agent_ids=agent_ids
        )
        self.agents = agents

    def get_agent(self, index: int) -> Agent:
        return self.agents[index]

    def get_agents(self) -> list[Agent]:
        return self.agents

    def update_agent_profile(
        self, index: int, trait_to_description: dict[str, str]
    ) -> None:
        self.agents[index].profile.update_profile(trait_to_description)

    def __iter__(self) -> Iterator[Agent]:
        return iter(self.agents)

    def __len__(self) -> int:
        return len(self.agents)

    def __getitem__(self, index: int) -> Agent:
        return self.agents[index]
