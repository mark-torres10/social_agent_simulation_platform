from typing import Optional

from agent.initialize_agents import initialize_agents
from config.config_loader import load_config
from memory.memory_manager import GlobalMemoryManager
from simulation.agent_session import AgentSession
from simulation.constants import DEFAULT_NUM_ROUNDS
from agent.agent_manager import AgentManager


class SimulationManager:
    """Manages the simulation of the agents."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Args:
            config_path: Path to the simulation config YAML file. If None or invalid, uses default config.
        """
        self.config = load_config(config_path, config_type="simulation")

    def init_agents(self):
        num_agents = getattr(self.config, "num_agents", 10)
        traits_list = getattr(self.config, "traits_list", None)
        agent_ids = getattr(self.config, "agent_ids", None)

        self.agents = initialize_agents(
            num_agents=num_agents, traits_list=traits_list, agent_ids=agent_ids
        )
        self.agent_manager = AgentManager(agents=self.agents)

    def init_simulation(self):
        self.global_memory_manager = GlobalMemoryManager()
        self.global_memory_manager.init_memory_managers(self.agents)

    def simulate_round(self):
        # NOTE: would also need to record the metadata here for the round,
        # whatever that metadata happens to be.
        for agent in self.agents:
            agent_session = AgentSession(agent=agent)
            agent_session.run()

    def simulate_rounds(self, num_rounds: int = DEFAULT_NUM_ROUNDS):
        print("Initializing simulation.")
        self.init_simulation()
        print(f"Simulating {num_rounds} total rounds...")
        breakpoint()
        for i in range(num_rounds):
            print(f"Simulating round {i+1}/{num_rounds}")
            self.simulate_round()
        print(f"Finished simulating {num_rounds} rounds. Exporting results.")
        self.export_simulation_results()

    def export_simulation_results(self):
        pass
