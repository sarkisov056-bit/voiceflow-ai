"""Conversation orchestration service.

This module defines ``ConversationService``, the future entry point for
managing the lifecycle of a conversation between a user and the AI
assistant. At this stage the class only defines its intended public API;
no business logic has been implemented yet.
"""

from __future__ import annotations

from app.ai.conversation.models import ConversationMessage
from app.ai.providers.interfaces import AIProvider


class ConversationService:
    """Orchestrates a conversation between a user and an AI provider.

    ``ConversationService`` is intended to be the central coordination
    point for a single conversation: it will be responsible for
    accumulating ``ConversationMessage`` history, delegating response
    generation to an injected :class:`~app.ai.providers.interfaces.AIProvider`,
    and exposing conversation state to the rest of the application.

    The concrete :class:`AIProvider` implementation is injected via the
    constructor rather than looked up globally, so that this service
    depends only on the ``AIProvider`` abstraction and never on a specific
    vendor (Dependency Inversion Principle). This also keeps the class
    free of singletons and global state: each ``ConversationService``
    instance is an independent, explicitly-constructed object.

    No business logic is implemented yet. Every public method currently
    raises ``NotImplementedError`` and will be filled in during a later
    iteration.
    """

    def __init__(self, ai_provider: AIProvider) -> None:
        """Initialize the conversation service.

        Args:
            ai_provider: The AI provider used to generate responses for
                this conversation. Must implement the ``AIProvider``
                interface. No concrete provider is wired up at this stage.
        """
        self._ai_provider = ai_provider

    async def start_conversation(self) -> None:
        """Start a new conversation.

        Intended to initialize any state required before messages can be
        exchanged (e.g. preparing an empty message history).

        Raises:
            NotImplementedError: Always, at this stage of development.
        """
        raise NotImplementedError()

    async def send_message(self, message: ConversationMessage) -> ConversationMessage:
        """Send a user message and obtain the AI assistant's reply.

        Intended to append ``message`` to the conversation history,
        delegate response generation to the configured ``AIProvider``,
        and return the assistant's reply as a new ``ConversationMessage``.

        Args:
            message: The message to add to the conversation.

        Returns:
            The AI assistant's reply as a ``ConversationMessage``.

        Raises:
            NotImplementedError: Always, at this stage of development.
        """
        raise NotImplementedError()

    def get_history(self) -> list[ConversationMessage]:
        """Return the full message history of the conversation.

        Returns:
            A list of ``ConversationMessage`` instances in chronological
            order.

        Raises:
            NotImplementedError: Always, at this stage of development.
        """
        raise NotImplementedError()
