# Medicinal Plant Identification AI Chat Assistant

## Purpose
Document the AI chat assistant component integrated into the project: backend implementation, frontend integration, data flow, and how to run it.

## Architecture
- `assis.py`: chat assistant class with plant context, conversation memory, and model calls (groq / langchain)
- `webapp/app.py`: Flask endpoints
  - `/predict` - plant prediction from image
  - `/chat/init` - initialize assistant with predicted plant
  - `/chat/message` - user Q/A messaging
  - `/chat` - chat UI page
- `webapp/templates/chat.html`: user chat interface
- `webapp/static/js/chat.js`: chat communication logic and history display
- `config.py`: `PLANT_CLASSES` metadata used by predictor and assistant

## Feature behavior
1. User uploads plant image
2. `src/predictor.py` returns the most likely plant name + confidence
3. UI shows plant summary and opens `chat` page via button
4. Chat assistant context is initialized with `set_plant()` in `MedicinalPlantChatAssistant`
5. User questions go through `/chat/message`, and responses are returned with structured suggestions

## Key implementation details
- prompt engineering ensures context-specific answers and reduces hallucination
- fallback deterministic answers used for safety when model declines
- persistent per-session conversation history is maintained until plant is changed

## Setup
1. Create `.env` with `GROQ_API_KEY` and `GROQ_MODEL` values.
2. Install dependencies from `requirements.txt`.
3. Run Flask app from `webapp/app.py`.

## Quick test
- Launch application
- Upload a test image from `dataset/`
- Predict plant and use chat for following questions:
  - "What are the main uses of <plant>?"
  - "Any safety concerns?"

## Troubleshooting
- If chat returns refusal patterns, verify `assis.py` fallback path.
- If model key fails, confirm `GROQ_API_KEY` and environment variables.
