from typing import Optional

from ai.agents import SocialMediaAgent
from db.models import Run, RunConfig, RunStatus, TurnResult
from db.repositories.run_repository import RunRepository
from db.repositories.profile_repository import ProfileRepository
from db.repositories.feed_post_repository import FeedPostRepository
from db.repositories.generated_bio_repository import GeneratedBioRepository
from db.repositories.generated_feed_repository import GeneratedFeedRepository

class SimulationEngine:
    def __init__(self, run_repo: RunRepository, profile_repo: ProfileRepository, feed_post_repo: FeedPostRepository, generated_bio_repo: GeneratedBioRepository, generated_feed_repo: GeneratedFeedRepository):
        self.run_repo = run_repo
        self.profile_repo = profile_repo
        self.feed_post_repo = feed_post_repo
        self.generated_bio_repo = generated_bio_repo
        self.generated_feed_repo = generated_feed_repo

    ## Public API ##

    def execute_run(self, run_config: RunConfig) -> Run:
        pass

    def get_run(self, run_id: str) -> Optional[Run]:
        pass

    def list_runs(self) -> list[Run]:
        pass

    def get_turn_data(self, run_id :str, turn_number: int) -> Optional[TurnResult]:
        pass

    ## Private Methods ##

    def _simulate_turn(self, run_id: str, turn_number: int) -> TurnResult:
        pass

    def _create_agents_for_run(self, run_config: RunConfig) -> list[SocialMediaAgent]:
        pass

    def _update_run_status_safely(self, run_id: str, status: RunStatus) -> None:
        pass
