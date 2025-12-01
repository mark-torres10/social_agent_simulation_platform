"""Domain-specific exceptions for database operations."""


class RunNotFoundError(Exception):
    """Raised when a run with the specified ID cannot be found."""

    def __init__(self, run_id: str):
        """Initialize RunNotFoundError.

        Args:
            run_id: The run ID that was not found
        """
        self.run_id = run_id
        super().__init__(f"Run '{run_id}' not found")


class InvalidTransitionError(Exception):
    """Raised when an invalid status transition is attempted."""

    def __init__(
        self,
        run_id: str,
        current_status: str,
        target_status: str,
        valid_transitions: list[str] | None = None,
    ):
        """Initialize InvalidTransitionError.

        Args:
            run_id: The run ID for which the transition was attempted
            current_status: The current status of the run
            target_status: The target status that was attempted
            valid_transitions: List of valid transition targets from current_status, or None if terminal state
        """
        self.run_id = run_id
        self.current_status = current_status
        self.target_status = target_status
        self.valid_transitions = valid_transitions

        if valid_transitions:
            transitions_str = ", ".join(valid_transitions)
        else:
            transitions_str = "none (terminal state)"

        message = (
            f"Invalid status transition for run '{run_id}': "
            f"{current_status} -> {target_status}. "
            f"Valid transitions from {current_status} are: {transitions_str}"
        )
        super().__init__(message)


class RunCreationError(Exception):
    """Raised when a run cannot be created."""

    def __init__(self, run_id: str, reason: str | None = None):
        """Initialize RunCreationError.

        Args:
            run_id: The run ID that failed to be created
            reason: Optional reason for the failure
        """
        self.run_id = run_id
        self.reason = reason

        if reason:
            message = f"Failed to create run '{run_id}': {reason}"
        else:
            message = f"Failed to create run '{run_id}'"

        super().__init__(message)


class RunStatusUpdateError(Exception):
    """Raised when a run status cannot be updated."""

    def __init__(self, run_id: str, reason: str | None = None):
        """Initialize RunStatusUpdateError.

        Args:
            run_id: The run ID that failed to be updated
            reason: Optional reason for the failure
        """
        self.run_id = run_id
        self.reason = reason

        if reason:
            message = f"Failed to update run status for '{run_id}': {reason}"
        else:
            message = f"Failed to update run status for '{run_id}'"

        super().__init__(message)


class DuplicateTurnMetadataError(Exception):
    """Raised when turn metadata already exists."""

    def __init__(self, run_id: str, turn_number: int):
        """Initialize DuplicateTurnMetadataError.

        Args:
            run_id: The run ID that has duplicate turn metadata
            turn_number: The turn number that has duplicate metadata
        """
        self.run_id = run_id
        self.turn_number = turn_number

        message = f"Turn metadata already exists for run '{run_id}', turn {turn_number}"
        super().__init__(message)
