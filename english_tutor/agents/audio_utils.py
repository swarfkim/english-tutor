import google.generativeai as genai
import os
from pathlib import Path

# Configure Gemini API Key
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print(
        "WARNING: GEMINI_API_KEY not found in environment variables. Audio features may fail."
    )


def upload_audio_to_gemini(file_path: str):
    """Uploads an audio file to Gemini File API."""
    audio_file = genai.upload_file(path=file_path)
    return audio_file


def generate_response_with_audio(audio_file, prompt: str):
    """Generates a response from Gemini given an audio file and a prompt."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([audio_file, prompt])
    return response.text


def text_to_speech_dummy(text: str, output_path: str):
    """
    Dummy TTS function. In a real scenario, use Google Cloud TTS or
    Gemini's speech generation if available in the SDK.
    """
    # For now, we just log. I'll implement a real TTS later.
    print(f"Generating speech for: {text[:50]}...")
    pass
