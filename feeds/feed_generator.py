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
    """Generate a feed for an agent."""
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
    """Generate feeds for all the agents.
    
    Returns a dictionary of agent handles to lists of hydrated BlueskyFeedPost models.

    Does the following:
    1. Generates a feed for each agent.
    2. Writes the unhydrated feeds to the database.
    3. Hydrates the posts for each feed.
    4. Returns a dictionary of agent handles to lists of hydrated BlueskyFeedPost models.
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
        # using [] instead of get() to raise an error if the post is not found.
        agent_to_hydrated_feeds[agent_handle] = [uri_to_post[post_uri] for post_uri in feed.post_uris]
    return agent_to_hydrated_feeds
