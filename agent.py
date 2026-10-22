"""Command-line AI agent with persistent JSON conversation memory."""

import os
from openai import OpenAI
from dotenv import load_dotenv

from memory_store import load_memory, save_memory, clear_memory

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")
MEMORY_FILE = os.getenv("MEMORY_FILE", "memory.json")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "300"))

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Use the conversation history to maintain "
    "context. Be clear, accurate, and honest. If you are unsure, say so."
)


def create_client() -> OpenAI:
    """Create an OpenAI-compatible client configured for OpenRouter."""
    if not API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Copy .env.example to .env "
            "and add your OpenRouter API key."
        )
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY,
    )


def main() -> None:
    try:
        client = create_client()
    except Exception as exc:
        print(f"Configuration error: {exc}")
        return

    conversation = load_memory(MEMORY_FILE)

    print("=" * 38)
    print("       MY AI AGENT WITH MEMORY")
    print("=" * 38)
    print(f"Model: {MODEL}")
    print("Commands: 'exit' to quit, 'clear' to erase chat memory.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAgent: Goodbye!")
            break

        if not user_input:
            continue

        command = user_input.lower()
        if command == "exit":
            print("Agent: Goodbye!")
            break

        if command == "clear":
            conversation = []
            clear_memory(MEMORY_FILE)
            print("Agent: Chat memory cleared.\n")
            continue

        conversation.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *conversation,
                ],
                max_tokens=MAX_TOKENS,
            )
            answer = response.choices[0].message.content or ""
            conversation.append({"role": "assistant", "content": answer})
            save_memory(conversation, MEMORY_FILE)
            print(f"\nAgent: {answer}\n")

        except Exception as exc:
            # Do not store a user turn if the API request failed.
            conversation.pop()
            print(f"\nAPI error: {exc}")
            print(
                "Check your API key, model availability, internet connection, "
                "and OpenRouter credits/limits.\n"
            )


if __name__ == "__main__":
    main()
