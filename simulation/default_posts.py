from faker import Faker

from feeds.models import FeedPost
from lib.helper import get_current_timestamp_str

fake = Faker()


def generate_dummy_posts(num_posts: int = 10) -> list[FeedPost]:
    """Generate dummy posts for testing.

    Args:
        num_posts: Number of posts to generate. Defaults to 10.

    Returns:
        list[FeedPost]: List of generated dummy posts
    """
    posts = []
    for i in range(num_posts):
        post = FeedPost(
            post_id=f"author_{i}_{get_current_timestamp_str()}",
            author=f"author_{i}",
            timestamp=get_current_timestamp_str(),
            text=fake.text(),
            attachments=None,
            liked_by=None,
            shared_by=None,
            comments=None,
        )
        posts.append(post)
    return posts
