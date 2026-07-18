"""Mapping between internal AI Core types and the OpenAI API shapes.

This module contains only pure, side-effect-free conversion logic
between:
    - ``ConversationMessage`` objects -> the ``input`` format expected by
      OpenAI's Responses API.
    - The raw OpenAI SDK response/streaming events -> the AI Core's
      ``GenerationResponse`` (or plain text chunks, for streaming).

Keeping this translation logic separate from ``OpenAIClient`` (which only
talks to the SDK) and ``OpenAIProvider`` (which orchestrates the two)
keeps each class focused on a single responsibility.
"""

from __future__ import annotations

from typing import Any

from app.ai.conversation.models import ConversationMessage
from app.ai.providers.interfaces import GenerationResponse


class OpenAIRequestResponseMapper:
    """Converts between AI Core types and the OpenAI Responses API shapes.

    This class holds no state — it is a small collection of stateless
    conversion methods grouped together for discoverability. It could
    equally be a set of module-level functions; it is written as a class
    to keep the provider layer consistent (each concern gets its own
    injectable collaborator) and to make it easy to add configuration or
    swap the mapping strategy later without changing ``OpenAIProvider``.
    """

    @staticmethod
    def to_openai_input(messages: list[ConversationMessage]) -> list[dict[str, str]]:
        """Convert conversation messages into the Responses API input format.

        Args:
            messages: The conversation history to convert, in
                chronological order.

        Returns:
            A list of role/content dictionaries in the shape expected by
            the ``input`` parameter of OpenAI's Responses API.
        """
        return [{"role": message.role, "content": message.content} for message in messages]

    @staticmethod
    def to_generation_response(raw_response: Any, model: str) -> GenerationResponse:
        """Convert a raw OpenAI Responses API result into a ``GenerationResponse``.

        Args:
            raw_response: The raw ``Response`` object returned by the
                OpenAI SDK's ``responses.create`` call.
            model: The model name/identifier that was requested, used as
                a fallback if the raw response does not expose one.

        Returns:
            A provider-agnostic ``GenerationResponse``.
        """
        text = getattr(raw_response, "output_text", "") or ""
        usage = getattr(raw_response, "usage", None)
        prompt_tokens = getattr(usage, "input_tokens", 0) if usage is not None else 0
        completion_tokens = getattr(usage, "output_tokens", 0) if usage is not None else 0
        response_model = getattr(raw_response, "model", None) or model

        return GenerationResponse(
            text=text,
            usage_prompt_tokens=prompt_tokens,
            usage_completion_tokens=completion_tokens,
            model=response_model,
        )

    @staticmethod
    def extract_text_delta(event: Any) -> str | None:
        """Extract a plain text chunk from a raw OpenAI streaming event.

        Args:
            event: A raw streaming event object yielded by the OpenAI
                SDK's ``responses.stream`` context manager.

        Returns:
            The text delta carried by the event, or ``None`` if the event
            does not carry a text delta (e.g. lifecycle events such as
            "response.created" or "response.completed").
        """
        if getattr(event, "type", None) == "response.output_text.delta":
            return getattr(event, "delta", None)
        return None
