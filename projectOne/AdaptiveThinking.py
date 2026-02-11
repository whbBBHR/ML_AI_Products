import anthropic
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Initialize the client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Basic request with Opus 4.6
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain quantum computing in simple terms"}
    ]
)

print(message.content[0].text)


# Adaptive thinking - Claude decides when to think deeply
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    thinking={
        "type": "adaptive"  # NEW in 4.6
    },
    messages=[
        {"role": "user", "content": "Solve this complex algorithm problem..."}
    ]
)

# Access thinking process
for block in message.content:
    if block.type == "thinking":
        print(f"Claude's reasoning: {block.thinking}")
    elif block.type == "text":
        print(f"Response: {block.text}")