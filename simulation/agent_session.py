from typing import Optional

from pydantic import BaseModel

from agent.initialize_agents import Agent


class FeedPost(BaseModel):
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
    desired_action: Optional[str] = (
        None  # desired action, e.g., like/post/comment/follow, etc.
    )
    desired_action_rationale: Optional[str] = (
        None  # description about why the user wants to do the desired action, if any.
    )


# flesh this out. This should be a class that contains how the user engaged with a post.
class UserEngagement(BaseModel):
    """Container class for a user engagement."""

    post: FeedPost
    observation: FeedObservation
    engagement: dict  # engagement, e.g., like/post/comment/follow, etc.


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
        pass


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
        pass

    def engage_with_feed(
        self, feed: Feed, observations: list[FeedObservation]
    ) -> list[UserEngagement]:
        """Engage with the feed, if any desired actions."""
        if len(feed) != len(observations):
            raise ValueError("Number of posts and observations must be the same.")

        engagements = []

        for post, observation in zip(feed, observations):
            if observation.desired_action:
                engagements.append(
                    self.engage_with_post(post=post, observation=observation)
                )

        return engagements


class AgentSession:
    """Single round of interaction for a given agent."""

    def __init__(self, agent: Agent):
        self.agent = agent
        self.user_engagement_manager = UserEngagementManager(agent=agent)
        self.user_feed_manager = UserFeedManager(agent=agent)
        self.user_feed_scroll_manager = UserFeedScrollManager(agent=agent)

    def scroll_feed(self):
        feed = self.user_feed_manager.load_latest_feed()
        observations = self.user_feed_scroll_manager.scroll_feed(feed=feed)
        engagements = self.user_engagement_manager.engage_with_feed(
            feed=feed, observations=observations
        )
        self.update_beliefs(
            feed=feed, observations=observations, engagements=engagements
        )

    def update_beliefs(
        self,
        feed: Feed,
        observations: list[FeedObservation],
        engagements: list[UserEngagement],
    ):
        """Update the agent's beliefs based on the feed, observations, and engagements."""
        pass

    def run(self):
        """Run the agent session."""
        print(f"Running agent session for agent {self.agent.agent_id}")
        self.scroll_feed()
        print(f"Finished scroling feed for agent {self.agent.agent_id}")


if __name__ == "__main__":
    agent = Agent(agent_id="test_agent")
    session = AgentSession(agent=agent)
    session.run()
