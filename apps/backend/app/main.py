"""Application entry point.

Wires up the AI Core (``ConversationService`` and its collaborators)
once at startup and exposes it over HTTP via the routers in ``app.api``.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.ai.conversation.service import ConversationService
from app.ai.memory.service import MemoryService
from app.ai.providers.interfaces import AIProviderError
from app.ai.providers.openai.provider import OpenAIProvider
from app.api.routers.chat import router as chat_router
from app.core.settings import load_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Build the AI Core collaborators once, for the lifetime of the app.

    ``ConversationService`` (and the ``MemoryService``/``OpenAIProvider``
    it depends on) is constructed exactly once here, at startup, and
    stored on ``app.state``. Route handlers never construct it
    themselves; they receive it via the ``get_conversation_service``
    dependency (see ``app.api.dependencies``), which simply reads it back
    off ``app.state``.

    Building it once (rather than per-request) is what allows
    conversation history in ``MemoryService`` to persist across HTTP
    requests for the same ``session_id``.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control back to FastAPI once startup wiring is complete.
    """
    settings = load_settings()
    ai_provider = OpenAIProvider.from_settings(settings)
    memory_service = MemoryService()
    app.state.conversation_service = ConversationService(
        ai_provider=ai_provider,
        memory_service=memory_service,
    )
    yield


app = FastAPI(
    title="AI Voice Sales Manager API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(chat_router)


@app.exception_handler(AIProviderError)
async def ai_provider_error_handler(request: Request, exc: AIProviderError) -> JSONResponse:
    """Translate AI provider failures into a generic HTTP 503.

    The underlying vendor error message (e.g. from the OpenAI SDK) is
    deliberately not included in the response, so internal provider
    details are never exposed to API consumers.

    Args:
        request: The incoming request that triggered the error.
        exc: The ``AIProviderError`` raised by the AI provider layer.

    Returns:
        A JSON response with HTTP status 503 and a generic message.
    """
    return JSONResponse(
        status_code=503,
        content={"detail": "The AI service is temporarily unavailable. Please try again later."},
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
