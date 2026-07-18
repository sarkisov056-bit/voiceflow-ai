"""OpenAI implementation of the ``AIProvider`` interface.

This module defines ``OpenAIProvider``, the concrete ``AIProvider``
implementation backed by OpenAI. It never talks to the OpenAI SDK
directly — all SDK interaction is delegated to ``OpenAIClient``, and all
data translation is delegated to ``OpenAIRequestResponseMapper``.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from app.ai.providers.interfaces import AIProvider, GenerationRequest, GenerationResponse
from app.ai.providers.openai.client import OpenAIClient
from app.ai.providers.openai.mapper import OpenAIRequestResponseMapper
from app.core.settings import Settings


class OpenAIProvider(AIProvider):
    """``AIProvider`` implementation backed by the OpenAI Responses API.

    ``OpenAIProvider`` composes an ``OpenAIClient`` (SDK interaction) and
    an ``OpenAIRequestResponseMapper`` (data translation) to implement
    the provider-agnostic ``AIProvider`` interface. It has no direct
    dependency on the ``openai`` package itself, and no business logic
    beyond orchestrating its two collaborators (Single Responsibility
    Principle).

    Both collaborators are injected through the constructor rather than
    constructed internally or looked up from global state, so this class
    has no singleton or global state and can be freely composed and
    tested with fakes or mocks in place of ``OpenAIClient``.
    """

    def __init__(
        self,
        client: OpenAIClient,
        mapper: OpenAIRequestResponseMapper,
        default_model: str,
    ) -> None:
        """Initialize the OpenAI provider.

        Args:
            client: The ``OpenAIClient`` used to talk to the OpenAI API.
            mapper: The mapper used to translate between AI Core types
                and the OpenAI API's request/response shapes.
            default_model: The model name used when a
                ``GenerationRequest`` does not specify one explicitly
                (i.e. when ``request.model`` is an empty string).
        """
        self._client = client
        self._mapper = mapper
        self._default_model = default_model

    @classmethod
    def from_settings(cls, settings: Settings) -> "OpenAIProvider":
        """Build a fully configured ``OpenAIProvider`` from ``Settings``.

        This is the intended entry point for constructing an
        ``OpenAIProvider`` in application composition code. It reads no
        environment variables itself — it relies entirely on the
        already-loaded ``Settings`` instance — so ``os.getenv`` never
        appears anywhere in the provider layer.

        Args:
            settings: The application settings, expected to contain the
                OpenAI-related configuration values.

        Returns:
            A fully configured ``OpenAIProvider`` instance.
        """
        client = OpenAIClient(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )
        return cls(
            client=client,
            mapper=OpenAIRequestResponseMapper(),
            default_model=settings.openai_default_model,
        )

    async def generate_response(self, request: GenerationRequest) -> GenerationResponse:
        """Generate a single, complete AI response via OpenAI.

        Args:
            request: The provider-agnostic generation request.

        Returns:
            The generated response as a ``GenerationResponse``.

        Raises:
            AIProviderError: If the OpenAI API call fails.
        """
        model = request.model or self._default_model
        input_items = self._mapper.to_openai_input(request.messages)

        raw_response = await self._client.create_response(
            model=model,
            input_items=input_items,
            instructions=request.system_prompt,
            temperature=request.temperature,
        )

        return self._mapper.to_generation_response(raw_response, model=model)

    async def stream_response(self, request: GenerationRequest) -> AsyncIterator[str]:
        """Generate an AI response as a stream of text chunks via OpenAI.

        Implemented as an async generator: awaiting/iterating this method
        yields partial response text as it arrives from OpenAI, rather
        than waiting for the full response to complete.

        Args:
            request: The provider-agnostic generation request.

        Yields:
            Partial response text chunks as they arrive from OpenAI.

        Raises:
            AIProviderError: If the OpenAI API call fails.
        """
        model = request.model or self._default_model
        input_items = self._mapper.to_openai_input(request.messages)

        async for event in self._client.stream_response_events(
            model=model,
            input_items=input_items,
            instructions=request.system_prompt,
            temperature=request.temperature,
        ):
            text_delta = self._mapper.extract_text_delta(event)
            if text_delta:
                yield text_delta
