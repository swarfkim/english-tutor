import reflex as rx
from english_tutor.models.content import Curriculum
from sqlmodel import select


def seed_curriculum():
    curricula = [
        {
            "level": 1,
            "title": "Level 1: Novice Basics",
            "description": "Fundamental greetings and personal identification.",
            "learning_goals": "1. Simple greetings (Hello, Good morning)\n2. Introducing oneself (My name is...)\n3. Basic pronouns (I, You, He, She)",
            "common_pitfalls": "1. Confusing 'I am' with 'I'\n2. Mixing up 'He' and 'She'",
            "base_content": "Introduction to basic greetings and self-introduction. Vocabulary: Hello, Goodbye, Name, Student, Teacher. Grammar: To be verb (am/are/is).",
        },
        {
            "level": 2,
            "title": "Level 2: Daily Survival",
            "description": "Essential communication for daily life.",
            "learning_goals": "1. Telling time and dates\n2. Basic numbers (1-100)\n3. Common daily verbs (eat, sleep, work)",
            "common_pitfalls": "1. Incorrect use of 'do' in questions\n2. Pluralization errors",
            "base_content": "Daily routines and basic surroundings. Vocabulary: Time, House, Food, Drink. Grammar: Present Simple tense.",
        },
        {
            "level": 3,
            "title": "Level 3: Social Interactions",
            "description": "Simple conversations on familiar topics.",
            "learning_goals": "1. Expressing likes and dislikes\n2. Talking about hobbies\n3. Basic conjunctions (and, but, because)",
            "common_pitfalls": "1. Overusing 'very'\n2. Misplacing adverbs of frequency",
            "base_content": "Interests and socializing. Vocabulary: Hobbies, Sports, Music, Movies. Grammar: Adverbs of frequency, basic adjectives.",
        },
        {
            "level": 4,
            "title": "Level 4: Workplace Communications",
            "description": "Uncomplicated professional and social tasks.",
            "learning_goals": "1. Describing past events\n2. Future plans (going to)\n3. Basic workplace vocabulary",
            "common_pitfalls": "1. Irregular past tense verbs\n2. Confusing 'will' and 'going to'",
            "base_content": "Work and future aspirations. Vocabulary: Office, Meeting, Job, Company. Grammar: Past Simple, Future with 'going to'.",
        },
        {
            "level": 5,
            "title": "Level 5: Intermediate Fluency",
            "description": "Conversing with ease on most topics.",
            "learning_goals": "1. Comparisons (better than, the best)\n2. Present Perfect (experience)\n3. Relative clauses (who, which, that)",
            "common_pitfalls": "1. Since vs For\n2. Choosing the wrong relative pronoun",
            "base_content": "Comparative experiences and descriptions. Vocabulary: Environment, Travel, News. Grammar: Present Perfect, Comparatives/Superlatives.",
        },
        {
            "level": 6,
            "title": "Level 6: Expressing Opinions",
            "description": "Handling complex situations and clear expression.",
            "learning_goals": "1. Modals of deduction (must be, might be)\n2. Passive voice basics\n3. Arguing for/against a point",
            "common_pitfalls": "1. Passive vs Active confusion\n2. Over-formalizing casual speech",
            "base_content": "Debates and complex scenarios. Vocabulary: Economy, Politics, Technology. Grammar: Passive Voice, Advanced Modals.",
        },
        {
            "level": 7,
            "title": "Level 7: Professional Mastery",
            "description": "Full participation in social and professional contexts.",
            "learning_goals": "1. Mixed conditionals\n2. Advanced academic vocabulary\n3. Nuanced idiomatic expressions",
            "common_pitfalls": "1. Conditional structure errors\n2. Using idioms incorrectly",
            "base_content": "Professional discourse and abstract concepts. Vocabulary: Philosophy, Science, Management. Grammar: Mixed Conditionals, Gerunds vs Infinitives.",
        },
        {
            "level": 8,
            "title": "Level 8: Superior Expression",
            "description": "Extensive discussion with precision and nuance.",
            "learning_goals": "1. Inversion for emphasis\n2. Subtle stylistic nuances\n3. Native-like conversational flow",
            "common_pitfalls": "1. Misinterpreting subtle cultural nuances\n2. Over-relying on formal structures",
            "base_content": "Extensive complex discussions. Vocabulary: Linguistics, Deep Tech, Art Theory. Grammar: Inversions, Stylistic focus.",
        },
    ]

    with rx.session() as session:
        for cur_data in curricula:
            existing = session.exec(
                select(Curriculum).where(Curriculum.level == cur_data["level"])
            ).first()
            if existing:
                for k, v in cur_data.items():
                    setattr(existing, k, v)
                session.add(existing)
            else:
                new_cur = Curriculum(**cur_data)
                session.add(new_cur)
        session.commit()
    print("Seed complete!")


if __name__ == "__main__":
    seed_curriculum()
