# Examples

Standalone, executable scripts that exercise the AI Core business logic
directly — without FastAPI, without HTTP, and without a running server.
They exist to demonstrate and manually verify that the underlying
Python classes (`ConversationService`, `MemoryService`, `OpenAIProvider`)
work correctly on their own.

## `chat_demo.py`

Sends a single message ("Здравствуйте!") through the real
`ConversationService` (backed by `OpenAIProvider` and an in-memory
`MemoryService`) and prints the AI's reply to the console.

### Prerequisites

1. Install the backend's dependencies (from `apps/backend/`):

   ```bash
   pip install --break-system-packages .
   ```

   (or use `uv sync` if you manage this project with [uv](https://docs.astral.sh/uv/)).

2. Set your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

   Optional environment variables (see `app/core/settings.py`):

   | Variable               | Purpose                                      | Default          |
   |------------------------|-----------------------------------------------|------------------|
   | `OPENAI_BASE_URL`      | Custom API base URL (e.g. a proxy)             | OpenAI's default |
   | `OPENAI_DEFAULT_MODEL` | Model used when none is specified              | `gpt-4.1-mini`   |

### Run it

From the `apps/backend` directory:

```bash
python examples/chat_demo.py
```

### Expected output

```
You: Здравствуйте!
AI: <the model's reply>
```

If `OPENAI_API_KEY` is missing, the script will fail fast with a clear
`RuntimeError` from `app.core.settings.load_settings()` instead of a
confusing SDK error.
