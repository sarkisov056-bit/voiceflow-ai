"""OpenAI provider implementation.

Contains the concrete implementation of :class:`~app.ai.providers.interfaces.AIProvider`
backed by the official OpenAI Python SDK, split into three layers:

    - ``client``: thin async wrapper around the OpenAI SDK (Responses API).
    - ``mapper``: pure functions converting between internal AI Core
      types (``GenerationRequest``/``GenerationResponse``) and the
      OpenAI API's request/response shapes.
    - ``provider``: ``OpenAIProvider``, the ``AIProvider`` implementation
      that composes the client and mapper.
"""
