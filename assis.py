from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from config import PLANT_CLASSES
import os

# Load environment variables from .env file
load_dotenv()

# Build model client using env var API key (groq expects it setup already)
# Make sure GROQ_API_KEY is set in the .env file.
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
MODEL_PROVIDER = "groq"


def _format_plant_text(plant_name):
    plant = PLANT_CLASSES.get(plant_name)
    if not plant:
        return "No data available for this plant."

    lines = [f"Plant: {plant_name}"]
    lines.append(f"Scientific Name: {plant.get('scientific_name', 'Unknown')}")
    lines.append(f"Common Names: {', '.join(plant.get('common_names', []))}")
    lines.append(f"Overview: {plant.get('overview', 'Not available')}")
    lines.append("Medicinal Uses:")
    for use in plant.get('medicinal_uses', []):
        lines.append(f"  - {use}")

    prep = plant.get('preparation', {})
    if prep:
        lines.append("Preparation methods:")
        for k, v in prep.items():
            lines.append(f"  - {k.capitalize()}: {v}")

    lines.append(f"Dosage: {plant.get('dosage', 'Not available')}")
    lines.append(f"Safety: {plant.get('safety', 'Not available')}")
    lines.append(f"Best time: {plant.get('best_time', 'Not available')}")
    lines.append(f"Did you know: {plant.get('did_you_know', 'N/A')}")
    return "\n".join(lines)


class MedicinalPlantChatAssistant:
    """AI chat assistant for medicinal plants, with plant-specific context and memory."""

    def __init__(self, model_name=MODEL_NAME, model_provider=MODEL_PROVIDER):
        self.client = init_chat_model(model_name, model_provider=model_provider)
        # conversation history: list of tuples (role, text)
        self.conversation_history = []
        self.current_plant = None

    def set_plant(self, plant_name: str):
        """Set active plant context, reset conversation history, and return initial summary."""
        if plant_name not in PLANT_CLASSES:
            raise ValueError(f"Plant '{plant_name}' not found in plant database")

        self.current_plant = plant_name
        self.conversation_history.clear()

        plant_text = _format_plant_text(plant_name)

        system_message = (
            "You are an AI medicinal plant expert. "
            "The identified plant is %{plant_name}% and the conversation should remain focused on this plant unless otherwise requested.".replace("%{plant_name}%", plant_name)
        )

        self.conversation_history.append(("system", system_message))
        self.conversation_history.append(("system", plant_text))

        plant_data = PLANT_CLASSES.get(plant_name, {})
        summary = {
            'plant': plant_name,
            'scientific_name': plant_data.get('scientific_name', ''),
            'image': plant_data.get('image', ''),
            'overview': plant_data.get('overview', ''),
            'medicinal_uses': plant_data.get('medicinal_uses', []),
            'dosage': plant_data.get('dosage', ''),
            'safety': plant_data.get('safety', ''),
            'best_time': plant_data.get('best_time', ''),
        }

        return {
            'plant': plant_name,
            'summary': summary,
            'message': f"Selected plant '{plant_name}' with context loaded.",
            'suggestions': self._generate_suggestions(plant_name)
        }

    def _get_prompt_with_history(self, user_question: str):
        if not self.current_plant:
            raise ValueError("No plant selected. Call set_plant(plant_name) first.")

        lines = ["System: You are an AI assistant specialized in medicinal plant knowledge."]
        lines.append(f"System: Active plant context: {self.current_plant}")

        for role, content in self.conversation_history:
            if role in ("user", "assistant"):
                prefix = "User" if role == "user" else "Assistant"
                lines.append(f"{prefix}: {content}")

        lines.append(f"User: {user_question}")

        return "\n".join(lines)

    def _is_refusal_response(self, text: str) -> bool:
        low = text.lower()
        terms = [
            'i cannot', 'i can’t', 'i cannot provide', 'as an ai', 'unable to provide',
            'i don\'t have', 'i do not have', 'no information available', 'not authorized'
        ]
        return any(term in low for term in terms)

    def _fallback_answer(self, question: str) -> str:
        plant = PLANT_CLASSES.get(self.current_plant, {})
        uses = plant.get('medicinal_uses', [])
        overview = plant.get('overview', 'No overview available.')
        safety = plant.get('safety', 'No safety information available.')
        preparation = plant.get('preparation', {})

        lower_question = question.lower()

        if 'side effect' in lower_question or 'precaution' in lower_question or 'safety' in lower_question:
            factors = [
                'May interact with blood thinners; consult a doctor if on medication.'
            ]
            if plant.get('safety'):
                factors = [plant.get('safety')]
            return (
                f"🔒 Known Side Effects & Precautions for {self.current_plant}:\n" +
                "\n".join(f"- {f}" for f in factors)
            )

        if 'main medicinal benefits' in lower_question or 'benefits' in lower_question or 'key uses' in lower_question:
            if uses:
                return (
                    f"💡 Main Medicinal Benefits of {self.current_plant}:\n" +
                    "\n".join(f"- {u}" for u in uses)
                )
            return "💡 No structured benefit data is available for this plant."

        # generic fallback
        answer_parts = []
        answer_parts.append(f"🌿 *{self.current_plant}* ({plant.get('scientific_name', 'Unknown')}) key info:")
        answer_parts.append(f"**Overview:** {overview}")

        if uses:
            answer_parts.append("**Medicinal uses:**")
            for u in uses:
                answer_parts.append(f"- {u}")

        if preparation:
            answer_parts.append("**Preparation methods:**")
            for method, details in preparation.items():
                answer_parts.append(f"- **{method.capitalize()}**: {details}")

        answer_parts.append(f"**Safety:** {safety}")

        return "\n".join(answer_parts)

    def _generate_suggestions(self, plant_name: str):
        return [
            f"What are the main medicinal benefits of {plant_name}?",
            f"How should I prepare {plant_name} safely?",
            f"Are there any known side effects or precautions for {plant_name}?"
        ]

    def answer_question(self, question: str):
        """Answer user question by using plant context and prior conversation history."""
        if not self.current_plant:
            raise RuntimeError("Plant context is not initialized; call set_plant(plant_name) first.")

        # if question is clearly mapped, provide deterministic expert response first
        if any(term in question.lower() for term in ['side effect', 'precaution', 'safety', 'main medicinal benefits', 'benefits', 'key uses']):
            deterministic = self._fallback_answer(question)
            self.conversation_history.append(("user", question))
            self.conversation_history.append(("assistant", deterministic))
            return {
                'answer': deterministic,
                'suggestions': self._generate_suggestions(self.current_plant),
                'plant': self.current_plant,
                'source': 'fallback'
            }

        plant_info_snippet = _format_plant_text(self.current_plant)
        prompt = (
            "You are an AI-powered medicinal plant assistant that answers questions only for the selected plant. "
            "Use only the data in the plant context, plus general medicinal plant knowledge. "
            "Do not refuse, do not say you are unable; always answer with relevant domain information from the plant. "
            "Use headings and bullet points in the answer where useful, and a friendly tone with a few emojis. "
            "If applicable, include a short summary and three easy follow-up suggestions."
        )

        # Persist the question in history
        self.conversation_history.append(("user", question))

        query = (
            f"{prompt}\n\n" +
            f"Selected plant: {self.current_plant}\n\n" +
            f"Plant context:\n{plant_info_snippet}\n\n" +
            f"Conversation so far (latest user question last):\n"
        )

        # include last 4 turns for context
        recent = self.conversation_history[-8:]
        for r, c in recent:
            role_label = "User" if r == "user" else "Assistant" if r == "assistant" else "System"
            query += f"{role_label}: {c}\n"

        query += f"User: {question}\n"

        # call model
        response = self.client.invoke(query)
        text = response.content.strip() if hasattr(response, 'content') else str(response)

        # If model appears reluctant or refuses, fall back to deterministic plant-based info
        if self._is_refusal_response(text):
            text = self._fallback_answer(question)
            source = 'fallback'
        else:
            source = 'groq'

        self.conversation_history.append(("assistant", text))

        # Structured response to support UI buttons and JSON payload
        return {
            'answer': text,
            'suggestions': self._generate_suggestions(self.current_plant),
            'plant': self.current_plant,
            'source': source
        }


if __name__ == '__main__':
    assistant = MedicinalPlantChatAssistant()

    print("Medicinal Plant Chat Assistant CLI")
    plant = input("Enter identified plant name: ").strip()
    try:
        intro = assistant.set_plant(plant)
        print(intro)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    while True:
        q = input("Ask a question (or 'exit'): ").strip()
        if q.lower() in ('exit', 'quit'):
            break
        try:
            ans = assistant.answer_question(q)
            print(f"Assistant: {ans}\n")
        except Exception as e:
            print(f"Error: {e}")
