import reflex as rx
from sqlmodel import Field
from datetime import datetime
from datetime import timezone


class TokenUsage(rx.Model, table=True):
    """Track detailed token usage per message."""

    # References
    message_id: int | None = None  # Optional reference to Message table
    session_id: int
    user_id: int

    # Model information
    model_name: str  # e.g., "gemini-1.5-pro"

    # Message content (for analysis)
    input_message: str
    output_message: str

    # Token breakdown
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cached_prompt_tokens: int = 0
    total_tokens: int = 0

    # Performance
    response_time_ms: int = 0  # Response time in milliseconds

    # Cost estimation (optional)
    estimated_cost: float = 0.0

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
