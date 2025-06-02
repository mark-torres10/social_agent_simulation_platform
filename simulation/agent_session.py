from typing import Optional

from pydantic import BaseModel

from agent.agent import Agent


class FeedPost(BaseModel):
    """Container class for a feed post."""

    post_id: str  # author + timestamp.
    author: str
    timestamp: str
    text: str
    attachments: list[
        str
    ]  # description of attachments (e.g., images, links). Instead of including images, just include description of image.
    liked_by: list[str]
    shared_by: list[str]
    comments: list[str]


class Feed(BaseModel):
    """Container class for a feed."""

    posts: list[FeedPost]

    def __len__(self):
        return len(self.posts)


class FeedObservation(BaseModel):
    """Observation/thought that a user has about a post in a feed."""

    metadata: dict  # metadata about the post.
    observation: Optional[str] = None  # observations about the post, if any
    desired_actions: Optional[dict] = (
        None  # desired action(s), e.g., like/post/comment/follow, etc, and the rationale for each.
    )


# flesh this out. This should be a class that contains how the user engaged with a post.
class UserEngagement(BaseModel):
    """Container class for a user engagement."""

    metadata: dict  # metadata about the post.
    observation: FeedObservation
    engagement: (
        dict  # engagement, e.g., like/post/comment/follow, etc., plus rationale.
    )


class UserFeedManager:
    """Manages the feed for a given user."""

    def __init__(self, agent: Agent):
        self.agent = agent

    def load_latest_feed():
        pass


class UserFeedScrollManager:
    """Base class enclosing any thoughts or observations that the agent
    has about the posts in a feed. Simulates scrolling the feed and then
    returning any thoughts or comments that the user has about posts in the feed.
    """

    def __init__(self, agent: Agent):
        self.agent = agent

    def scroll_feed(self, feed: Feed) -> list[FeedObservation]:
        return [self.make_observation_about_post(post) for post in feed]

    # TODO: should be an LLM prompt + based on their engagement tendencies.
    def make_observation_about_post(self, post: FeedPost) -> FeedObservation:
        """Agent makes an observation about the feed."""
        metadata = {
            "post_id": post.post_id,
            "author": post.author,
            "timestamp": post.timestamp,
        }

        # stub this for now. Probably should be an LLM prompt.
        observation = f"I think this post is about {post.text}"

        # stub this for now. Probably should be an LLM prompt.
        desired_actions = {
            "like": f"I like this post because it is about {post.text}",
            "post": f"I want to post this because it is about {post.text}",
            "comment": f"I want to comment on this because it is about {post.text}",
            "follow": f"I want to follow this because it is about {post.text}",
        }

        return FeedObservation(
            metadata=metadata,
            observation=observation,
            desired_actions=desired_actions,
        )


class UserEngagementManager:
    """Manages the engagement of a user with the feed (e.g., likes, shares, comments)."""

    def __init__(self, agent: Agent):
        self.agent = agent

    def get_context_for_engagement(self, engagement_type: str, metadata: dict):
        """Fetch any context relevant for any engagement.

        For example, if a user is writing a post, we want to pull the post
        as well as their past preferences.
        """
        pass

    def engage_with_post(
        self, post: FeedPost, observation: FeedObservation
    ) -> UserEngagement:
        """Engage with a post, if any desired actions."""
        metadata = {
            "post_id": post.post_id,
            "author": post.author,
            "timestamp": post.timestamp,
        }
        engagement = {}
        for action in observation.desired_actions:
            engagement[action] = observation.desired_actions[action]

        return UserEngagement(
            metadata=metadata,
            observation=observation,
            engagement=engagement,
        )

    def engage_with_feed(
        self, feed: Feed, observations: list[FeedObservation]
    ) -> list[UserEngagement | None]:
        """Engage with the feed, if any desired actions."""
        if len(feed) != len(observations):
            raise ValueError("Number of posts and observations must be the same.")

        engagements: list[UserEngagement | None] = []

        for post, observation in zip(feed, observations):
            if observation.desired_actions:
                engagements.append(
                    self.engage_with_post(post=post, observation=observation)
                )
            else:
                engagements.append(None)

        return engagements


class AgentSession:
    """Single round of interaction for a given agent."""

    def __init__(self, agent: Agent):
        self.agent = agent
        self.user_engagement_manager = UserEngagementManager(agent=agent)
        self.user_feed_manager = UserFeedManager(agent=agent)
        self.user_feed_scroll_manager = UserFeedScrollManager(agent=agent)

    def scroll_feed(self):
        feed: Feed = self.user_feed_manager.load_latest_feed()
        observations: list[FeedObservation] = self.user_feed_scroll_manager.scroll_feed(
            feed=feed
        )
        engagements: list[UserEngagement | None] = (
            self.user_engagement_manager.engage_with_feed(
                feed=feed, observations=observations
            )
        )
        self.update_beliefs(
            feed=feed, observations=observations, engagements=engagements
        )

    def update_beliefs(
        self,
        feed: Feed,
        observations: list[FeedObservation],
        engagements: list[UserEngagement | None],
    ):
        """Update the agent's beliefs based on the feed, observations, and engagements."""
        print(f"Updating beliefs for agent {self.agent.agent_id}")
        print(f"Feed: {len(feed)} posts. First post: {feed.posts[0]}")
        print(
            f"Observations: {len(observations)} observations. First observation: {observations[0]}"
        )
        print(
            f"Engagements: {len(engagements)} engagements. First engagement: {engagements[0]}"
        )
        updated_beliefs = self.agent.profile.beliefs.get_description()
        self.agent.update_beliefs(updated_beliefs=updated_beliefs)
        print(f"Finished updating beliefs for agent {self.agent.agent_id}")

    # TODO: connect with MemoryManager.
    def record_activity(self):
        """Record the activity of the agent."""
        pass

    def run(self):
        """Run the agent session."""
        print(f"Running agent session for agent {self.agent.agent_id}")
        self.scroll_feed()
        self.record_activity()
        print(f"Finished scroling feed for agent {self.agent.agent_id}")


if __name__ == "__main__":
    agent = Agent(agent_id="test_agent")
    session = AgentSession(agent=agent)
    session.run()
