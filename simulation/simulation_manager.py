from config.models import SimulationConfig

from memory.memory_manager import GlobalMemoryManager
from simulation.constants import DEFAULT_NUM_ROUNDS


class SimulationManager:
    """Manages the simulation of the agents."""

    def __init__(self, config: SimulationConfig):
        self.config = config

    def init_agents(self):
        self.agents = []

    def init_simulation(self):
        self.global_memory_manager = GlobalMemoryManager()
        self.global_memory_manager.init_memory_managers(self.agents)

    def simulate_round(self):
        pass

    def simulate_rounds(self, num_rounds: int = DEFAULT_NUM_ROUNDS):
        print("Initializing simulation.")
        self.init_simulation()
        print(f"Simulating {num_rounds} total rounds...")
        for i in range(num_rounds):
            print(f"Simulating round {i+1}/{num_rounds}")
            self.simulate_round()
        print(f"Finished simulating {num_rounds} rounds. Exporting results.")
        self.export_simulation_results()

    def export_simulation_results(self):
        pass


if __name__ == "__main__":
    config = SimulationConfig()
    simulation_manager = SimulationManager(config=config)
    simulation_manager.init_agents()
    simulation_manager.init_simulation()
    simulation_manager.simulate_rounds()
