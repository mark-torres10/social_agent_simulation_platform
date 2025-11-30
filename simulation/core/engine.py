from typing import Optional

from db.repositories.feed_post_repository import FeedPostRepository
from db.repositories.generated_bio_repository import GeneratedBioRepository
from db.repositories.generated_feed_repository import GeneratedFeedRepository
from db.repositories.profile_repository import ProfileRepository
from db.repositories.run_repository import RunRepository

from simulation.core.models.agents import SocialMediaAgent
from simulation.core.models.runs import Run, RunConfig, RunStatus

from .models import TurnResult


class SimulationEngine:
    def __init__(
        self,
        run_repo: RunRepository,
        profile_repo: ProfileRepository,
        feed_post_repo: FeedPostRepository,
        generated_bio_repo: GeneratedBioRepository,
        generated_feed_repo: GeneratedFeedRepository,
    ):
        self.run_repo = run_repo
        self.profile_repo = profile_repo
        self.feed_post_repo = feed_post_repo
        self.generated_bio_repo = generated_bio_repo
        self.generated_feed_repo = generated_feed_repo

    ## Public API ##

    def execute_run(self, run_config: RunConfig) -> Run:
        """Execute a simulation run.

        Args:
            run_config: The configuration for the run.

        Returns:
            The run that was executed.
        """
        raise NotImplementedError  # Stub for PR 1

    def get_run(self, run_id: str) -> Optional[Run]:
        """Get a run by its ID.

        Args:
            run_id: The ID of the run to get.

        Returns:
            The run if found, None otherwise.
        """
        if not run_id or not run_id.strip():
            raise ValueError("run_id cannot be empty")
        return self.run_repo.get_run(run_id)

    def list_runs(self) -> list[Run]:
        """List all runs.

        Returns:
            A list of all runs.
        """
        return self.run_repo.list_runs()

    def get_turn_metadata(self, run_id: str, turn_number: int) -> Optional[TurnMetadata]:
        """Get turn metadata for a specific run and turn number.

        Args:
            run_id: The ID of the run.
            turn_number: The turn number (0-indexed).

        Returns:
            The turn metadata if found, None otherwise.
        """
        if not run_id or not run_id.strip():
            raise ValueError("run_id cannot be empty")
        if turn_number < 0:
            raise ValueError("turn_number cannot be negative")
        return self.run_repo.get_turn_metadata(run_id, turn_number)

    def get_turn_data(self, run_id: str, turn_number: int) -> Optional[TurnData]:
        """Returns full turn data with feeds and posts

        Args:
            run_id: The ID of the run.
            turn_number: The turn number (0-indexed).

        Returns:
            Complete turn data including all feeds and hydrated posts.
            Used in the UI for detailed views or full turn history.
        """
        if not run_id or not run_id.strip():
            raise ValueError("run_id cannot be empty")
        if turn_number < 0:
            raise ValueError("turn_number cannot be negative")
        

    ## Private Methods ##

    def _simulate_turn(
        self, run_id: str, turn_number: int, agents: list[SocialMediaAgent]
    ) -> TurnResult:
        """Simulate a single turn of the simulation.

        Args:
            run_id: The ID of the run.
            turn_number: The turn number (0-indexed).
            agents: The list of agents participating in the turn.

        Returns:
            The result of the turn execution.
        """
        raise NotImplementedError  # Stub for PR 1

    def _create_agents_for_run(self, config: RunConfig) -> list[SocialMediaAgent]:
        """Create agents for a simulation run.

        Args:
            config: The run configuration.

        Returns:
            A list of agents for the run.
        """
        raise NotImplementedError  # Stub for PR 1

    def _update_run_status_safely(self, run_id: str, status: RunStatus) -> None:
        """Update run status without masking original exceptions.

        Args:
            run_id: The ID of the run.
            status: The new status.
        """
        raise NotImplementedError  # Stub for PR 1
