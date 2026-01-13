# English Tutoring Agent - Documentation

## Overview
This solution is a multi-agent English tutoring platform built with **Reflex**, **LangChain**, and **Gemini Audio API**. It uses **PGLite** (via `py-pglite`) as an embedded PostgreSQL database for low-latency persistence.

## Project Structure
- `agents/`: logic for different tutoring stages.
- `models/`: Database schema for Users, Sessions, Messages, Evaluations, and Curriculum.
- `prompts/`: Versioned system prompts for the AI agents.
- `state/`: Global application state management (Auth, Chat).
- `views/`: UI components for Chat, Dashboard, Admin, and Landing pages.

## Key Features
1. **Multi-Agent Orchestration**: Switches between Onboarding, Evaluation, Tutoring, and Planning based on session state.
2. **Audio-Ready**: Integrated with Gemini Audio API for STT and multimodal understanding.
3. **Advanced Analytics**: Plotly-based charts to track learning progress over time.
4. **Embedded DB**: High-performance PostgreSQL features in a local environment.

## Getting Started
1. Install Python 3.12: `uv python install 3.12`
2. Install dependencies: `uv sync`
3. Run type checks: `uv run ty check`
4. Run database migrations: `reflex db init` (automatic on reflex run)
5. Start the dev server: `reflex run`
