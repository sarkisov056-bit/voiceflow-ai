"""HTTP API layer.

This package is the only part of the application allowed to know about
FastAPI, HTTP requests/responses, and status codes. It exposes the
existing AI Core business logic (``ConversationService``) over HTTP
without altering it: no business logic lives here, only request/response
schemas, routing, dependency wiring, and error translation.
"""
