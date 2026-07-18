"""Thin async wrapper around the OpenAI SDK.

This module is the only place in the OpenAI provider implementation that
is allowed to import and call the ``openai`` package directly. Every
other module in the provider layer (``provider.py``, ``mapper.py``) must
go through ``OpenAIClient`` instead of touching the SDK itself, so that
the SDK dependency stays fully isolated behind this one class.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

import openai
from openai import AsyncOpenAI

from app.ai.providers.interfaces import AIProviderError


class OpenAIClient:
    """Async wrapper around the OpenAI SDK's Responses API.

    ``OpenAIClient`` owns the OpenAI SDK client instance and is
    responsible only for sending requests to OpenAI and translating SDK
    exceptions into the provider-agnostic ``AIProviderError``. It knows
    nothing about the AI Core's internal ``GenerationRequest``/
    ``GenerationResponse`` types — that translation is the responsibility
    of ``mapper.py``. Keeping this separation means ``OpenAIProvider``
    never imports the ``openai`` package directly (Single Responsibility
    Principle).

    Each ``OpenAIClient`` instance is explicitly constructed with its own
    configuration; there is no global or singleton client shared across
    the application.
    """

    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        """Initialize the underlying OpenAI SDK client.

        Args:
            api_key: The secret API key used to authenticate with OpenAI.
            base_url: Optional custom base URL for the OpenAI API (e.g.
                for proxies or OpenAI-compatible endpoints). ``None``
                uses the SDK's default base URL.
        """
        self._sdk_client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def create_response(
        self,
        *,
        model: str,
        input_items: list[dict[str, Any]],
        instructions: str | None,
        temperature: float,
    ) -> Any:
        """Call OpenAI's Responses API and return the raw SDK response.

        Args:
            model: The model name/identifier to use.
            input_items: The conversation input, already formatted for
                the Responses API's ``input`` parameter (see
                ``mapper.py``).
            instructions: The system/instructions prompt for the model.
            temperature: Sampling temperature.

        Returns:
            The raw ``Response`` object returned by the OpenAI SDK.

        Raises:
            AIProviderError: If the OpenAI API call fails for any reason
                (network error, rate limiting, invalid request, server
                error, etc.).
        """
        try:
            return await self._sdk_client.responses.create(
                model=model,
                input=input_items,
                instructions=instructions,
                temperature=temperature,
            )
        except openai.APIError as exc:
            raise AIProviderError(f"OpenAI API request failed: {exc}") from exc

    async def stream_response_events(
        self,
        *,
        model: str,
        input_items: list[dict[str, Any]],
        instructions: str | None,
        temperature: float,
    ) -> AsyncIterator[Any]:
        """Call OpenAI's Responses API in streaming mode.

        Yields the raw streaming event objects produced by the OpenAI
        SDK as they arrive. Translating those events into plain text
        chunks is the responsibility of ``mapper.py``.

        Args:
            model: The model name/identifier to use.
            input_items: The conversation input, already formatted for
                the Responses API's ``input`` parameter (see
                ``mapper.py``).
            instructions: The system/instructions prompt for the model.
            temperature: Sampling temperature.

        Yields:
            Raw streaming event objects as returned by the OpenAI SDK.

        Raises:
            AIProviderError: If the OpenAI API call fails for any reason
                (network error, rate limiting, invalid request, server
                error, etc.).
        """
        try:
            async with self._sdk_client.responses.stream(
                model=model,
                input=input_items,
                instructions=instructions,
                temperature=temperature,
            ) as stream:
                async for event in stream:
                    yield event
        except openai.APIError as exc:
            raise AIProviderError(f"OpenAI API streaming request failed: {exc}") from exc
