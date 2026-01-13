import dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage as AIChatMessage,
)


dotenv.load_dotenv()


class BaseAgent:
    def __init__(self, name: str, prompt_file: str):
        self.name = name
        with open(prompt_file, "r") as f:
            self.system_prompt = f.read()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            # Fallback or let langchain handle it if GOOGLE_API_KEY is set
            pass
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview", google_api_key=api_key
        )

    def get_response(self, history: list[dict[str, str]], **kwargs) -> tuple[str, dict]:
        """Get response from LLM and return (text, metadata) tuple."""
        messages = [SystemMessage(content=self.system_prompt.format(**kwargs))]
        for msg in history:
            if msg["sender"] == "user":
                messages.append(HumanMessage(content=msg["content_text"]))
            else:
                messages.append(AIChatMessage(content=msg["content_text"]))

        response = self.llm.invoke(messages)
        content = response.content

        # Extract usage metadata
        metadata = {
            "model_name": getattr(response, "model", "gemini-3-flash-preview"),
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "cached_prompt_tokens": 0,
            "total_tokens": 0,
        }

        # Try to extract token usage if available
        if hasattr(response, "usage_metadata"):
            usage = response.usage_metadata
            metadata["prompt_tokens"] = getattr(usage, "prompt_token_count", 0)
            metadata["completion_tokens"] = getattr(usage, "candidates_token_count", 0)
            metadata["cached_prompt_tokens"] = getattr(
                usage, "cached_content_token_count", 0
            )
            metadata["total_tokens"] = getattr(usage, "total_token_count", 0)
        elif hasattr(response, "response_metadata"):
            # Alternative metadata location
            resp_meta = response.response_metadata
            if "token_usage" in resp_meta:
                usage = resp_meta["token_usage"]
                metadata["prompt_tokens"] = usage.get("prompt_tokens", 0)
                metadata["completion_tokens"] = usage.get("completion_tokens", 0)
                metadata["total_tokens"] = usage.get("total_tokens", 0)

        def extract_text(part):
            if isinstance(part, str):
                return part
            elif isinstance(part, dict):
                return part.get("text", "")
            elif hasattr(part, "text"):
                return part.text
            else:
                return str(part)

        if isinstance(content, str):
            return content, metadata
        elif isinstance(content, list):
            # Handle list of content parts (e.g. from Gemini)
            text_parts = [extract_text(part) for part in content]
            return " ".join(text_parts), metadata
        elif isinstance(content, dict):
            return content.get("text", ""), metadata
        else:
            return str(content), metadata


class CounselorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Counselor", "english_tutor/prompts/counselor.txt")


class EvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Evaluator", "english_tutor/prompts/evaluator.txt")


class TutorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Tutor", "english_tutor/prompts/tutor.txt")


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Planner", "english_tutor/prompts/planner.txt")
