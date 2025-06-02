"""Helper functions."""

from datetime import datetime, timezone

timestamp_format = "%Y-%m-%d-%H:%M:%S"


def get_current_timestamp_str():
    """Get the current timestamp as a string."""
    return datetime.now(timezone.utc).strftime(timestamp_format)
