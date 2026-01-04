# SQL_Query_Craft

Natural-language to SQL demo (FastAPI + Gradio + SQLite). Convert plain English to SQL and get AI-generated insights.

## Setup
1) Install deps (ideally in a venv):
```
pip install -r requirements.txt
```
2) Create the sample database:
```
python seed_db.py
```
3) Export your OpenAI key (Windows PowerShell):
```
$Env:OPENAI_API_KEY="your-key"
```
(Optional) pick a model via `OPENAI_MODEL` (default: gpt-4o-mini).

## Run (Single Command)
```
python launch.py
```
This starts both the API (port 8000) and Gradio UI (port 7860). Open http://127.0.0.1:7860 in your browser.

Press Ctrl+C to stop both services.

## Run (Manual - Two Terminals)
### Terminal 1: API
```
uvicorn app:app --reload --port 8000
```
Health check: http://localhost:8000/health

### Terminal 2: Gradio client
```
python chatbot_ui.py
```
Set `API_URL` env var if the API is on a different host/port.

## Notes
- The prompt enforces SELECT-only and adds LIMIT 50 if missing.
- Basic guards block DDL/DML and multiple statements; harden with a real SQL parser for production.
- Schema is in `seed_db.py` and mirrored in `app.py` prompt. Sync both if you change the schema.
