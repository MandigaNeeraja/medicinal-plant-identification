import sys
from datetime import datetime, timezone

PROJECT_ROOT = __import__('os').path.abspath(
    __import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..', '..')
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from assis import MedicinalPlantChatAssistant  # noqa: E402
from backend.app.extensions import db
from backend.app.models import ChatMessage, ChatSession


class ChatService:
    _assistants = {}

    @classmethod
    def _get_assistant(cls, user_id):
        if user_id not in cls._assistants:
            cls._assistants[user_id] = MedicinalPlantChatAssistant()
        return cls._assistants[user_id]

    @staticmethod
    def _get_or_create_session(user_id, plant_name):
        session = (
            ChatSession.query.filter_by(user_id=user_id, plant_name=plant_name)
            .order_by(ChatSession.updated_at.desc())
            .first()
        )
        if not session:
            session = ChatSession(user_id=user_id, plant_name=plant_name)
            db.session.add(session)
            db.session.commit()
        return session

    @staticmethod
    def _save_message(session_id, role, content):
        message = ChatMessage(session_id=session_id, role=role, content=content)
        db.session.add(message)
        db.session.commit()
        return message

    @staticmethod
    def _load_history(session_id):
        return (
            ChatMessage.query.filter_by(session_id=session_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )

    @classmethod
    def init_chat(cls, user_id, plant_name):
        session = cls._get_or_create_session(user_id, plant_name)
        stored_messages = cls._load_history(session.id)
        assistant = cls._get_assistant(user_id)

        if stored_messages:
            assistant.set_plant(plant_name)
            assistant.conversation_history = [
                (message.role, message.content) for message in stored_messages
            ]
            result = {
                'plant': plant_name,
                'summary': {'plant': plant_name},
                'message': f"Chat history loaded for '{plant_name}'.",
                'suggestions': assistant._generate_suggestions(plant_name),
            }
        else:
            result = assistant.set_plant(plant_name)
            for role, content in assistant.conversation_history:
                cls._save_message(session.id, role, content)

        session.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return {
            'session': session.to_dict(),
            'plant': plant_name,
            'summary': result.get('summary'),
            'suggestions': result.get('suggestions', []),
            'message': result.get('message'),
        }

    @classmethod
    def send_message(cls, user_id, plant_name, message):
        if not message:
            raise ValueError('Message is required')

        session = cls._get_or_create_session(user_id, plant_name)
        assistant = cls._get_assistant(user_id)

        if assistant.current_plant != plant_name:
            cls.init_chat(user_id, plant_name)

        response = assistant.answer_question(message)
        cls._save_message(session.id, 'user', message)
        cls._save_message(session.id, 'assistant', response.get('answer', ''))

        session.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return {
            'plant': response.get('plant'),
            'answer': response.get('answer'),
            'suggestions': response.get('suggestions', []),
            'source': response.get('source', 'groq'),
        }

    @staticmethod
    def get_history(user_id, plant_name):
        session = (
            ChatSession.query.filter_by(user_id=user_id, plant_name=plant_name)
            .order_by(ChatSession.updated_at.desc())
            .first()
        )
        if not session:
            return {'session': None, 'messages': []}

        messages = ChatService._load_history(session.id)
        return {
            'session': session.to_dict(),
            'messages': [
                message.to_dict()
                for message in messages
                if message.role in ('user', 'assistant')
            ],
        }
