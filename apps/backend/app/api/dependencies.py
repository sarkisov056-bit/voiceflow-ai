"""Dependency providers for the HTTP API layer.

These functions are FastAPI dependencies (used via ``Depends``) that
supply already-constructed AI Core collaborators to route handlers.
Route handlers never construct ``ConversationService`` (or its
collaborators) themselves — they only declare a dependency on it.

The actual instances are built once, at application startup (see the
``lifespan`` context manager in ``app.main``), and stored on
``app.state``. This is composition-root wiring, not a singleton pattern
inside the AI Core: none of the AI Core classes (``ConversationService``,
``MemoryService``, ``OpenAIProvider``) know about or enforce single-
instance behavior themselves: it is FastAPI's own dependency-injection
container, at the edge of the application, that decides to reuse one
instance per process so that conversation history persists across HTTP
requests.
"""

from __future__ import annotations

from fastapi import Request

from app.ai.conversation.service import ConversationService


def get_conversation_service(request: Request) -> ConversationService:
    """Provide the application's shared ``ConversationService`` instance.

    Args:
        request: The incoming FastAPI request, used to reach the
            application instance and its ``state``.

    Returns:
        The ``ConversationService`` instance created at application
        startup.
    """
    return request.app.state.conversation_service
