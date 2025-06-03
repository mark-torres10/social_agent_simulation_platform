from simulation.agent_session import Feed
from simulation.default_posts import generate_dummy_posts


def build_feed_for_agent(agent_id: str) -> Feed:
    """Build a feed for a given agent."""
    print(f"Building feed for agent {agent_id}...")
    return Feed(posts=generate_dummy_posts(num_posts=10))
