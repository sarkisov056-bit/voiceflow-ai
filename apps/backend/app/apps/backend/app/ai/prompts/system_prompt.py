"""System prompt definitions.

This module will hold the system prompt(s) used to instruct the AI
assistant on its role, tone, and constraints. No prompt content has been
authored yet — only a placeholder accessor is defined so that other
modules can depend on a stable import path from the start.
"""

from __future__ import annotations


def get_system_prompt() -> str:
    """Return the system prompt used to initialize the AI assistant.

    Returns:
        The system prompt text.

    Raises:
        NotImplementedError: Always, at this stage of development. The
            actual prompt content will be added in a later iteration.
    """
    raise NotImplementedError()
