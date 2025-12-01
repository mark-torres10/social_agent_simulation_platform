"""Shared validation helpers for Pydantic models."""


def validate_non_empty_string(v: str, field_name: str) -> str:
    """Validate that a string field is non-empty after stripping.

    Args:
        v: The string value to validate
        field_name: The name of the field being validated (for error messages)

    Returns:
        The stripped string value

    Raises:
        ValueError: If the string is empty or contains only whitespace
    """
    if not v or not v.strip():
        raise ValueError(f"{field_name} cannot be empty")
    return v.strip()
