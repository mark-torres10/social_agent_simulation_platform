from ai.agents import SocialMediaAgent
from db.models import BlueskyFeedPost, GeneratedFeed
from db.repositories.feed_post_repository import create_sqlite_feed_post_repository
from db.repositories.generated_feed_repository import (
    create_sqlite_generated_feed_repository,
)
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
    generated_feed_repo = create_sqlite_generated_feed_repository()
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
        generated_feed_repo.create_or_update_generated_feed(feed)
        feeds[agent.handle] = feed

    # now iterate through all the feeds and hydrate the posts.
    # PERFORMANCE NOTE: This loads ALL posts into memory, which is inefficient
    # for large datasets. This approach is acceptable for small-scale simulations
    # but should be optimized when the dataset grows beyond ~10K posts. Potential
    # optimizations include:
    # - Batch queries: Query posts by URI sets instead of loading all
    # - Pagination: Process feeds in batches
    # - Caching: Cache frequently accessed posts
    # - Database indexes: Ensure proper indexes on uri column
    # TODO: Optimize when post count exceeds 10K or performance degrades
    feed_post_repo = create_sqlite_feed_post_repository()
    all_posts = feed_post_repo.list_all_feed_posts()
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
