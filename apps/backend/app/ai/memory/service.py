"""Memory service shell for future context persistence and retrieval."""

from collections.abc import Sequence

from app.ai.conversation.models import ConversationMessage


class MemoryService:
    """Manages future conversation memory operations.

    This service is reserved for persistence, retrieval, and preparation of
    conversation context that may be needed by AI workflows. Keeping memory
    responsibilities isolated from conversation orchestration makes it possible
    to evolve storage and retrieval strategies without changing provider or
    conversation service contracts.

    No storage backend, cache, or external dependency is configured here. Future
    implementations should receive required collaborators through dependency
    injection rather than through global state or singleton instances.
    """

    async def load_messages(self, conversation_id: str) -> Sequence[ConversationMessage]:
        """Load messages associated with a conversation identifier.

        Args:
            conversation_id: Stable identifier for the conversation whose memory
                should be loaded.

        Returns:
            Ordered conversation messages associated with the identifier.
        """
        raise NotImplementedError()

    async def save_message(
        self,
        conversation_id: str,
        message: ConversationMessage,
    ) -> None:
        """Persist a message for a conversation identifier.

        Args:
            conversation_id: Stable identifier for the conversation to update.
            message: Conversation message to persist.
        """
        raise NotImplementedError()
