"""Contains logic for simulating a single round of interaction for a given agent."""

from agent.agent import Agent
from feeds.build_feeds import build_feed_for_agent
from feeds.models import Feed, FeedObservation, FeedPost
from simulation.models import UserEngagement


class UserFeedManager:
    """Manages the feed for a given user."""

    def __init__(self, agent: Agent):
        self.agent = agent

    # generic function for now. Would be the place to put some custom logic
    # for loading each user's feed. Probably would want to precompute the
    # feeds for the user, or dynamically adjust the recommendation algorithm
    # based on the user's engagements from the previous rounds.
    def load_latest_feed(self) -> Feed:
        return build_feed_for_agent(agent_id=self.agent.agent_id)


class UserFeedScrollManager:
    """Base class enclosing any thoughts or observations that the agent
    has about the posts in a feed. Simulates scrolling the feed and then
    returning any thoughts or comments that the user has about posts in the feed.
    """

    def __init__(self, agent: Agent):
        self.agent = agent

    def scroll_feed(self, feed: Feed) -> list[FeedObservation]:
        return [self.make_observation_about_post(post) for post in feed.posts]

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

    def scroll_feed(self):
        self.feed: Feed = self.user_feed_manager.load_latest_feed()
        self.observations: list[FeedObservation] = (
            self.user_feed_scroll_manager.scroll_feed(feed=self.feed)
        )
        self.engagements: list[UserEngagement | None] = (
            self.user_engagement_manager.engage_with_feed(
                feed=self.feed, observations=self.observations
            )
        )
        self.update_beliefs(
            feed=self.feed,
            observations=self.observations,
            engagements=self.engagements,
        )

    def run(self) -> dict:
        """Run the agent session."""
        print(f"Running agent session for agent {self.agent.agent_id}")
        self.scroll_feed()
        print(f"Finished scroling feed for agent {self.agent.agent_id}")
        return {
            "agent": self.agent,
            "feed": self.feed,
            "observations": self.observations,
            "engagements": self.engagements,
        }


if __name__ == "__main__":
    agent = Agent(agent_id="test_agent")
    session = AgentSession(agent=agent)
    session.run()
