# projectOne - Claude Opus 4.6 API Examples

Python scripts demonstrating the Anthropic Claude Opus 4.6 API, including basic requests, adaptive thinking, and a FastAPI bot-to-bot communication server.

## Scripts

| File | Description |
|------|-------------|
| `Python.py` | Basic API request — sends a prompt and prints the response |
| `AdaptiveThinking.py` | Demonstrates adaptive thinking mode where Claude decides when to reason deeply |
| `Bot2Bot.py` | FastAPI server with bot-to-bot communication endpoints (standard + streaming) |

## Setup

### Prerequisites
- Python 3.9+
- Anthropic API key

### Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic python-dotenv fastapi uvicorn
```

### Environment variables
Create a `.env` file in the repo root (`ML_AI_Products/.env`):
```
ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

### Run standalone scripts
```bash
.venv/bin/python Python.py
.venv/bin/python AdaptiveThinking.py
```

### Run the Bot2Bot server
```bash
.venv/bin/uvicorn Bot2Bot:app --reload --port 8000
```

### API endpoints

**POST /bot-communicate** — Standard request
```bash
curl -X POST http://127.0.0.1:8000/bot-communicate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello", "use_thinking": false}'
```

**POST /bot-communicate-stream** — Streaming response
```bash
curl -X POST http://127.0.0.1:8000/bot-communicate-stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'
```

Interactive API docs available at: `http://127.0.0.1:8000/docs`
