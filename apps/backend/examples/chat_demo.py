"""Standalone, no-HTTP demo of VoiceFlow AI's conversation layer.

This script wires up the real ``ConversationService`` — backed by
``OpenAIProvider`` and the in-memory ``MemoryService`` — and sends it a
single message, printing the AI's reply to the console.

It exists purely to prove that the AI Core business logic works end to
end without FastAPI, HTTP, or a running server: it is a plain Python
script that talks to OpenAI directly through the same classes the future
API layer will use.

Usage:
    cd apps/backend
    export OPENAI_API_KEY=sk-...   # see examples/README.md for details
    python examples/chat_demo.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# This script lives in apps/backend/examples/. When run directly (e.g.
# `python examples/chat_demo.py`), Python only puts this file's own
# directory on sys.path, not the apps/backend package root — so
# `import app...` would fail. Adding the parent directory here lets the
# script run as-is, without requiring the caller to set PYTHONPATH.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.ai.conversation.service import ConversationService  # noqa: E402
from app.ai.memory.service import MemoryService  # noqa: E402
from app.ai.providers.openai.provider import OpenAIProvider  # noqa: E402
from app.core.settings import load_settings  # noqa: E402


async def main() -> None:
    """Send one message through ConversationService and print the reply."""
    settings = load_settings()

    ai_provider = OpenAIProvider.from_settings(settings)
    memory_service = MemoryService()
    conversation_service = ConversationService(
        ai_provider=ai_provider,
        memory_service=memory_service,
    )

    user_message = "Здравствуйте!"
    print(f"You: {user_message}")

    reply = await conversation_service.chat(
        session_id="demo-session",
        message=user_message,
    )
    print(f"AI: {reply}")


if __name__ == "__main__":
    asyncio.run(main())
