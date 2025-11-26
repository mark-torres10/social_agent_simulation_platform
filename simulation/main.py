from ai.agents import SocialMediaAgent, record_agent_actions
from ai.create_initial_agents import create_initial_agents
from db.models import BlueskyFeedPost
from feeds.feed_generator import generate_feeds
from lib.utils import get_current_timestamp

def simulate_turn(agents: list[SocialMediaAgent], run_id: str, turn_number: int) -> dict:
    """
    Simulate a single turn of the social media agents and return aggregated action counts.
    
    Parameters:
        agents (list[SocialMediaAgent]): Agents participating in this turn.
        run_id (str): Identifier for the current simulation run.
        turn_number (int): Zero-based index of the current turn.
    
    Returns:
        dict: Mapping with keys "likes", "comments", and "follows" whose values are the total counts of each action performed by all agents during this turn.
    """
    total_actions = {
        "likes": 0,
        "comments": 0,
        "follows": 0,
    }

    # generate all the feeds for the agents.
    agent_to_hydrated_feeds: dict[str, list[BlueskyFeedPost]] = generate_feeds(
        agents=agents,
        run_id=run_id,
        turn_number=turn_number
    )

    # iterate through all the agents.
    for agent in agents:
        feed: list[BlueskyFeedPost] = agent_to_hydrated_feeds[agent.handle]

        likes = agent.like_posts(posts=feed)
        comments = agent.comment_posts(posts=feed)
        follows = agent.follow_users(posts=feed)

        record_agent_actions({
            "likes": likes,
            "comments": comments,
            "follows": follows,
        })

        total_actions["likes"] += len(likes)
        total_actions["comments"] += len(comments)
        total_actions["follows"] += len(follows)

    return total_actions

def do_simulation_run(run_id: str, total_turns: int) -> None:
    """
    Run a complete simulation for the given run identifier and number of turns.
    
    Creates the initial agents, executes simulate_turn once per turn (0-based), prints per-turn action summaries, and prints a completion message when finished.
    
    Parameters:
        run_id (str): Unique identifier for this simulation run.
        total_turns (int): Number of turns to execute (non-negative integer).
    """
    agents: list[SocialMediaAgent] = create_initial_agents()
    for i in range(total_turns):
        print(f"Turn {i}")
        total_actions = simulate_turn(
            agents=agents,
            run_id=run_id,
            turn_number=i
        )
        print(f"Total actions on turn {i}: {total_actions}")
    print(f"Simulation run {run_id} completed in {total_turns} turns.")

def main():
    """
    Execute a simulation run using a timestamped run identifier and ten turns.
    
    This function obtains the current timestamp, constructs a run ID in the form "run_<timestamp>", sets the simulation length to 10 turns, and invokes do_simulation_run with those values.
    """
    start_timestamp = get_current_timestamp()
    run_id = f"run_{start_timestamp}"
    total_turns = 10
    do_simulation_run(run_id=run_id, total_turns=total_turns)


if __name__ == "__main__":
    main()