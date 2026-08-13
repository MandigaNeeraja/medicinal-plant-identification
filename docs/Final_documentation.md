# Final Documentation: Medicinal Plant Identification by Leaf Images

## Project Overview
This project identifies medicinal plants from leaf images using deep learning and provides expert guidance through an AI chat assistant. It combines computer vision, model inference, and plant domain knowledge to support educational and practical use cases.

## Goals
- Accurately classify medicinal plants from leaf pictures
- Deliver plant details (common name, scientific name, uses, safety)
- Provide interactive AI chat assistant with context-aware Q&A
- Maintain user-friendly web interface for upload, prediction and chat

## System Architecture
1. User uploads leaf image through the web app (`webapp/templates/index.html`).
2. Image preprocessing and machine learning prediction in `src/predictor.py`.
3. Predicted plant class and confidence shown in dashboard.
4. User initiates chat with `MedicinalPlantChatAssistant` (`assis.py`) and plant context set via `set_plant()`.
5. Questions are sent to backend endpoints (`webapp/app.py`): `/chat/init`, `/chat/message`.
6. LLM answers via `groq` model (LangChain wrapper), with fallback logic to deterministic plant info if needed.

## Key Components
### `src/predictor.py`
- Loads model from `models/best_model.h5`
- Processes images to target shape (128x128)
- Predicts plant class probabilities
- Returns top name and confidence

### `config.py`
- `PLANT_CLASSES`: dictionary of plant metadata with:
  - scientific_name
  - common_names
  - overview
  - medicinal_uses
  - preparation
  - dosage
  - safety
  - best_time
  - did_you_know

### `webapp/app.py`
- Flask app around model/predictor and assistant:
  - `/` index page
  - `/predict` handles image upload
  - `/chat` chat UI route
  - `/chat/init` initialize plant context
  - `/chat/message` answer questions

### `assis.py`
- `MedicinalPlantChatAssistant` class
- Plant context setup and conversation history
- `answer_question` with:
  - deterministic fallback for safety and key queries
  - groq LLM invocation by default
  - refusal detection and fallback

### Frontend
- `webapp/templates/index.html`: image upload and prediction card
- `webapp/static/js/script_new.js`: upload and AJAX prediction
- `webapp/templates/chat.html`: chat interface
- `webapp/static/js/chat.js`: chat request & response handling
- `webapp/static/css/style.css`: layout and widget style

## Features
- Leaf-based medicinal plant identification
- Confidence-based prediction with easy-to-read results
- Library of plant health and medicinal properties
- AI-driven Q&A with plant-specific context
- Structured suggestions and follow-up prompts
- Separation of prediction flow and chat flow

## Technology Stack
- Python 3.x
- Flask
- TensorFlow/Keras (model loading and inference)
- OpenCV (image pre-processing)
- LangChain + Groq for chat model integration
- HTML/CSS/JavaScript for UI
- Optional: local virtual environment (`env/`)

## Instructions to Run
1. Activate virtual env: `env\Scripts\Activate.ps1` (Windows)
2. Install dependencies: `pip install -r requirements.txt`
3. Add `.env` with:
   - `GROQ_API_KEY=<your_key>`
   - `GROQ_MODEL=llama-3.1-8b-instant`
4. Start app: `python webapp/app.py`
5. Open `http://127.0.0.1:5000`
6. Upload a leaf image and observe predictions. Use chat page to ask questions.

## Testing
- Check model inference with sample images in `dataset/`
- Test chat initialization with predicted plant
- Submit questions and verify response text + fallback behavior
- Ensure UI elements work (button navigation, loading indicators)

## Known limitations
- Model depends on dataset coverage; misclassifications possible
- Groq API usage may incur latency or cost
- No authentication for multi-user isolation (single session state)

## Future Enhancements
- Add user login and history preservation
- Collect user feedback on predictions
- Expand dataset and classes beyond current plant set
- Add image augmentation and live camera upload
- More rigorous model validation and cross-validation

## Conclusion
Final product combines machine learning and AI chat for an end-to-end plant identification assistant. Clear code paths and docs make it maintainable and extensible for research and real-world utility.
