"""Domain-specific exceptions for the simulation engine."""

class SimulationError(Exception):
    """
    Base exception class for simulation-related errors.

    Optionally includes context information such as run ID and turn number.

    Usage:
        raise SimulationError("Something went wrong", run_id="abc123", turn_number=5)
    """

    def __init__(self, message: str, run_id: str | None = None, turn_number: int | None = None):
        """
        Initialize SimulationError.

        Args:
            message: The error message to display.
            run_id: Optional. The ID of the run where the error occurred.
            turn_number: Optional. The turn number where the error occurred.
        """
        self.run_id = run_id
        self.turn_number = turn_number
        super().__init__(message)


class InsufficientAgentsError(SimulationError):
    """
    Raised when there are not enough agents to perform the requested action.

    Usage example:
        raise InsufficientAgentsError(requested=10, available=3, run_id="run-x")
    """

    def __init__(
        self, 
        requested: int, 
        available: int, 
        run_id: str | None = None, 
        turn_number: int | None = None
    ):
        """
        Initialize InsufficientAgentsError.

        Args:
            requested: Number of agents requested.
            available: Number of agents actually available.
            run_id: Optional. The ID of the run.
            turn_number: Optional. The turn number.
        """
        self.requested = requested
        self.available = available
        message = (
            f"Not enough agents: requested {requested}, but only {available} available."
        )
        super().__init__(message, run_id=run_id, turn_number=turn_number)
