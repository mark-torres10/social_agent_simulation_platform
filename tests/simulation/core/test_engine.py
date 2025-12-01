"""Tests for simulation.core.engine module."""

from unittest.mock import Mock

import pytest

from db.exceptions import RunNotFoundError
from db.repositories.feed_post_repository import FeedPostRepository
from db.repositories.generated_bio_repository import GeneratedBioRepository
from db.repositories.generated_feed_repository import GeneratedFeedRepository
from db.repositories.profile_repository import ProfileRepository
from db.repositories.run_repository import RunRepository
from simulation.core.engine import SimulationEngine
from simulation.core.models.feeds import GeneratedFeed
from simulation.core.models.posts import BlueskyFeedPost
from simulation.core.models.runs import Run, RunStatus
from simulation.core.models.turns import TurnData


@pytest.fixture
def mock_repos():
    """Fixture that creates and returns a dictionary of mock repositories."""
    return {
        "run_repo": Mock(spec=RunRepository),
        "profile_repo": Mock(spec=ProfileRepository),
        "feed_post_repo": Mock(spec=FeedPostRepository),
        "generated_bio_repo": Mock(spec=GeneratedBioRepository),
        "generated_feed_repo": Mock(spec=GeneratedFeedRepository),
    }


@pytest.fixture
def engine(mock_repos):
    """Fixture that creates and returns a SimulationEngine with mock repositories."""
    return SimulationEngine(
        run_repo=mock_repos["run_repo"],
        profile_repo=mock_repos["profile_repo"],
        feed_post_repo=mock_repos["feed_post_repo"],
        generated_bio_repo=mock_repos["generated_bio_repo"],
        generated_feed_repo=mock_repos["generated_feed_repo"],
    )


class TestSimulationEngineGetRun:
    """Tests for SimulationEngine.get_run method."""

    def test_returns_run_when_found(self, engine, mock_repos):
        """Test that get_run returns a Run when it exists."""
        # Arrange
        run_id = "run_123"
        expected_run = Run(
            run_id=run_id,
            created_at="2024_01_01-12:00:00",
            total_turns=10,
            total_agents=5,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.RUNNING,
            completed_at=None,
        )
        mock_repos["run_repo"].get_run.return_value = expected_run

        # Act
        result = engine.get_run(run_id)

        # Assert
        assert result is not None
        assert result == expected_run
        mock_repos["run_repo"].get_run.assert_called_once_with(run_id)

    def test_returns_none_when_run_not_found(self, engine, mock_repos):
        """Test that get_run returns None when run does not exist."""
        # Arrange
        run_id = "nonexistent_run"
        mock_repos["run_repo"].get_run.return_value = None

        # Act
        result = engine.get_run(run_id)

        # Assert
        assert result is None
        mock_repos["run_repo"].get_run.assert_called_once_with(run_id)

    def test_raises_value_error_for_empty_run_id(self, engine, mock_repos):
        """Test that get_run raises ValueError for empty run_id."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="run_id cannot be empty"):
            engine.get_run("")

        # Verify repository was not called
        mock_repos["run_repo"].get_run.assert_not_called()

    def test_raises_value_error_for_whitespace_only_run_id(self, engine, mock_repos):
        """Test that get_run raises ValueError for whitespace-only run_id."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="run_id cannot be empty"):
            engine.get_run("   ")

        # Verify repository was not called
        mock_repos["run_repo"].get_run.assert_not_called()

    def test_raises_value_error_for_none_run_id(self, engine, mock_repos):
        """Test that get_run raises ValueError for None run_id."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="run_id cannot be empty"):
            engine.get_run(None)  # type: ignore

        # Verify repository was not called
        mock_repos["run_repo"].get_run.assert_not_called()

    def test_repository_exceptions_propagate(self, engine, mock_repos):
        """Test that repository exceptions propagate without wrapping."""
        # Arrange
        run_id = "run_123"
        original_error = RunNotFoundError(run_id)
        mock_repos["run_repo"].get_run.side_effect = original_error

        # Act & Assert
        with pytest.raises(RunNotFoundError) as exc_info:
            engine.get_run(run_id)

        # Verify it's the same exception (not wrapped)
        assert exc_info.value is original_error
        mock_repos["run_repo"].get_run.assert_called_once_with(run_id)


class TestSimulationEngineListRuns:
    """Tests for SimulationEngine.list_runs method."""

    def test_returns_list_of_runs(self, engine, mock_repos):
        """Test that list_runs returns a list of runs."""
        # Arrange
        expected_runs = [
            Run(
                run_id="run_1",
                created_at="2024_01_01-12:00:00",
                total_turns=10,
                total_agents=5,
                started_at="2024_01_01-12:00:00",
                status=RunStatus.RUNNING,
                completed_at=None,
            ),
            Run(
                run_id="run_2",
                created_at="2024_01_02-12:00:00",
                total_turns=20,
                total_agents=10,
                started_at="2024_01_02-12:00:00",
                status=RunStatus.COMPLETED,
                completed_at="2024_01_02-13:00:00",
            ),
        ]
        mock_repos["run_repo"].list_runs.return_value = expected_runs

        # Act
        result = engine.list_runs()

        # Assert
        assert result == expected_runs
        assert len(result) == 2
        mock_repos["run_repo"].list_runs.assert_called_once()

    def test_returns_empty_list_when_no_runs_exist(self, engine, mock_repos):
        """Test that list_runs returns empty list when no runs exist."""
        # Arrange
        mock_repos["run_repo"].list_runs.return_value = []

        # Act
        result = engine.list_runs()

        # Assert
        assert result == []
        assert len(result) == 0
        mock_repos["run_repo"].list_runs.assert_called_once()

    def test_repository_exceptions_propagate(self, engine, mock_repos):
        """Test that repository exceptions propagate without wrapping."""
        # Arrange
        original_error = RuntimeError("Database connection failed")
        mock_repos["run_repo"].list_runs.side_effect = original_error

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            engine.list_runs()

        # Verify it's the same exception (not wrapped)
        assert exc_info.value is original_error
        mock_repos["run_repo"].list_runs.assert_called_once()


class TestSimulationEngineGetTurnData:
    """Tests for SimulationEngine.get_turn_data method."""

    def test_returns_turn_data_with_feeds_and_posts(self, engine, mock_repos):
        """Test that get_turn_data returns TurnData with correct feeds and posts."""
        # Arrange
        run_id = "run_123"
        turn_number = 0
        run = Run(
            run_id=run_id,
            created_at="2024_01_01-12:00:00",
            total_turns=10,
            total_agents=5,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.RUNNING,
            completed_at=None,
        )

        # Create feeds
        feed1 = GeneratedFeed(
            feed_id="feed_1",
            run_id=run_id,
            turn_number=turn_number,
            agent_handle="agent1.bsky.social",
            post_uris=["uri1", "uri2"],
            created_at="2024_01_01-12:00:00",
        )
        feed2 = GeneratedFeed(
            feed_id="feed_2",
            run_id=run_id,
            turn_number=turn_number,
            agent_handle="agent2.bsky.social",
            post_uris=["uri3"],
            created_at="2024_01_01-12:00:01",
        )

        # Create posts
        post1 = BlueskyFeedPost(
            id="uri1",
            uri="uri1",
            author_display_name="Author 1",
            author_handle="author1.bsky.social",
            text="Post 1 text",
            bookmark_count=0,
            like_count=5,
            quote_count=0,
            reply_count=2,
            repost_count=1,
            created_at="2024_01_01-12:00:00",
        )
        post2 = BlueskyFeedPost(
            id="uri2",
            uri="uri2",
            author_display_name="Author 2",
            author_handle="author2.bsky.social",
            text="Post 2 text",
            bookmark_count=1,
            like_count=10,
            quote_count=0,
            reply_count=3,
            repost_count=2,
            created_at="2024_01_01-12:01:00",
        )
        post3 = BlueskyFeedPost(
            id="uri3",
            uri="uri3",
            author_display_name="Author 3",
            author_handle="author3.bsky.social",
            text="Post 3 text",
            bookmark_count=0,
            like_count=0,
            quote_count=0,
            reply_count=0,
            repost_count=0,
            created_at="2024_01_01-12:02:00",
        )

        mock_repos["run_repo"].get_run.return_value = run
        mock_repos["generated_feed_repo"].read_feeds_for_turn.return_value = [
            feed1,
            feed2,
        ]
        mock_repos["feed_post_repo"].read_feed_posts_by_uris.return_value = [
            post1,
            post2,
            post3,
        ]

        # Act
        result = engine.get_turn_data(run_id, turn_number)

        # Assert
        assert result is not None
        assert isinstance(result, TurnData)
        assert result.turn_number == turn_number
        assert result.agents == []
        assert result.actions == {}
        assert len(result.feeds) == 2
        assert "agent1.bsky.social" in result.feeds
        assert "agent2.bsky.social" in result.feeds
        assert len(result.feeds["agent1.bsky.social"]) == 2
        assert len(result.feeds["agent2.bsky.social"]) == 1
        assert result.feeds["agent1.bsky.social"][0].uri == "uri1"
        assert result.feeds["agent1.bsky.social"][1].uri == "uri2"
        assert result.feeds["agent2.bsky.social"][0].uri == "uri3"

        # Verify repository calls
        mock_repos["run_repo"].get_run.assert_called_once_with(run_id)
        mock_repos["generated_feed_repo"].read_feeds_for_turn.assert_called_once_with(
            run_id, turn_number
        )
        mock_repos["feed_post_repo"].read_feed_posts_by_uris.assert_called_once()
        # Verify batch query was called with all URIs
        call_args = mock_repos["feed_post_repo"].read_feed_posts_by_uris.call_args[0][0]
        assert set(call_args) == {"uri1", "uri2", "uri3"}

    def test_returns_none_when_turn_does_not_exist(self, engine, mock_repos):
        """Test that get_turn_data returns None when turn doesn't exist (no feeds)."""
        # Arrange
        run_id = "run_123"
        turn_number = 0
        run = Run(
            run_id=run_id,
            created_at="2024_01_01-12:00:00",
            total_turns=10,
            total_agents=5,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.RUNNING,
            completed_at=None,
        )

        mock_repos["run_repo"].get_run.return_value = run
        mock_repos["generated_feed_repo"].read_feeds_for_turn.return_value = []

        # Act
        result = engine.get_turn_data(run_id, turn_number)

        # Assert
        assert result is None
        mock_repos["run_repo"].get_run.assert_called_once_with(run_id)
        mock_repos["generated_feed_repo"].read_feeds_for_turn.assert_called_once_with(
            run_id, turn_number
        )
        # Should not call feed_post_repo when no feeds
        mock_repos["feed_post_repo"].read_feed_posts_by_uris.assert_not_called()

    def test_raises_value_error_for_empty_run_id(self, engine, mock_repos):
        """Test that get_turn_data raises ValueError for empty run_id."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="run_id cannot be empty"):
            engine.get_turn_data("", 0)

        # Verify repositories were not called
        mock_repos["run_repo"].get_run.assert_not_called()
        mock_repos["generated_feed_repo"].read_feeds_for_turn.assert_not_called()

    def test_raises_value_error_for_negative_turn_number(self, engine, mock_repos):
        """Test that get_turn_data raises ValueError for negative turn_number."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="turn_number cannot be negative"):
            engine.get_turn_data("run_123", -1)

        # Verify repositories were not called
        mock_repos["run_repo"].get_run.assert_not_called()
        mock_repos["generated_feed_repo"].read_feeds_for_turn.assert_not_called()

    def test_raises_run_not_found_error_when_run_does_not_exist(
        self, engine, mock_repos
    ):
        """Test that get_turn_data raises RunNotFoundError for non-existent run."""
        # Arrange
        run_id = "nonexistent_run"
        turn_number = 0
        mock_repos["run_repo"].get_run.return_value = None

        # Act & Assert
        with pytest.raises(RunNotFoundError) as exc_info:
            engine.get_turn_data(run_id, turn_number)

        assert exc_info.value.run_id == run_id
        mock_repos["run_repo"].get_run.assert_called_once_with(run_id)
        # Should not call other repositories
        mock_repos["generated_feed_repo"].read_feeds_for_turn.assert_not_called()
        mock_repos["feed_post_repo"].read_feed_posts_by_uris.assert_not_called()

    def test_handles_missing_posts_gracefully(self, engine, mock_repos):
        """Test that get_turn_data handles missing posts gracefully (skips missing, returns partial feeds)."""
        # Arrange
        run_id = "run_123"
        turn_number = 0
        run = Run(
            run_id=run_id,
            created_at="2024_01_01-12:00:00",
            total_turns=10,
            total_agents=5,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.RUNNING,
            completed_at=None,
        )

        feed = GeneratedFeed(
            feed_id="feed_1",
            run_id=run_id,
            turn_number=turn_number,
            agent_handle="agent1.bsky.social",
            post_uris=[
                "uri1",
                "uri2",
                "missing_uri",
            ],  # uri2 and missing_uri don't exist
            created_at="2024_01_01-12:00:00",
        )

        post1 = BlueskyFeedPost(
            id="uri1",
            uri="uri1",
            author_display_name="Author 1",
            author_handle="author1.bsky.social",
            text="Post 1 text",
            bookmark_count=0,
            like_count=5,
            quote_count=0,
            reply_count=2,
            repost_count=1,
            created_at="2024_01_01-12:00:00",
        )

        mock_repos["run_repo"].get_run.return_value = run
        mock_repos["generated_feed_repo"].read_feeds_for_turn.return_value = [feed]
        # Only uri1 exists, uri2 and missing_uri don't
        mock_repos["feed_post_repo"].read_feed_posts_by_uris.return_value = [post1]

        # Act
        result = engine.get_turn_data(run_id, turn_number)

        # Assert
        assert result is not None
        assert len(result.feeds["agent1.bsky.social"]) == 1  # Only uri1 found
        assert result.feeds["agent1.bsky.social"][0].uri == "uri1"
        # Verify batch query was called with all URIs (including missing ones)
        call_args = mock_repos["feed_post_repo"].read_feed_posts_by_uris.call_args[0][0]
        assert set(call_args) == {"uri1", "uri2", "missing_uri"}

    def test_handles_empty_feeds_when_all_posts_missing(self, engine, mock_repos):
        """Test that get_turn_data returns TurnData with empty feeds dict when all posts missing."""
        # Arrange
        run_id = "run_123"
        turn_number = 0
        run = Run(
            run_id=run_id,
            created_at="2024_01_01-12:00:00",
            total_turns=10,
            total_agents=5,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.RUNNING,
            completed_at=None,
        )

        feed = GeneratedFeed(
            feed_id="feed_1",
            run_id=run_id,
            turn_number=turn_number,
            agent_handle="agent1.bsky.social",
            post_uris=["missing_uri1", "missing_uri2"],
            created_at="2024_01_01-12:00:00",
        )

        mock_repos["run_repo"].get_run.return_value = run
        mock_repos["generated_feed_repo"].read_feeds_for_turn.return_value = [feed]
        # No posts found
        mock_repos["feed_post_repo"].read_feed_posts_by_uris.return_value = []

        # Act
        result = engine.get_turn_data(run_id, turn_number)

        # Assert
        assert result is not None
        assert result.turn_number == turn_number
        assert result.feeds["agent1.bsky.social"] == []  # Empty list, not None
        # Turn exists but data is incomplete

    def test_handles_multiple_feeds_with_overlapping_uris(self, engine, mock_repos):
        """Test that get_turn_data handles multiple feeds with overlapping post URIs correctly."""
        # Arrange
        run_id = "run_123"
        turn_number = 0
        run = Run(
            run_id=run_id,
            created_at="2024_01_01-12:00:00",
            total_turns=10,
            total_agents=5,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.RUNNING,
            completed_at=None,
        )

        # Two feeds with overlapping URIs
        feed1 = GeneratedFeed(
            feed_id="feed_1",
            run_id=run_id,
            turn_number=turn_number,
            agent_handle="agent1.bsky.social",
            post_uris=["uri1", "uri2"],  # uri2 is shared
            created_at="2024_01_01-12:00:00",
        )
        feed2 = GeneratedFeed(
            feed_id="feed_2",
            run_id=run_id,
            turn_number=turn_number,
            agent_handle="agent2.bsky.social",
            post_uris=["uri2", "uri3"],  # uri2 is shared
            created_at="2024_01_01-12:01:00",
        )

        post1 = BlueskyFeedPost(
            id="uri1",
            uri="uri1",
            author_display_name="Author 1",
            author_handle="author1.bsky.social",
            text="Post 1",
            bookmark_count=0,
            like_count=0,
            quote_count=0,
            reply_count=0,
            repost_count=0,
            created_at="2024_01_01-12:00:00",
        )
        post2 = BlueskyFeedPost(
            id="uri2",
            uri="uri2",
            author_display_name="Author 2",
            author_handle="author2.bsky.social",
            text="Post 2",
            bookmark_count=0,
            like_count=0,
            quote_count=0,
            reply_count=0,
            repost_count=0,
            created_at="2024_01_01-12:01:00",
        )
        post3 = BlueskyFeedPost(
            id="uri3",
            uri="uri3",
            author_display_name="Author 3",
            author_handle="author3.bsky.social",
            text="Post 3",
            bookmark_count=0,
            like_count=0,
            quote_count=0,
            reply_count=0,
            repost_count=0,
            created_at="2024_01_01-12:02:00",
        )

        mock_repos["run_repo"].get_run.return_value = run
        mock_repos["generated_feed_repo"].read_feeds_for_turn.return_value = [
            feed1,
            feed2,
        ]
        mock_repos["feed_post_repo"].read_feed_posts_by_uris.return_value = [
            post1,
            post2,
            post3,
        ]

        # Act
        result = engine.get_turn_data(run_id, turn_number)

        # Assert
        assert result is not None
        assert len(result.feeds) == 2
        assert len(result.feeds["agent1.bsky.social"]) == 2  # uri1, uri2
        assert len(result.feeds["agent2.bsky.social"]) == 2  # uri2, uri3
        # Verify batch query was called with unique URIs only (uri1, uri2, uri3)
        call_args = mock_repos["feed_post_repo"].read_feed_posts_by_uris.call_args[0][0]
        assert set(call_args) == {"uri1", "uri2", "uri3"}
        assert len(call_args) == 3  # No duplicates

    def test_repository_exceptions_propagate(self, engine, mock_repos):
        """Test that repository exceptions propagate without wrapping."""
        # Arrange
        run_id = "run_123"
        turn_number = 0
        run = Run(
            run_id=run_id,
            created_at="2024_01_01-12:00:00",
            total_turns=10,
            total_agents=5,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.RUNNING,
            completed_at=None,
        )

        original_error = RuntimeError("Database connection failed")
        mock_repos["run_repo"].get_run.return_value = run
        mock_repos[
            "generated_feed_repo"
        ].read_feeds_for_turn.side_effect = original_error

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            engine.get_turn_data(run_id, turn_number)

        # Verify it's the same exception (not wrapped)
        assert exc_info.value is original_error
        mock_repos["run_repo"].get_run.assert_called_once_with(run_id)
        mock_repos["generated_feed_repo"].read_feeds_for_turn.assert_called_once_with(
            run_id, turn_number
        )
