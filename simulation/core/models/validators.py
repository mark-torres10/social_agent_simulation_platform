"""Shared validation helpers for Pydantic models."""


def validate_non_empty_string(v: str, field_name: str) -> str:
    """Validate that a string field is non-empty after stripping.

    This function is intended to be called from Pydantic field_validators
    after type coercion has occurred, so v should already be a str.
    However, we include defensive None checking for robustness.

    Args:
        v: The string value to validate (expected to be str after Pydantic coercion)
        field_name: The name of the field being validated (for error messages)

    Returns:
        The stripped string value

    Raises:
        ValueError: If the value is None, not a string, or empty after stripping
    """
    if v is None:
        raise ValueError(f"{field_name} cannot be None")
    if not isinstance(v, str):
        raise ValueError(f"{field_name} must be a string")
    v = v.strip()
    if not v:
        raise ValueError(f"{field_name} cannot be empty")
    return v
