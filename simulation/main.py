import sys

from ai.agents import SocialMediaAgent, record_agent_actions
from ai.create_initial_agents import create_initial_agents
from db.db import initialize_database
from db.models import BlueskyFeedPost, RunConfig, Run, RunStatus
from db.repositories.run_repository import RunRepository
from feeds.feed_generator import generate_feeds

def simulate_turn(agents: list[SocialMediaAgent], run_id: str, turn_number: int) -> dict:
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

        likes = agent.like_posts(feed=feed)
        comments = agent.comment_posts(feed=feed)
        follows = agent.follow_users(feed=feed)

        record_agent_actions({
            "likes": likes,
            "comments": comments,
            "follows": follows,
        })

        total_actions["likes"] += len(likes)
        total_actions["comments"] += len(comments)
        total_actions["follows"] += len(follows)

    return total_actions

def do_simulation_run(
    run_repo: RunRepository,
    config: RunConfig
) -> None:
    """Execute a simulation run.
    
    Args:
        run_repo: Repository for run operations
        config: Configuration for the run
    """
    run: Run = run_repo.create_run(config)
    print(f"Created run {run.run_id}: {config.num_agents} agents, {config.num_turns} turns")
    agents: list[SocialMediaAgent] = create_initial_agents()
    agents = agents[:config.num_agents]
    try:
        for i in range(run.total_turns):
            print(f"Turn {i}")
            total_actions = simulate_turn(
                agents=agents,
                run_id=run.run_id,
                turn_number=i
            )
            print(f"Total actions on turn {i}: {total_actions}")
        run_repo.update_run_status(run.run_id, RunStatus.COMPLETED)
    except Exception as e:
        # Attempt to update status, but don't let status update failure mask original error
        try:
            run_repo.update_run_status(run.run_id, RunStatus.FAILED)
        except Exception as status_error:
            print(f"Error: Failed to update run status to FAILED: {status_error}")
            # Continue to raise original exception
        raise RuntimeError(f"Failed to complete simulation run {run.run_id}: {e}") from e
    print(f"Simulation run {run.run_id} completed in {run.total_turns} turns.")

def main():
    """CLI entry point - creates repository and runs simulation."""
    initialize_database()

    from db.repositories.run_repository import SQLiteRunRepository
    run_repo = SQLiteRunRepository()

    config = RunConfig(
        num_agents=10,
        num_turns=10,
    )

    try:
        do_simulation_run(run_repo=run_repo, config=config)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
