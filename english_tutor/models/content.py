import reflex as rx
from sqlmodel import Field


class Curriculum(rx.Model, table=True):
    """Curriculum content for each level."""

    level: int  # 1-8
    title: str
    description: str
    base_content: str  # LLM uses this to generate session content
    learning_goals: str = ""  # Specific points to be mastered
    common_pitfalls: str = ""  # Common mistakes for this level/chapter


class AgentPrompt(rx.Model, table=True):
    """Versioned agent prompts."""

    agent_name: str  # evaluation, tutoring, learning_plan, counseling
    prompt_text: str
    version: int = 1
    is_active: bool = True
