"""Interfaces for AI provider implementations."""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Sequence

from app.ai.conversation.models import ConversationMessage


class AIProvider(ABC):
    """Abstract contract for future AI model providers.

    Implementations of this interface will encapsulate provider-specific
    integration details, such as request formatting, authentication, response
    parsing, and streaming mechanics. The application layer should depend on
    this abstraction rather than on concrete SDKs or vendors, which keeps the
    AI Core open for extension without forcing callers to change when a new
    provider is added.

    This interface intentionally does not connect to any external provider yet.
    Concrete implementations should be introduced separately when provider
    integration becomes part of the project scope.
    """

    @abstractmethod
    async def generate_response(
        self,
        messages: Sequence[ConversationMessage],
    ) -> ConversationMessage:
        """Generate a complete response for the supplied conversation messages.

        Args:
            messages: Ordered conversation messages that provide context for the
                provider request.

        Returns:
            A conversation message containing the generated assistant response.
        """
        raise NotImplementedError()

    @abstractmethod
    async def stream_response(
        self,
        messages: Sequence[ConversationMessage],
    ) -> AsyncIterator[str]:
        """Stream response chunks for the supplied conversation messages.

        Args:
            messages: Ordered conversation messages that provide context for the
                provider request.

        Returns:
            An asynchronous iterator that yields response text chunks.
        """
        raise NotImplementedError()
