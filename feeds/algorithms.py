"""Container logic for different feed generation algorithms"""

# TODO: for now, we'll generate the feeds in real-time during the simulations,
# but in practice we would generate them offline.
from db.models import GeneratedFeed
from ai.agents import SocialMediaAgent
from db.models import BlueskyFeedPost

from lib.utils import get_current_timestamp


MAX_POSTS_PER_FEED = 20

def generate_chronological_feed(
    posts: list[BlueskyFeedPost],
    agent: SocialMediaAgent,
    limit: int = MAX_POSTS_PER_FEED
) -> GeneratedFeed:
    """Generate a chronological feed for an agent."""
    candidate_posts = [p for p in posts if p.author_handle != agent.handle]
    # TODO: fast follow: insert randomness so that the feed isn't always the
    # same across rounds.
    sorted_posts = sorted(candidate_posts, key=lambda p: p.created_at, reverse=True)
    sorted_posts = sorted_posts[:limit]
    feed_id = GeneratedFeed.generate_feed_id()
    feed = GeneratedFeed(
        feed_id=feed_id,
        agent_handle=agent.handle,
        created_at=get_current_timestamp(),
        items=sorted_posts
    )
    return feed


# TODO: placeholder for next ticket.
def generate_rag_feed() -> GeneratedFeed:
    pass
