"""Logic for initializing agents."""

from typing import List, Dict, Optional
from agent.components.persistent.profile import AgentProfile

DEFAULT_NUM_AGENTS = 10


class Agent:
    def __init__(self, profile: AgentProfile, agent_id: Optional[str] = None):
        self.profile = profile
        self.agent_id = agent_id

    def __str__(self):
        return f"Agent(id={self.agent_id})\n{str(self.profile)}"

    def __repr__(self):
        return self.__str__()


def initialize_agents(
    num_agents: int = DEFAULT_NUM_AGENTS,
    traits_list: Optional[List[Dict[str, str]]] = None,
    agent_ids: Optional[List[str]] = None,
) -> List[Agent]:
    """
    Initialize a list of agents.
    - num_agents: number of agents to create (ignored if traits_list is provided)
    - traits_list: list of trait_to_description dicts, one per agent
    - agent_ids: optional list of agent IDs; if not provided, defaults to string indices
    Returns: list of Agent objects
    """
    agents = []
    if traits_list is not None:
        n = len(traits_list)
        ids = agent_ids if agent_ids is not None else [str(i) for i in range(n)]
        for i, trait_dict in enumerate(traits_list):
            profile = AgentProfile(trait_to_description=trait_dict)
            agent_id = ids[i] if i < len(ids) else None
            agents.append(Agent(profile, agent_id=agent_id))
    else:
        n = num_agents
        ids = agent_ids if agent_ids is not None else [str(i) for i in range(n)]
        for i in range(n):
            profile = AgentProfile()
            agent_id = ids[i] if i < len(ids) else None
            agents.append(Agent(profile, agent_id=agent_id))
    return agents
