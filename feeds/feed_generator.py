from ai.agents import SocialMediaAgent
from db.models import GeneratedFeed, BlueskyFeedPost
from db.db import write_generated_feed, read_all_feed_posts
from feeds.algorithms import generate_chronological_feed
from feeds.candidate_generation import load_candidate_posts
from lib.utils import get_current_timestamp

def generate_feed(
    agent: SocialMediaAgent,
    candidate_posts: list[BlueskyFeedPost],
    run_id: str,
    turn_number: int,
    feed_type: str
) -> GeneratedFeed:
    """
    Create a GeneratedFeed for the given agent from candidate posts.
    
    Parameters:
        agent (SocialMediaAgent): The agent for whom the feed is generated.
        candidate_posts (list[BlueskyFeedPost]): Candidate posts to consider when building the feed.
        run_id (str): Identifier for the current run.
        turn_number (int): Turn number within the run.
        feed_type (str): Type of feed to generate; supported value: "chronological".
    
    Returns:
        GeneratedFeed: A feed object populated with feed_id, run_id, turn_number, agent_handle, post_uris, and created_at.
    
    Raises:
        NotImplementedError: If an unsupported feed_type is provided.
    """
    if feed_type == "chronological":
        feed_dict = generate_chronological_feed(
            candidate_posts=candidate_posts,
            agent=agent
        )
        feed = GeneratedFeed(
            feed_id=feed_dict["feed_id"],
            run_id=run_id,
            turn_number=turn_number,
            agent_handle=feed_dict["agent_handle"],
            post_uris=feed_dict["post_uris"],
            created_at=get_current_timestamp(),
        )
        return feed
    else:
        raise NotImplementedError(f"Feed type {feed_type} not implemented")


def generate_feeds(
    agents: list[SocialMediaAgent],
    run_id: str,
    turn_number: int,
    feed_type: str = "chronological"
) -> dict[str, list[BlueskyFeedPost]]:
    """
    Generate and hydrate feeds for a list of agents.
    
    Parameters:
        agents (list[SocialMediaAgent]): Agents to generate feeds for.
        run_id (str): Identifier for this run.
        turn_number (int): Turn number within the run.
        feed_type (str): Type of feed to generate; currently supports "chronological".
    
    Returns:
        dict[str, list[BlueskyFeedPost]]: Mapping from agent handle to the ordered, hydrated list of feed posts.
    
    Raises:
        ValueError: If a feed references a post URI that cannot be found during hydration.
    """
    feeds: dict[str, GeneratedFeed] = {}
    for agent in agents:
        # TODO: right now we load all posts per agent, but obviously
        # can optimize and personalize later to save on queries.
        candidate_posts: list[BlueskyFeedPost] = load_candidate_posts(
            agent=agent,
            run_id=run_id
        )
        feed: GeneratedFeed = generate_feed(
            agent=agent,
            candidate_posts=candidate_posts,
            run_id=run_id,
            turn_number=turn_number,
            feed_type=feed_type
        )
        write_generated_feed(feed)
        feeds[agent.handle] = feed

    # now iterate through all the feeds and hydrate the posts.
    # TODO: again, not efficient since this also loads ALL the posts.
    # but we can come back to efficiency later.
    all_posts = read_all_feed_posts()
    uri_to_post = {p.uri: p for p in all_posts}
    agent_to_hydrated_feeds: dict[str, list[BlueskyFeedPost]] = {}
    for agent_handle, feed in feeds.items():
        hydrated_posts = []
        for idx, post_uri in enumerate(feed.post_uris):
            if post_uri not in uri_to_post:
                raise ValueError(
                    f"Missing post URI in feed: agent_handle={agent_handle}, "
                    f"feed_id={feed.feed_id}, post_index={idx}, missing_uri={post_uri}"
                )
            hydrated_posts.append(uri_to_post[post_uri])
        agent_to_hydrated_feeds[agent_handle] = hydrated_posts
    return agent_to_hydrated_feeds