from .content import Curriculum, AgentPrompt
import reflex as rx


def seed_data():
    """Seed initial curriculum and prompts."""
    curricula = [
        Curriculum(
            level=1,
            title="Beginner Basics",
            description="Focus on greetings and basic introduction.",
            base_content="Introduce yourself and ask for the user's name.",
        ),
        Curriculum(
            level=2,
            title="Daily Routines",
            description="Describe daily activities.",
            base_content="Talk about what you do in the morning.",
        ),
        Curriculum(
            level=3,
            title="Hobbies & Interests",
            description="Discuss things you like to do.",
            base_content="What are your favorite hobbies?",
        ),
        Curriculum(
            level=4,
            title="Travel & Culture",
            description="Discuss travel experiences.",
            base_content="Talk about a place you've visited.",
        ),
    ]

    with rx.session() as session:
        # Clear existing
        # session.exec(Curriculum.delete())
        for c in curricula:
            session.add(c)
        session.commit()


if __name__ == "__main__":
    seed_data()
