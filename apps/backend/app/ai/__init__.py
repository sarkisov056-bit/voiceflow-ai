"""AI Core package.

This package is the foundation for the AI subsystem of VoiceFlow AI.
It groups together the building blocks needed to talk to language model
providers, manage conversation state, retain long-term memory, expose
skills/tools to the model, and store system prompts.

The package currently only defines the architectural skeleton (interfaces,
data structures, and empty service classes). No provider integrations or
business logic are implemented yet — that will be added in follow-up work.

Sub-packages:
    - ``providers``: abstract interfaces for AI model providers (e.g. LLMs).
    - ``conversation``: conversation state management (messages, service).
    - ``memory``: long-term/short-term memory management for conversations.
    - ``skills``: registry and interfaces for pluggable AI skills/tools.
    - ``prompts``: system prompt definitions used to steer AI behavior.
"""
