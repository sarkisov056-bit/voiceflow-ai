"""Conversation data models used by AI Core services."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ConversationMessage:
    """Immutable representation of a single conversation message.

    The model captures the minimum common shape needed to pass conversation
    context between future AI Core components without binding the application to
    a specific provider schema. It is intentionally lightweight so provider
    adapters, memory services, and orchestration code can transform it as needed
    while preserving a stable internal contract.

    Attributes:
        role: Logical author of the message, such as a user, assistant, or
            system role.
        content: Textual message content.
        timestamp: Time when the message was created or accepted by the system.
    """

    role: str
    content: str
    timestamp: datetime
