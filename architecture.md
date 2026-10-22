# Architecture notes

## Current implementation

- `agent.py` reads configuration, receives CLI input, calls OpenRouter, and coordinates the conversation.
- `memory_store.py` loads, validates, saves, and clears the JSON conversation history.
- `memory.json` is created at runtime and should remain local because it may contain private data.
- OpenRouter exposes an OpenAI-compatible chat-completions endpoint.

## Request flow

1. Load `.env` settings and existing memory.
2. Accept a message from the terminal.
3. Send the system prompt and conversation history to the configured model.
4. Display the response and save both sides of the exchange.
5. If the API call fails, remove the unsent user message from in-memory history.

## Known design trade-off

All prior messages are sent with each request. This is easy to understand, but input size grows with conversation length. Future versions could limit recent messages, summarize old turns, or retrieve selected facts from a database/vector store.

## Robotics extension (future work, not implemented)

A future version could pass validated high-level intents to ROS 2. An LLM should not directly command motors; use deterministic controllers, explicit authorization, and safety checks.
