"""Conversation orchestration service.

This module defines ``ConversationService``, the central coordination
point for a single chat interaction: it retrieves history from a
``MemoryService``, builds a provider-agnostic ``GenerationRequest``,
delegates generation to an injected ``AIProvider``, and stores the
result back into memory.

``ConversationService`` is a plain Python class with no dependency on
FastAPI, HTTP, or any specific AI vendor SDK. It can be constructed and
exercised directly in unit tests, without running a server.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.ai.conversation.models import ConversationMessage
from app.ai.memory.service import MemoryService
from app.ai.prompts.system_prompt import get_system_prompt
from app.ai.providers.interfaces import AIProvider, GenerationRequest


class ConversationService:
    """Orchestrates a single chat turn between a user and an AI provider.

    ``ConversationService`` is the first business-logic layer of the AI
    Core. For a given session, it:

        1. Reads the existing message history from ``MemoryService``.
        2. Appends the new user message to that history.
        3. Builds a provider-agnostic ``GenerationRequest``.
        4. Delegates response generation to the injected ``AIProvider``.
        5. Stores the assistant's reply back into ``MemoryService``.
        6. Returns only the assistant's reply text to the caller.

    Both the ``AIProvider`` and the ``MemoryService`` are injected via the
    constructor (Dependency Injection), so ``ConversationService`` depends
    only on their abstractions/public interfaces — never on a specific AI
    vendor SDK or storage mechanism (Dependency Inversion Principle). This
    also means the class holds no global or singleton state: each
    instance is independent and explicitly constructed, and is a plain
    Python object that can be unit tested without FastAPI or a running
    server.
    """

    def __init__(self, ai_provider: AIProvider, memory_service: MemoryService) -> None:
        """Initialize the conversation service.

        Args:
            ai_provider: The AI provider used to generate responses.
                Must implement the ``AIProvider`` interface.
            memory_service: The service used to read and store
                conversation history, scoped by session id.
        """
        self._ai_provider = ai_provider
        self._memory_service = memory_service

    async def chat(self, session_id: str, message: str) -> str:
        """Process one chat turn for a session and return the AI's reply.

        Args:
            session_id: The unique identifier of the conversation
                session. A new session is created implicitly the first
                time it is used.
            message: The user's message text for this turn.

        Returns:
            The AI assistant's reply text.

        Raises:
            AIProviderError: If the underlying AI provider fails to
                generate a response.
        """
        history = await self._memory_service.get_history(session_id)

        user_message = ConversationMessage(
            role="user",
            content=message,
            timestamp=datetime.now(timezone.utc),
        )
        await self._memory_service.add_message(session_id, user_message)

        request = GenerationRequest(
            system_prompt=get_system_prompt(),
            messages=[*history, user_message],
        )
        response = await self._ai_provider.generate_response(request)

        assistant_message = ConversationMessage(
            role="assistant",
            content=response.text,
            timestamp=datetime.now(timezone.utc),
        )
        await self._memory_service.add_message(session_id, assistant_message)

        return response.text
