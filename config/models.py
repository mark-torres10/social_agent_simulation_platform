class SimulationConfig:
    def __init__(self, num_agents=10, traits_list=None, agent_ids=None):
        self.num_agents = num_agents
        self.traits_list = traits_list
        self.agent_ids = agent_ids


class AgentConfig:
    def __init__(self, agent_name="default_agent"):
        self.agent_name = agent_name
