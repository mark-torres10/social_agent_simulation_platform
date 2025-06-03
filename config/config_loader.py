import os
import yaml
from config.models import SimulationConfig, AgentConfig


def load_config(path: str, config_type: str = "simulation"):
    """
    Load a SimulationConfig or AgentConfig from a YAML file at the given path.
    If loading fails, return the default config object.
    Args:
        path: Path to the YAML config file.
        config_type: 'simulation' or 'agent'.
    Returns:
        SimulationConfig or AgentConfig instance.
    """
    if not path or not os.path.exists(path):
        return SimulationConfig() if config_type == "simulation" else AgentConfig()
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        if config_type == "simulation":
            return SimulationConfig(
                num_agents=data.get("num_agents", 10),
                traits_list=data.get("traits_list", None),
                agent_ids=data.get("agent_ids", None),
            )
        elif config_type == "agent":
            return AgentConfig(agent_name=data.get("agent_name", "default_agent"))
        else:
            raise ValueError(f"Unknown config_type: {config_type}")
    except Exception:
        # Log error if needed
        return SimulationConfig() if config_type == "simulation" else AgentConfig()
