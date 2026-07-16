"""Conversation service shell for future AI orchestration logic."""

from collections.abc import Sequence

from app.ai.conversation.models import ConversationMessage


class ConversationService:
    """Coordinates future conversation-level AI workflows.

    This service is intended to become the application-facing entry point for
    conversation orchestration. Future responsibilities may include validating
    incoming conversation input, coordinating memory retrieval, invoking an AI
    provider through an abstraction, and returning normalized conversation
    output.

    The class currently contains no business logic and does not instantiate or
    depend on concrete providers. Dependencies should be injected by callers when
    implementations are added, preserving single responsibility and dependency
    inversion principles.
    """

    async def generate_reply(
        self,
        messages: Sequence[ConversationMessage],
    ) -> ConversationMessage:
        """Generate a normalized assistant reply for a conversation.

        Args:
            messages: Ordered messages representing the current conversation
                context.

        Returns:
            A generated assistant conversation message.
        """
        raise NotImplementedError()
