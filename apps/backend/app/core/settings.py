"""Application settings.

This module is the single place in the application that is expected to
read configuration from the environment. Every other component (AI
providers, services, etc.) must receive an already-built ``Settings``
instance through constructor injection instead of calling
``os.getenv``/``os.environ`` itself. This keeps configuration reading
centralized and makes components easy to test with explicit, in-memory
``Settings`` values.

``load_settings`` is a plain factory function, not a singleton: each call
builds a fresh ``Settings`` instance from the current environment. It is
the caller's responsibility (e.g. application startup/composition code)
to call it once and pass the resulting instance around.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Immutable application configuration values.

    Attributes:
        openai_api_key: Secret API key used to authenticate with OpenAI.
        openai_base_url: Optional custom base URL for the OpenAI API
            (useful for proxies or OpenAI-compatible endpoints). ``None``
            means the SDK's default base URL is used.
        openai_default_model: Model name used when a ``GenerationRequest``
            does not specify one explicitly.
    """

    openai_api_key: str
    openai_base_url: str | None
    openai_default_model: str


def load_settings() -> Settings:
    """Build a ``Settings`` instance from the current environment.

    Reads the following environment variables:
        - ``OPENAI_API_KEY`` (required): secret key for OpenAI.
        - ``OPENAI_BASE_URL`` (optional): custom API base URL.
        - ``OPENAI_DEFAULT_MODEL`` (optional): defaults to
          ``"gpt-4.1-mini"`` if not set.

    Returns:
        A populated ``Settings`` instance.

    Raises:
        RuntimeError: If a required environment variable is missing.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError(
            "Missing required environment variable: OPENAI_API_KEY."
        )

    return Settings(
        openai_api_key=openai_api_key,
        openai_base_url=os.environ.get("OPENAI_BASE_URL") or None,
        openai_default_model=os.environ.get("OPENAI_DEFAULT_MODEL", "gpt-4.1-mini"),
    )
