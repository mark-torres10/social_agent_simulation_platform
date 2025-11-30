from pydantic import BaseModel

class GenerationMetadata(BaseModel):
    """Metadata about AI generation process."""
    model_used: str | None = None
    generation_metadata: dict[str, Any] | None = None
    created_at: str
