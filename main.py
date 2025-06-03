from simulation.simulation_manager import SimulationManager


if __name__ == "__main__":
    config_path = "config/simulation_config.yml"
    simulation_manager = SimulationManager(config_path=config_path)
    simulation_manager.init_agents()
    simulation_manager.init_simulation()
    simulation_manager.simulate_rounds()
