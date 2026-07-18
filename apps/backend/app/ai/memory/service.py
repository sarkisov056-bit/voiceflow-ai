"""Conversation memory service.

This module defines ``MemoryService``, the future entry point for storing
and retrieving memory associated with a conversation or a user (e.g.
long-term facts, summaries, preferences). At this stage the class only
defines its intended public API; no storage backend or business logic has
been implemented yet.
"""

from __future__ import annotations

from app.ai.conversation.models import ConversationMessage


class MemoryService:
    """Manages long-term and short-term memory for conversations.

    ``MemoryService`` is intended to abstract away *how* and *where*
    conversational memory is persisted (e.g. in a database, vector store,
    or cache) from the rest of the AI Core. Consumers of this class should
    depend only on its public interface, not on any specific storage
    mechanism, which keeps the storage backend free to change later
    without affecting callers.

    No storage backend or global/singleton state is used: each
    ``MemoryService`` instance is expected to be explicitly constructed
    and, once implemented, configured with whatever storage dependency it
    needs via its constructor.

    No business logic is implemented yet. Every public method currently
    raises ``NotImplementedError`` and will be filled in during a later
    iteration.
    """

    async def remember(self, message: ConversationMessage) -> None:
        """Persist a message (or facts derived from it) into memory.

        Args:
            message: The conversation message to remember.

        Raises:
            NotImplementedError: Always, at this stage of development.
        """
        raise NotImplementedError()

    async def recall(self, query: str) -> list[ConversationMessage]:
        """Retrieve memory entries relevant to a given query.

        Args:
            query: A natural-language query used to search stored memory.

        Returns:
            A list of ``ConversationMessage`` instances relevant to the
            query.

        Raises:
            NotImplementedError: Always, at this stage of development.
        """
        raise NotImplementedError()

    async def clear(self) -> None:
        """Clear all stored memory managed by this service instance.

        Raises:
            NotImplementedError: Always, at this stage of development.
        """
        raise NotImplementedError()
