"""Data models for conversation state.

This module defines the plain data structures used to represent a
conversation. It intentionally contains no behavior/business logic —
only data.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConversationMessage:
    """A single message exchanged within a conversation.

    This is a plain data holder (no behavior) representing one turn in a
    conversation between a user, an AI assistant, or the system.

    Attributes:
        role: Who produced the message (e.g. "user", "assistant",
            "system"). Kept as ``str`` at this stage so the exact set of
            allowed roles can be decided in a later iteration.
        content: The textual content of the message.
        timestamp: The point in time the message was created.
    """

    role: str
    content: str
    timestamp: datetime
