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
from dataclasses import dataclass, field

from app.ai.conversation.models import ConversationMessage


@dataclass
class GenerationRequest:
    """Provider-agnostic request to generate an AI response.

    This dataclass is the single, vendor-neutral shape that any
    :class:`AIProvider` implementation accepts as input. It intentionally
    contains no vendor-specific fields (e.g. no OpenAI-only parameters),
    so that swapping the underlying provider never requires changing the
    calling code.

    Attributes:
        system_prompt: The instruction/system prompt that should steer
            the model's behavior for this generation.
        messages: The conversation history to send to the model, in
            chronological order.
        temperature: Sampling temperature controlling response
            randomness. Interpretation is provider-specific. ``None``
            means "use the provider/model's default" — this matters
            because some models (e.g. OpenAI's reasoning models) reject
            this parameter entirely if it is set at all.
        model: The name/identifier of the model to use for generation.
    """

    system_prompt: str
    messages: list[ConversationMessage] = field(default_factory=list)
    temperature: float | None = None
    model: str = ""


@dataclass
class GenerationResponse:
    """Provider-agnostic result of an AI response generation.

    This dataclass is the single, vendor-neutral shape returned by any
    :class:`AIProvider` implementation, regardless of which vendor
    produced it underneath.

    Attributes:
        text: The generated response text.
        usage_prompt_tokens: Number of tokens consumed by the prompt/
            input side of the request.
        usage_completion_tokens: Number of tokens produced in the
            generated completion/output.
        model: The name/identifier of the model that produced the
            response.
    """

    text: str
    usage_prompt_tokens: int
    usage_completion_tokens: int
    model: str


class AIProviderError(Exception):
    """Raised when an AI provider fails to generate a response.

    This exception is the single, vendor-neutral error type that any
    :class:`AIProvider` implementation must raise when the underlying
    vendor SDK/API call fails, so that calling code never needs to know
    about or catch vendor-specific exception types (e.g. OpenAI SDK
    errors). Concrete providers are expected to catch their vendor's
    exceptions internally and re-raise them wrapped as
    ``AIProviderError``.
    """


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
    async def generate_response(self, request: GenerationRequest) -> GenerationResponse:
        """Generate a single, complete AI response.

        Args:
            request: The provider-agnostic generation request, containing
                the system prompt, conversation history, temperature, and
                model to use.

        Returns:
            The generated response as a ``GenerationResponse``.

        Raises:
            AIProviderError: If the underlying provider fails to generate
                a response.
            NotImplementedError: Always, since this is an unimplemented
                interface method. Concrete subclasses must override it.
        """
        raise NotImplementedError()

    @abstractmethod
    def stream_response(self, request: GenerationRequest) -> AsyncIterator[str]:
        """Generate an AI response as an asynchronous stream of chunks.

        Args:
            request: The provider-agnostic generation request, containing
                the system prompt, conversation history, temperature, and
                model to use.

        Returns:
            An asynchronous iterator yielding partial response text
            chunks as they become available, enabling low-latency,
            incremental delivery of output.

        Raises:
            AIProviderError: If the underlying provider fails to generate
                a response.
            NotImplementedError: Always, since this is an unimplemented
                interface method. Concrete subclasses must override it.
        """
        raise NotImplementedError()
