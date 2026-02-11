#Complete Example for Bot-to-Bot System FastAPI + PyTorch
import anthropic
import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

app = FastAPI()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

class BotRequest(BaseModel):
    prompt: str
    image_base64: str = None
    use_thinking: bool = True

@app.post("/bot-communicate")
async def bot_to_bot_communication(request: BotRequest):
    """
    Bot-to-bot communication endpoint using Opus 4.6
    """
    try:
        # Prepare message content
        content = []
        
        if request.image_base64:
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": request.image_base64
                }
            })
        
        content.append({
            "type": "text",
            "text": request.prompt
        })
        
        # Make API call with Opus 4.6
        kwargs = {
            "model": "claude-opus-4-6",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": content}],
        }
        if request.use_thinking:
            kwargs["thinking"] = {"type": "adaptive", "effort": "high"}
        message = client.messages.create(**kwargs)
        
        # Extract response
        response_text = ""
        thinking_text = ""
        
        for block in message.content:
            if block.type == "thinking":
                thinking_text = block.thinking
            elif block.type == "text":
                response_text = block.text
        
        return {
            "response": response_text,
            "thinking": thinking_text,
            "model": "claude-opus-4-6",
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens
            }
        }
        
    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Async streaming example
@app.post("/bot-communicate-stream")
async def bot_communicate_stream(request: BotRequest):
    """
    Streaming bot communication
    """
    async def generate():
        async with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": request.prompt}
            ]
        ) as stream:
            async for text in stream.text_stream:
                yield text
    
    return StreamingResponse(generate(), media_type="text/plain")