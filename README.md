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
# SQL_Query_Craft

Natural-language to SQL demo (FastAPI + Gradio + SQLite) that converts plain English into SQL queries, executes them safely against a sample SQLite database, and returns AI-generated natural-language insights.

## Overview

`SQL_Query_Craft` is a lightweight prototype demonstrating how to build a conversational interface that translates user questions into SQL using an LLM (OpenAI), executes those queries against a read-only database, and summarizes results in human-friendly language. The goal is a developer-friendly starting point for experiments and quick demos — not production-ready infrastructure.

Key features:
- Natural-language → SQL generation using OpenAI
- SQL execution against a local SQLite demo DB (`demo.db`)
- Gradio chat UI with a schema reference and sample prompts
- AI-generated natural-language summaries of query results
- Basic safeguards: SELECT-only validation, single-statement guard

## Architecture

- Frontend: Gradio (`chatbot_ui.py`) — chat tab, schema tab, sample prompts
- Backend: FastAPI (`app.py`) — builds prompts, calls OpenAI, validates SQL, executes queries
- Database: SQLite (`demo.db`) seeded by `seed_db.py`
- Orchestration: `launch.py` starts the API and UI together for local demos

Flow:
1. User enters a question in Gradio (or clicks a sample prompt).
2. Gradio calls the FastAPI `/chat` endpoint with the question.
3. Backend constructs a prompt (schema + examples) and asks OpenAI for a SQL statement.
4. Backend validates the SQL (SELECT-only, single statement), runs it, and retrieves rows.
5. Backend asks OpenAI to summarize the rows in natural language and returns both SQL + summary to the UI.

## Files of interest
- `app.py` — FastAPI backend and OpenAI integration
- `chatbot_ui.py` — Gradio UI (chat + schema + sample prompts)
- `seed_db.py` — creates `demo.db` and seeds with sample data
- `launch.py` — convenience launcher for local development
- `requirements.txt` — Python dependencies
- `.gitignore` — local ignores

## Quickstart (local)

1. Create and activate a virtual environment (recommended):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Seed the demo database:

```powershell
python seed_db.py
```

4. Set your OpenAI API key (PowerShell):

```powershell
$Env:OPENAI_API_KEY="your-key-here"
```

5. Start both services (launcher):

```powershell
python launch.py
```

Open the UI at: http://127.0.0.1:7860

Or run separately:

```powershell
# Terminal 1 (API)
python -m uvicorn app:app --reload --port 8000

# Terminal 2 (UI)
python chatbot_ui.py
```

## Docker

You can run the backend in Docker for easier demos or deployment.

Build the image:

```powershell
docker build -t sql-query-craft:latest .
```

Run the container (remember to set a real OpenAI key for production):

```powershell
docker run -e OPENAI_API_KEY="your-key" -p 8000:8000 sql-query-craft:latest
```

The container exposes the API on port 8000. For local demos, keep the Gradio UI running outside the container and point `API_URL` to `http://host.docker.internal:8000/chat` (Windows/Mac) or the correct host IP on Linux.

## Docker Compose

A `docker-compose.yml` is included to run both the API and Gradio UI together as containers. The services are built from the same image; the UI container is configured to call the API service by its Compose DNS name.

Bring the services up (ensure `OPENAI_API_KEY` is set in your shell or a `.env` file):

```powershell
docker-compose up --build
```

This exposes:
- API: http://localhost:8000/health
- UI:  http://localhost:7860

To stop:

```powershell
docker-compose down
```

Notes:
- For production, use a proper secret store for `OPENAI_API_KEY` and a dedicated database service (Postgres) instead of the built-in SQLite demo DB.
- If you run Docker on Linux, update `API_URL` environment in the `docker-compose.yml` if necessary.

### Local development (live reload)

A `docker-compose.override.yml` is provided to mount the project directory into the containers and enable live reload for the backend. This lets you edit code on your host and see changes immediately without rebuilding the image.

Run with the override (default Compose behavior loads `docker-compose.override.yml` automatically):

```powershell
docker-compose up --build
```

Notes:
- The `api` service runs `uvicorn` with `--reload` so code changes restart the server inside the container.
- The `ui` service runs the Gradio script from the mounted source; some UI frameworks hot-reload automatically, otherwise restart the `ui` container if needed.
- To develop against a host OpenAI key without embedding it in the file, use a local `.env` with `OPENAI_API_KEY=your-key` and run `docker-compose up --build`.

## CI (GitHub Actions)

A workflow is included at `.github/workflows/ci.yml` that:
- installs dependencies and seeds the demo DB,
- runs `pytest`,
- builds the Docker image and performs a simple health check.


## API

- `POST /chat` — body: `{ "question": "..." }`
- response: `{ "sql": "...", "summary": "...", "raw_data": [...] }`

The backend uses a small prompt template (`app.py`) which includes the schema and a few exemplars. The model is asked to return only a single SELECT statement.

## Prompts & Guardrails

- Include the DB schema in the prompt so the model only references valid columns/tables.
- Few-shot examples improve accuracy for common queries.
- Basic validation blocks non-SELECT statements and multiple-statement injections.
- For production, add a SQL parser (e.g., `sqlglot`) and an allowlist of tables/columns.

## Security & Safety Considerations

- Treat model output as untrusted: always validate/parse SQL before execution.
- Use read-only DB credentials and separate replica for analytics queries.
- Enforce timeouts and result limits to avoid long-running queries.
- Log user queries and generated SQL for auditing.
- Consider requiring user confirmation for risky or high-cost queries (e.g., large scans).

## Deployment & Productionization

Suggested improvements to move toward production:

- Swap SQLite for Postgres or another production RDBMS and use a connection pool.
- Add user authentication + RBAC for data access controls.
- Harden SQL validation with `sqlglot` or a proper parser and implement table/column allowlists.
- Containerize with Docker and add CI/CD (GitHub Actions) to lint, test, and build images.
- Add request rate limits and monitoring (Prometheus/Grafana).

## Commercial Use & Product Ideas

This prototype can be extended into various commercial products:

- Dashboard assistant: embed NL→SQL in analytics dashboards to let business users ask questions.
- Data assistant API: provide a hosted service that accepts NL questions and returns results + explanations.
- Integration plugins: Slack/Teams bots that let users query databases conversationally.
- Vertical solutions: domain-specific prompt tuning (finance, healthcare) + prebuilt schema mappings.

Monetization strategies:

- Hosted SaaS with tiered usage, per-query pricing, or subscription.
- Enterprise contracts with on-prem connectors and enhanced security.

## Limitations

- LLM output is probabilistic — expect occasional errors or hallucinations.
- The current prototype lacks strong SQL parsing/validation and authentication.
- Not safe for running against production databases without added guardrails.

## Next steps (recommended)

1. Add `sqlglot` to parse and validate SQL AST before execution.
2. Replace SQLite with Postgres; add migrations and sample data scripts.
3. Add authentication to the API and secure the UI.
4. Add tests for prompt → SQL mapping and end-to-end behavior.
5. Create a GitHub repository, Dockerfile, and CI pipeline.

## License

Add your preferred license (e.g., MIT) before publishing.


