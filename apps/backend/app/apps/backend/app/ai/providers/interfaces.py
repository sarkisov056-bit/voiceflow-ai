"""Abstract interface for AI model providers.

This module defines the contract that concrete AI providers (e.g. OpenAI,
Anthropic, local models, etc.) must implement. Defining this as an
abstract interface allows the rest of the AI Core to depend on an
abstraction rather than a concrete provider implementation, following the
Dependency Inversion Principle (the "D" in SOLID).

No concrete provider is implemented in this module. Implementations will
be added in dedicated modules (e.g. ``providers/openai_provider.py``) in
future work.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any


class AIProvider(ABC):
    """Abstract base class describing an AI model provider.

    Any class that wants to act as a source of AI-generated responses
    (for example, a wrapper around a specific LLM vendor's API) must
    inherit from this class and implement all of its abstract methods.

    This interface intentionally knows nothing about *which* provider is
    used underneath (OpenAI, Anthropic, a local model, etc.). Consumers of
    this interface (such as ``ConversationService``) should only depend on
    this abstraction, never on a concrete provider class, so that
    providers can be swapped or added without changing consumer code
    (Open/Closed Principle).
    """

    @abstractmethod
    async def generate_response(self, *args: Any, **kwargs: Any) -> Any:
        """Generate a single, complete AI response.

        This method is expected to take conversation input (e.g. a list of
        messages) and return a full response once generation is complete.

        Args:
            *args: Positional arguments defined by the concrete provider
                implementation.
            **kwargs: Keyword arguments defined by the concrete provider
                implementation.

        Returns:
            The generated response. The exact type will be defined once a
            concrete provider implementation is added.

        Raises:
            NotImplementedError: Always, since this is an unimplemented
                interface method. Concrete subclasses must override it.
        """
        raise NotImplementedError()

    @abstractmethod
    def stream_response(self, *args: Any, **kwargs: Any) -> AsyncIterator[Any]:
        """Generate an AI response as an asynchronous stream of chunks.

        This method is expected to take conversation input (e.g. a list of
        messages) and yield partial response chunks as they become
        available, enabling low-latency, incremental delivery of output.

        Args:
            *args: Positional arguments defined by the concrete provider
                implementation.
            **kwargs: Keyword arguments defined by the concrete provider
                implementation.

        Returns:
            An asynchronous iterator yielding response chunks. The exact
            chunk type will be defined once a concrete provider
            implementation is added.

        Raises:
            NotImplementedError: Always, since this is an unimplemented
                interface method. Concrete subclasses must override it.
        """
        raise NotImplementedError()
