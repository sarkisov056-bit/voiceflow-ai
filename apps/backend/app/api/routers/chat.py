"""``/chat`` HTTP route.

Exposes the existing ``ConversationService.chat()`` business logic over
HTTP. This module contains no business logic of its own: it only
translates an HTTP request into a call to ``ConversationService`` and
the result back into an HTTP response.

Errors raised by the underlying AI provider (``AIProviderError``) are
not handled here — they propagate up and are translated into an HTTP 503
by the app-level exception handler registered in ``app.main``, so this
keeps the route handler itself free of error-translation logic.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.ai.conversation.service import ConversationService
from app.api.dependencies import get_conversation_service
from app.api.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send a chat message and get the AI assistant's reply",
    description=(
        "Sends a user message for a given conversation session to the "
        "existing ConversationService and returns the AI assistant's "
        "reply text."
    ),
)
async def chat(
    request: ChatRequest,
    conversation_service: ConversationService = Depends(get_conversation_service),
) -> ChatResponse:
    """Handle ``POST /chat``.

    Args:
        request: The parsed request body (``session_id`` and
            ``message``).
        conversation_service: The application's ``ConversationService``,
            injected by FastAPI via ``Depends`` — never constructed here.

    Returns:
        A ``ChatResponse`` containing the AI assistant's reply text.
    """
    reply = await conversation_service.chat(
        session_id=request.session_id,
        message=request.message,
    )
    return ChatResponse(reply=reply)
