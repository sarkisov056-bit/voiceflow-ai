"""Pydantic request/response schemas for the HTTP API.

These models define the wire format of the API only. They intentionally
mirror the shape of ``ConversationService.chat()``'s parameters and
return value, but remain separate from it: the HTTP layer should never
leak into (or be leaked into by) the AI Core's internal types.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for ``POST /chat``.

    Attributes:
        session_id: Identifier of the conversation session. A new
            session is created implicitly the first time it is used.
        message: The user's message text for this turn.
    """

    session_id: str = Field(..., description="Conversation session identifier.")
    message: str = Field(..., description="The user's message text.")


class ChatResponse(BaseModel):
    """Response body for ``POST /chat``.

    Attributes:
        reply: The AI assistant's reply text.
    """

    reply: str = Field(..., description="The AI assistant's reply text.")
