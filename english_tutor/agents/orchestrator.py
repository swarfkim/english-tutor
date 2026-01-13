from .base import CounselorAgent, EvaluatorAgent, TutorAgent, PlannerAgent
from ..models.user import Session, User
from ..models.evaluation import Message
import reflex as rx


class Orchestrator:
    def __init__(self):
        self.agents = {
            "onboarding": CounselorAgent(),
            "evaluation": EvaluatorAgent(),
            "tutoring": TutorAgent(),
            "planning": PlannerAgent(),
        }

    def get_agent_for_session(self, session: Session):
        if session.session_type == "onboarding":
            return self.agents["onboarding"]
        elif session.session_type == "evaluation":
            return self.agents["evaluation"]
        elif session.session_type == "tutoring":
            return self.agents["tutoring"]
        elif session.session_type == "planning":
            return self.agents["planning"]
        return self.agents["onboarding"]

    def process_message(self, session_id: int, user_id: int, text: str):
        # This will be called from the Reflex state
        pass
