import reflex as rx
from sqlmodel import Field
from datetime import datetime
from datetime import timezone


class Message(rx.Model, table=True):
    """Individual chat messages."""

    session_id: int
    sender: str  # user, agent
    content_text: str
    content_audio_path: str = ""
    feedback: int = 0  # 1 for thumb-up, -1 for thumb-down
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Evaluation(rx.Model, table=True):
    """Quantitative evaluation results."""

    user_id: int
    session_id: int

    # Core language skills
    pronunciation_score: float = 0.0  # 발음
    grammar_score: float = 0.0  # 문법
    vocabulary_score: float = 0.0  # 어휘력

    # Advanced evaluation criteria
    fluency_score: float = 0.0  # 유창성
    expression_score: float = 0.0  # 표현력
    confidence_score: float = 0.0  # 자신감

    # Overall assessment
    overall_score: float = 0.0
    feedback_summary: str = ""
    detailed_correction: str = ""  # AI's correction/suggestions
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
