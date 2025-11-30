"""Tests for simulation.core.engine module."""

from unittest.mock import Mock

import pytest

from db.exceptions import RunNotFoundError
from db.models import Run, RunStatus
from db.repositories.feed_post_repository import FeedPostRepository
from db.repositories.generated_bio_repository import GeneratedBioRepository
from db.repositories.generated_feed_repository import GeneratedFeedRepository
from db.repositories.profile_repository import ProfileRepository
from db.repositories.run_repository import RunRepository
from simulation.core.engine import SimulationEngine


class TestSimulationEngineGetRun:
    """Tests for SimulationEngine.get_run method."""

    def test_returns_run_when_found(self):
        """Test that get_run returns a Run when it exists."""
        # Arrange
        mock_run_repo = Mock(spec=RunRepository)
        mock_profile_repo = Mock(spec=ProfileRepository)
        mock_feed_post_repo = Mock(spec=FeedPostRepository)
        mock_generated_bio_repo = Mock(spec=GeneratedBioRepository)
        mock_generated_feed_repo = Mock(spec=GeneratedFeedRepository)

        engine = SimulationEngine(
            run_repo=mock_run_repo,
            profile_repo=mock_profile_repo,
            feed_post_repo=mock_feed_post_repo,
            generated_bio_repo=mock_generated_bio_repo,
            generated_feed_repo=mock_generated_feed_repo,
        )

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
        mock_run_repo.get_run.return_value = expected_run

        # Act
        result = engine.get_run(run_id)

        # Assert
        assert result is not None
        assert result == expected_run
        mock_run_repo.get_run.assert_called_once_with(run_id)

    def test_returns_none_when_run_not_found(self):
        """Test that get_run returns None when run does not exist."""
        # Arrange
        mock_run_repo = Mock(spec=RunRepository)
        mock_profile_repo = Mock(spec=ProfileRepository)
        mock_feed_post_repo = Mock(spec=FeedPostRepository)
        mock_generated_bio_repo = Mock(spec=GeneratedBioRepository)
        mock_generated_feed_repo = Mock(spec=GeneratedFeedRepository)

        engine = SimulationEngine(
            run_repo=mock_run_repo,
            profile_repo=mock_profile_repo,
            feed_post_repo=mock_feed_post_repo,
            generated_bio_repo=mock_generated_bio_repo,
            generated_feed_repo=mock_generated_feed_repo,
        )

        run_id = "nonexistent_run"
        mock_run_repo.get_run.return_value = None

        # Act
        result = engine.get_run(run_id)

        # Assert
        assert result is None
        mock_run_repo.get_run.assert_called_once_with(run_id)

    def test_raises_value_error_for_empty_run_id(self):
        """Test that get_run raises ValueError for empty run_id."""
        # Arrange
        mock_run_repo = Mock(spec=RunRepository)
        mock_profile_repo = Mock(spec=ProfileRepository)
        mock_feed_post_repo = Mock(spec=FeedPostRepository)
        mock_generated_bio_repo = Mock(spec=GeneratedBioRepository)
        mock_generated_feed_repo = Mock(spec=GeneratedFeedRepository)

        engine = SimulationEngine(
            run_repo=mock_run_repo,
            profile_repo=mock_profile_repo,
            feed_post_repo=mock_feed_post_repo,
            generated_bio_repo=mock_generated_bio_repo,
            generated_feed_repo=mock_generated_feed_repo,
        )

        # Act & Assert
        with pytest.raises(ValueError, match="run_id cannot be empty"):
            engine.get_run("")

        # Verify repository was not called
        mock_run_repo.get_run.assert_not_called()

    def test_raises_value_error_for_whitespace_only_run_id(self):
        """Test that get_run raises ValueError for whitespace-only run_id."""
        # Arrange
        mock_run_repo = Mock(spec=RunRepository)
        mock_profile_repo = Mock(spec=ProfileRepository)
        mock_feed_post_repo = Mock(spec=FeedPostRepository)
        mock_generated_bio_repo = Mock(spec=GeneratedBioRepository)
        mock_generated_feed_repo = Mock(spec=GeneratedFeedRepository)

        engine = SimulationEngine(
            run_repo=mock_run_repo,
            profile_repo=mock_profile_repo,
            feed_post_repo=mock_feed_post_repo,
            generated_bio_repo=mock_generated_bio_repo,
            generated_feed_repo=mock_generated_feed_repo,
        )

        # Act & Assert
        with pytest.raises(ValueError, match="run_id cannot be empty"):
            engine.get_run("   ")

        # Verify repository was not called
        mock_run_repo.get_run.assert_not_called()

    def test_raises_value_error_for_none_run_id(self):
        """Test that get_run raises ValueError for None run_id."""
        # Arrange
        mock_run_repo = Mock(spec=RunRepository)
        mock_profile_repo = Mock(spec=ProfileRepository)
        mock_feed_post_repo = Mock(spec=FeedPostRepository)
        mock_generated_bio_repo = Mock(spec=GeneratedBioRepository)
        mock_generated_feed_repo = Mock(spec=GeneratedFeedRepository)

        engine = SimulationEngine(
            run_repo=mock_run_repo,
            profile_repo=mock_profile_repo,
            feed_post_repo=mock_feed_post_repo,
            generated_bio_repo=mock_generated_bio_repo,
            generated_feed_repo=mock_generated_feed_repo,
        )

        # Act & Assert
        with pytest.raises(ValueError, match="run_id cannot be empty"):
            engine.get_run(None)  # type: ignore

        # Verify repository was not called
        mock_run_repo.get_run.assert_not_called()

    def test_repository_exceptions_propagate(self):
        """Test that repository exceptions propagate without wrapping."""
        # Arrange
        mock_run_repo = Mock(spec=RunRepository)
        mock_profile_repo = Mock(spec=ProfileRepository)
        mock_feed_post_repo = Mock(spec=FeedPostRepository)
        mock_generated_bio_repo = Mock(spec=GeneratedBioRepository)
        mock_generated_feed_repo = Mock(spec=GeneratedFeedRepository)

        engine = SimulationEngine(
            run_repo=mock_run_repo,
            profile_repo=mock_profile_repo,
            feed_post_repo=mock_feed_post_repo,
            generated_bio_repo=mock_generated_bio_repo,
            generated_feed_repo=mock_generated_feed_repo,
        )

        run_id = "run_123"
        original_error = RunNotFoundError(run_id)
        mock_run_repo.get_run.side_effect = original_error

        # Act & Assert
        with pytest.raises(RunNotFoundError) as exc_info:
            engine.get_run(run_id)

        # Verify it's the same exception (not wrapped)
        assert exc_info.value is original_error
        mock_run_repo.get_run.assert_called_once_with(run_id)


class TestSimulationEngineListRuns:
    """Tests for SimulationEngine.list_runs method."""

    def test_returns_list_of_runs(self):
        """Test that list_runs returns a list of runs."""
        # Arrange
        mock_run_repo = Mock(spec=RunRepository)
        mock_profile_repo = Mock(spec=ProfileRepository)
        mock_feed_post_repo = Mock(spec=FeedPostRepository)
        mock_generated_bio_repo = Mock(spec=GeneratedBioRepository)
        mock_generated_feed_repo = Mock(spec=GeneratedFeedRepository)

        engine = SimulationEngine(
            run_repo=mock_run_repo,
            profile_repo=mock_profile_repo,
            feed_post_repo=mock_feed_post_repo,
            generated_bio_repo=mock_generated_bio_repo,
            generated_feed_repo=mock_generated_feed_repo,
        )

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
        mock_run_repo.list_runs.return_value = expected_runs

        # Act
        result = engine.list_runs()

        # Assert
        assert result == expected_runs
        assert len(result) == 2
        mock_run_repo.list_runs.assert_called_once()

    def test_returns_empty_list_when_no_runs_exist(self):
        """Test that list_runs returns empty list when no runs exist."""
        # Arrange
        mock_run_repo = Mock(spec=RunRepository)
        mock_profile_repo = Mock(spec=ProfileRepository)
        mock_feed_post_repo = Mock(spec=FeedPostRepository)
        mock_generated_bio_repo = Mock(spec=GeneratedBioRepository)
        mock_generated_feed_repo = Mock(spec=GeneratedFeedRepository)

        engine = SimulationEngine(
            run_repo=mock_run_repo,
            profile_repo=mock_profile_repo,
            feed_post_repo=mock_feed_post_repo,
            generated_bio_repo=mock_generated_bio_repo,
            generated_feed_repo=mock_generated_feed_repo,
        )

        mock_run_repo.list_runs.return_value = []

        # Act
        result = engine.list_runs()

        # Assert
        assert result == []
        assert len(result) == 0
        mock_run_repo.list_runs.assert_called_once()

    def test_repository_exceptions_propagate(self):
        """Test that repository exceptions propagate without wrapping."""
        # Arrange
        mock_run_repo = Mock(spec=RunRepository)
        mock_profile_repo = Mock(spec=ProfileRepository)
        mock_feed_post_repo = Mock(spec=FeedPostRepository)
        mock_generated_bio_repo = Mock(spec=GeneratedBioRepository)
        mock_generated_feed_repo = Mock(spec=GeneratedFeedRepository)

        engine = SimulationEngine(
            run_repo=mock_run_repo,
            profile_repo=mock_profile_repo,
            feed_post_repo=mock_feed_post_repo,
            generated_bio_repo=mock_generated_bio_repo,
            generated_feed_repo=mock_generated_feed_repo,
        )

        original_error = RuntimeError("Database connection failed")
        mock_run_repo.list_runs.side_effect = original_error

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            engine.list_runs()

        # Verify it's the same exception (not wrapped)
        assert exc_info.value is original_error
        mock_run_repo.list_runs.assert_called_once()
