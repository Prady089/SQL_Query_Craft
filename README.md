# SQL Query Craft 🔍

**Transform natural language into SQL queries with AI-powered intelligence**

SQL Query Craft is an intelligent chatbot application that bridges the gap between natural language and database queries. Built with modern Python frameworks and powered by OpenAI's language models, it enables users to interact with databases using plain English, eliminating the need for SQL expertise.

<img width="1906" height="824" alt="image" src="https://github.com/user-attachments/assets/430ac914-2c96-401f-a5ce-e4dea5271645" />


## 🎯 Overview

SQL Query Craft is a proof-of-concept application demonstrating the power of Large Language Models (LLMs) in database interaction. It solves a common problem in data analytics: enabling non-technical users to query databases without learning SQL syntax.

**What does it do?**

1. **Accepts natural language questions** — Users type questions like "Show me the top 5 customers by total spending"
2. **Generates SQL queries** — The AI translates the question into a valid SQL SELECT statement
3. **Executes safely** — Query validation and execution against a SQLite database
4. **Returns insights** — Results are displayed both as raw data and AI-generated natural language summaries

**Who is it for?**

- **Developers** exploring LLM-powered database interfaces
- **Data Analysts** prototyping conversational analytics tools
- **Product Teams** evaluating natural language query solutions
- **Educators** teaching AI/database integration concepts
- **Startups** building data accessibility features

---

## ✨ Key Features

### 🤖 AI-Powered Query Generation
- Leverages OpenAI's GPT models (gpt-4o-mini by default) for natural language understanding
- Context-aware SQL generation based on your database schema
- Few-shot learning with example queries for improved accuracy

### 💬 Interactive Chat Interface
- Modern Gradio-based web UI with tabs for Chat and Schema reference
- Pre-built sample prompts for quick exploration
- Real-time SQL query display for transparency and learning
- Natural language summaries of query results

### 🛡️ Safety & Validation
- **SELECT-only enforcement** — Prevents destructive operations (INSERT, UPDATE, DELETE)
- **Single-statement validation** — Blocks SQL injection attempts via multiple statements
- **Error handling** — Graceful failure with user-friendly error messages
- **Query sanitization** — Strips markdown code fences and cleans generated SQL

### 🗃️ Demo Database
- Pre-configured SQLite database with realistic e-commerce schema
- Sample data including customers, products, orders, and order items
- Easily extensible to your own schema and data

### 🚀 Developer-Friendly
- Simple setup with minimal dependencies
- Hot-reload support for rapid development
- Comprehensive test suite with pytest
- CI/CD pipeline with GitHub Actions
- Well-documented codebase with clear separation of concerns

---

## 🎬 Demo & Use Cases

### Example Interactions

**Question:** "How many customers do we have?"
- **Generated SQL:** `SELECT COUNT(*) FROM customers`
- **Summary:** "You currently have 10 customers in the database."

**Question:** "Show me the top 3 products by revenue"
- **Generated SQL:** `SELECT p.name, SUM(oi.quantity * oi.price) as revenue FROM products p JOIN order_items oi ON p.id = oi.product_id GROUP BY p.id ORDER BY revenue DESC LIMIT 3`
- **Summary:** "The top three products by revenue are: Laptop ($4,500), Smartphone ($3,600), and Tablet ($2,100)."

### Real-World Applications

- **Business Intelligence Dashboards** — Add conversational query capabilities to analytics platforms
- **Customer Support Tools** — Enable support teams to query data without SQL knowledge
- **Internal Admin Panels** — Simplify data exploration for non-technical staff
- **Educational Platforms** — Teach SQL concepts through natural language translation
- **Data Exploration Tools** — Rapid prototyping and ad-hoc analysis

---

## 🏗️ Architecture

SQL Query Craft follows a clean three-tier architecture:

```
┌─────────────────┐
│   Gradio UI     │  Frontend: Web interface for user interaction
│ (chatbot_ui.py) │  Port 7860
└────────┬────────┘
         │ HTTP POST
         ▼
┌─────────────────┐
│   FastAPI       │  Backend: API server with business logic
│    (app.py)     │  Port 8000
└────────┬────────┘
         │ SQL Execution
         ▼
┌─────────────────┐
│   SQLite DB     │  Database: Local demo.db file
│   (demo.db)     │
└─────────────────┘

External API Call:
┌─────────────────┐
│  OpenAI API     │  LLM Service: Query generation & summarization
└─────────────────┘
```

### Request Flow

1. **User Input** → User types a question in the Gradio interface
2. **API Request** → Frontend sends `POST /chat` with question payload
3. **Prompt Construction** → Backend builds a prompt with schema + examples + user question
4. **LLM Call #1** → OpenAI generates SQL query from the prompt
5. **Validation** → Backend validates SQL (SELECT-only, single statement)
6. **Execution** → Query runs against SQLite database
7. **LLM Call #2** → OpenAI generates natural language summary of results
8. **Response** → Backend returns `{sql, summary, raw_data}` to frontend
9. **Display** → UI shows SQL code block, summary text, and (optionally) raw data

### Component Responsibilities

| Component | File | Purpose |
|-----------|------|---------|
| **Backend API** | `app.py` | FastAPI server, OpenAI integration, SQL execution |
| **Frontend UI** | `chatbot_ui.py` | Gradio interface with chat and schema tabs |
| **Database Seeder** | `seed_db.py` | Creates and populates demo.db with sample data |
| **Launcher** | `launch.py` | Convenience script to start both API and UI |
| **Tests** | `tests/test_health.py` | Pytest suite for API health checks |

---

## 🛠️ Technology Stack

### Core Technologies

- **Python 3.11+** — Modern Python with type hints and async support
- **FastAPI** — High-performance async web framework for the API layer
- **Gradio** — Rapid UI development framework for ML/AI applications
- **SQLite** — Lightweight embedded database (easily replaceable with PostgreSQL/MySQL)
- **OpenAI API** — GPT models for natural language processing

### Key Libraries

```
fastapi==0.115.6        # Web framework
uvicorn==0.34.0         # ASGI server
gradio==5.9.1           # UI framework
openai==1.59.3          # OpenAI Python client
python-dotenv==1.0.1    # Environment variable management
pytest==8.3.4           # Testing framework
```

### Development Tools

- **Git** — Version control
- **GitHub Actions** — CI/CD automation
- **pytest** — Test runner and framework
- **uvicorn** — Development server with hot-reload

---

## 📁 Project Structure

```
SQL_Query_Craft/
│
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   └── test_health.py          # Health check tests
│
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore patterns
│
├── app.py                      # FastAPI backend (main API logic)
├── chatbot_ui.py               # Gradio frontend (UI)
├── seed_db.py                  # Database initialization script
├── launch.py                   # Convenience launcher
│
├── demo.db                     # SQLite database (generated)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

### File Descriptions

#### `app.py` — Backend API
The core FastAPI application containing:
- `build_prompt(question)` — Constructs LLM prompt with schema and few-shot examples
- `validate_sql(sql)` — Security validation (SELECT-only, single statement)
- `run_sql(sql)` — Executes SQL against demo.db and returns results
- `generate_natural_language_summary(question, rows)` — Creates human-readable summaries
- `/chat` endpoint — Main API endpoint accepting questions and returning SQL + summaries
- `/health` endpoint — Health check for monitoring

#### `chatbot_ui.py` — Frontend Interface
Gradio application featuring:
- Two-tab layout (Chat + Schema)
- Text input for user questions
- Sample prompt buttons for quick testing
- SQL code display block
- Natural language summary output
- Database schema reference tab

#### `seed_db.py` — Database Setup
Creates the demo database with:
- `customers` table — Customer information
- `products` table — Product catalog
- `orders` table — Order headers
- `order_items` table — Order line items
- Sample data for realistic queries

#### `launch.py` — Development Launcher
Convenience script that:
- Starts the FastAPI backend in a subprocess
- Launches the Gradio frontend
- Handles graceful shutdown of both services

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Python 3.11 or higher** installed ([Download Python](https://www.python.org/downloads/))
- **OpenAI API Key** ([Get your key](https://platform.openai.com/api-keys))
- **Git** for cloning the repository ([Download Git](https://git-scm.com/downloads))
- **PowerShell** or **Command Prompt** (Windows) / **Terminal** (Mac/Linux)

### Installation

#### Step 1: Clone the Repository

```powershell
git clone https://github.com/Prady089/SQL_Query_Craft.git
cd SQL_Query_Craft
```

#### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies:

```powershell
# Windows PowerShell
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
py -m venv .venv
.venv\Scripts\activate.bat

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` prefix in your terminal prompt when activated.

#### Step 3: Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

This installs all required packages including FastAPI, Gradio, OpenAI client, and testing tools.

#### Step 4: Initialize the Database

Create and populate the demo database:

```powershell
python seed_db.py
```

Expected output:
```
Database seeded successfully!
Created tables: customers, products, orders, order_items
Inserted sample data for testing.
```

This creates `demo.db` in your project directory.

### Configuration

#### Environment Variables

Create a `.env` file from the template:

```powershell
copy .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
# Required: Your OpenAI API key
OPENAI_API_KEY=sk-your-api-key-here

# Optional: OpenAI model to use (default: gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# Optional: API URL for the Gradio UI (default: http://localhost:8000/chat)
API_URL=http://localhost:8000/chat
```

**Alternative:** Set environment variables directly in your terminal session:

```powershell
# Windows PowerShell
$Env:OPENAI_API_KEY = "sk-your-api-key-here"
$Env:OPENAI_MODEL = "gpt-4o-mini"  # Optional

# Mac/Linux
export OPENAI_API_KEY="sk-your-api-key-here"
export OPENAI_MODEL="gpt-4o-mini"  # Optional
```

### Running the Application

#### Option 1: Quick Start (Recommended)

Use the launcher script to start both services:

```powershell
python launch.py
```

This will:
1. Start the FastAPI backend on http://localhost:8000
2. Start the Gradio UI on http://localhost:7860
3. Automatically open your browser to the UI

**Access the application:** Navigate to http://127.0.0.1:7860

#### Option 2: Run Services Separately

If you need more control or want to debug individually:

**Terminal 1 — Start the API Backend:**

```powershell
python -m uvicorn app:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**Terminal 2 — Start the Gradio UI:**

```powershell
python chatbot_ui.py
```

You should see:
```
Running on local URL:  http://127.0.0.1:7860
```

The `--reload` flag enables hot-reload for development — the server automatically restarts when you modify code.

#### Stopping the Application

- **If using launch.py:** Press `Ctrl+C` in the terminal
- **If running separately:** Press `Ctrl+C` in each terminal window

---

## 📡 API Documentation

### Endpoints

#### `POST /chat`

Main endpoint for natural language to SQL conversion.

**Request:**

```json
{
  "question": "Show me all customers who spent more than $1000"
}
```

**Response:**

```json
{
  "sql": "SELECT c.id, c.name, c.email, SUM(oi.quantity * oi.price) as total_spent FROM customers c JOIN orders o ON c.id = o.customer_id JOIN order_items oi ON o.id = oi.order_id GROUP BY c.id HAVING total_spent > 1000",
  "summary": "There are 3 customers who have spent more than $1000: John Doe ($4,500), Jane Smith ($3,200), and Bob Johnson ($1,800).",
  "raw_data": [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "total_spent": 4500},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "total_spent": 3200},
    {"id": 5, "name": "Bob Johnson", "email": "bob@example.com", "total_spent": 1800}
  ]
}
```

**Error Response:**

```json
{
  "detail": "Invalid SQL: Only SELECT statements are allowed"
}
```

Status codes:
- `200 OK` — Successful query
- `400 Bad Request` — Invalid SQL or validation failure
- `500 Internal Server Error` — OpenAI API error or database error

#### `GET /health`

Health check endpoint for monitoring.

**Response:**

```json
{
  "status": "ok"
}
```

### Using the API with cURL

```powershell
# Test the health endpoint
curl http://localhost:8000/health

# Send a question
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{\"question\": \"How many orders were placed?\"}'
```

### Using the API with Python

```python
import requests

url = "http://localhost:8000/chat"
payload = {"question": "Show me the top 5 products by price"}

response = requests.post(url, json=payload)
data = response.json()

print(f"SQL: {data['sql']}")
print(f"Summary: {data['summary']}")
print(f"Results: {data['raw_data']}")
```

---

## 🗄️ Database Schema

The demo database (`demo.db`) contains an e-commerce schema with four related tables:

### Tables Overview

```sql
-- Customers: Basic customer information
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Products: Product catalog
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT,
    stock INTEGER DEFAULT 0
);

-- Orders: Order headers
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Order Items: Line items for each order
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Sample Data

The seeder script populates:
- **10 customers** with realistic names and emails
- **15 products** across categories (Electronics, Accessories, Home Goods)
- **20 orders** with various statuses (completed, pending, shipped)
- **50+ order items** linking orders to products

### Entity Relationship Diagram

```
customers (1) ─────< (N) orders (1) ─────< (N) order_items (N) >───── (1) products
```

- One customer can have many orders
- One order can have many order items
- One product can appear in many order items

---

## 🔧 How It Works

### Detailed Process Flow

#### 1. Prompt Engineering

When a user asks a question, the backend constructs a carefully crafted prompt:

```python
def build_prompt(question: str) -> str:
    schema = """
    Database Schema:
    - customers (id, name, email, created_at)
    - products (id, name, price, category, stock)
    - orders (id, customer_id, order_date, status)
    - order_items (id, order_id, product_id, quantity, price)
    """
    
    examples = """
    Examples:
    Q: How many customers do we have?
    A: SELECT COUNT(*) FROM customers
    
    Q: Show me the most expensive product
    A: SELECT name, price FROM products ORDER BY price DESC LIMIT 1
    """
    
    return f"{schema}\n{examples}\n\nQuestion: {question}\nSQL:"
```

This provides the LLM with:
- **Schema context** — Available tables and columns
- **Few-shot examples** — Sample question-SQL pairs
- **Clear instruction** — Generate only SQL, no explanations

#### 2. SQL Generation

The prompt is sent to OpenAI's API:

```python
response = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    messages=[
        {"role": "system", "content": "You are a SQL expert. Generate only valid SQL SELECT statements."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.0  # Deterministic output
)
```

#### 3. SQL Cleaning & Validation

The generated SQL undergoes sanitization:

```python
# Remove markdown code fences
sql = sql.replace("```sql", "").replace("```", "").strip()

# Validate: must be SELECT-only
if not sql.upper().startswith("SELECT"):
    raise ValueError("Only SELECT statements allowed")

# Validate: single statement only
if ";" in sql.strip().rstrip(";"):
    raise ValueError("Multiple statements not allowed")
```

#### 4. Query Execution

Validated SQL runs against SQLite:

```python
conn = sqlite3.connect("demo.db")
conn.row_factory = sqlite3.Row  # Return dict-like rows
cursor = conn.execute(sql)
rows = [dict(row) for row in cursor.fetchall()]
conn.close()
```

#### 5. Natural Language Summary

Results are sent back to OpenAI for summarization:

```python
summary_prompt = f"""
Question: {question}
SQL Results: {rows}

Generate a friendly natural language summary of these results.
"""

summary = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    messages=[
        {"role": "system", "content": "You are a helpful data analyst."},
        {"role": "user", "content": summary_prompt}
    ]
).choices[0].message.content
```

#### 6. Response Assembly

All components are packaged and returned:

```python
return {
    "sql": sql,              # The generated query
    "summary": summary,      # Natural language explanation
    "raw_data": rows         # Query results as JSON
}
```

---

## 🧪 Testing

### Running Tests

The project includes a pytest-based test suite for API validation.

**Run all tests:**

```powershell
pytest
```

**Run with verbose output:**

```powershell
pytest -v
```

**Run with coverage:**

```powershell
pip install pytest-cov
pytest --cov=app --cov-report=html
```

**Run quietly (minimal output):**

```powershell
pytest -q
```

### Test Structure

```
tests/
├── conftest.py         # Pytest configuration and fixtures
└── test_health.py      # Health endpoint tests
```

### Example Test

```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_endpoint():
    """Test that the health endpoint returns OK status"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

### Troubleshooting Tests

If pytest cannot import `app`, set `PYTHONPATH`:

```powershell
# Windows PowerShell
$Env:PYTHONPATH = "$PWD"
pytest -q

# Mac/Linux
export PYTHONPATH=$(pwd)
pytest -q
```

Or run from the repository root with:

```powershell
python -m pytest
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The project includes a CI pipeline at `.github/workflows/ci.yml` that automatically:

1. ✅ **Installs dependencies** — Sets up Python 3.11 and pip packages
2. ✅ **Seeds the database** — Runs `seed_db.py` to create test data
3. ✅ **Runs tests** — Executes pytest suite with coverage
4. ✅ **Validates code quality** — Ensures imports and syntax are correct

### Triggering CI

The workflow runs automatically on:
- **Push to `main` branch**
- **Pull requests to `main` branch**

### Manual Trigger

You can also trigger the workflow manually from GitHub Actions tab.

### Viewing Results

1. Navigate to your repository on GitHub
2. Click the "Actions" tab
3. Select the most recent workflow run
4. View logs and test results

### CI Configuration

```yaml
name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test-and-build:
    runs-on: ubuntu-latest
    env:
      PYTHONPATH: ${{ github.workspace }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pytest
      - run: python seed_db.py
      - run: pytest -q
        env:
          OPENAI_API_KEY: test
```

---

## 🔒 Security & Safety

### Current Safeguards

#### 1. SELECT-Only Enforcement
```python
if not sql.upper().startswith("SELECT"):
    raise ValueError("Only SELECT statements are allowed")
```
Prevents destructive operations like `DELETE`, `UPDATE`, `INSERT`, `DROP`.

#### 2. Single Statement Validation
```python
if ";" in sql.strip().rstrip(";"):
    raise ValueError("Multiple statements not allowed")
```
Blocks SQL injection attempts via statement chaining.

#### 3. Error Handling
```python
try:
    rows = run_sql(sql)
except sqlite3.Error as e:
    raise HTTPException(status_code=400, detail=f"SQL execution error: {str(e)}")
```
Catches and safely reports database errors without exposing internals.

### Known Vulnerabilities

⚠️ **This is a demo application. Do NOT use in production without hardening!**

1. **No Authentication** — Anyone can access the API
2. **No Rate Limiting** — Vulnerable to abuse and API cost attacks
3. **Basic SQL Validation** — Regex-based validation can be bypassed
4. **No Query Timeouts** — Long-running queries could DoS the service
5. **Shared Database** — SQLite is not designed for concurrent access
6. **API Key Exposure** — OpenAI key stored in environment variables

### Production Security Checklist

Before deploying to production, implement:

- [ ] **Authentication & Authorization** — Add OAuth2/JWT for user authentication
- [ ] **Role-Based Access Control (RBAC)** — Limit query access by user role
- [ ] **SQL Parser** — Use `sqlglot` or `sqlparse` for robust AST-based validation
- [ ] **Table/Column Allowlist** — Explicitly whitelist queryable tables and columns
- [ ] **Query Timeouts** — Set maximum execution time (e.g., 30 seconds)
- [ ] **Result Set Limits** — Cap maximum rows returned (e.g., 1000 rows)
- [ ] **Rate Limiting** — Implement per-user/IP rate limits (e.g., 10 requests/minute)
- [ ] **Audit Logging** — Log all queries with user ID, timestamp, and results
- [ ] **Read-Only Database User** — Create DB user with SELECT-only permissions
- [ ] **Database Replica** — Query against a read replica, not production master
- [ ] **Input Sanitization** — Validate and sanitize user input before LLM processing
- [ ] **API Key Security** — Use secret management (AWS Secrets Manager, HashiCorp Vault)
- [ ] **HTTPS Only** — Enforce TLS/SSL for all API communication
- [ ] **CORS Configuration** — Restrict allowed origins for API access
- [ ] **Content Security Policy** — Add CSP headers to prevent XSS

### Example: Adding Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "your-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return credentials.credentials

@app.post("/chat", dependencies=[Depends(verify_token)])
async def chat(request: QuestionRequest):
    # Protected endpoint
    ...
```

### Example: Adding sqlglot Validation

```python
import sqlglot

def validate_sql_advanced(sql: str) -> bool:
    try:
        # Parse SQL into AST
        parsed = sqlglot.parse_one(sql, dialect="sqlite")
        
        # Check it's a SELECT statement
        if not isinstance(parsed, sqlglot.exp.Select):
            raise ValueError("Only SELECT queries allowed")
        
        # Extract all table references
        tables = [table.name for table in parsed.find_all(sqlglot.exp.Table)]
        allowed_tables = {"customers", "products", "orders", "order_items"}
        
        # Validate tables are in allowlist
        for table in tables:
            if table not in allowed_tables:
                raise ValueError(f"Access to table '{table}' not allowed")
        
        return True
    except sqlglot.errors.ParseError as e:
        raise ValueError(f"Invalid SQL syntax: {e}")
```

---

## 🚢 Production Deployment

### Recommended Architecture for Production

```
┌─────────────┐
│   Load      │
│  Balancer   │  (AWS ALB, Nginx)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   API       │
│  Servers    │  (Kubernetes, ECS, App Engine)
│  (3+ pods)  │
└──────┬──────┘
       │
       ├─────────────┐
       ▼             ▼
┌─────────────┐ ┌─────────────┐
│  PostgreSQL │ │   OpenAI    │
│   Replica   │ │     API     │
│  (read-only)│ │             │
└─────────────┘ └─────────────┘
```

### Deployment Steps

#### 1. Database Migration

Replace SQLite with PostgreSQL/MySQL:

```python
# Replace in app.py
import psycopg2
from psycopg2.extras import RealDictCursor

def run_sql(sql: str):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows
```

#### 2. Environment Configuration

Use proper secret management:

```bash
# AWS Secrets Manager
aws secretsmanager get-secret-value --secret-id prod/sql-query-craft/openai-key

# Kubernetes Secrets
kubectl create secret generic api-secrets \
  --from-literal=OPENAI_API_KEY=sk-... \
  --from-literal=DB_PASSWORD=...
```

#### 3. Containerization (Optional)

Since Docker files were removed, you can create a simple production Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```powershell
docker build -t sql-query-craft:latest .
docker run -e OPENAI_API_KEY=sk-... -p 8000:8000 sql-query-craft:latest
```

#### 4. Cloud Platform Deployment

**AWS Elastic Beanstalk:**

```powershell
eb init sql-query-craft --region us-east-1 --platform python-3.11
eb create prod-env
eb deploy
```

**Google Cloud Run:**

```powershell
gcloud run deploy sql-query-craft \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=sk-...
```

**Azure App Service:**

```powershell
az webapp up --name sql-query-craft \
  --runtime PYTHON:3.11 \
  --sku B1
```

#### 5. Monitoring & Observability

Add application monitoring:

```python
# Example: Add Prometheus metrics
from prometheus_client import Counter, Histogram, make_asgi_app

query_counter = Counter('queries_total', 'Total queries processed')
query_duration = Histogram('query_duration_seconds', 'Query execution time')

@app.post("/chat")
async def chat(request: QuestionRequest):
    query_counter.inc()
    with query_duration.time():
        # ... existing logic ...
```

Mount metrics endpoint:

```python
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

### Scaling Considerations

- **Horizontal Scaling** — Run multiple API instances behind a load balancer
- **Connection Pooling** — Use SQLAlchemy or psycopg2 pool for DB connections
- **Caching** — Cache common queries with Redis to reduce LLM API calls
- **Async Processing** — Use background workers for long-running queries
- **CDN** — Serve static Gradio UI assets via CDN

---

## ⚠️ Limitations & Caveats

### Technical Limitations

1. **LLM Hallucinations** — The AI may generate syntactically correct but semantically wrong SQL
2. **Schema Awareness** — Model only knows about schema provided in prompt; cannot auto-discover changes
3. **Complex Queries** — Struggles with very complex joins, subqueries, or window functions
4. **Ambiguity Handling** — Cannot ask clarifying questions; makes assumptions
5. **Performance** — Each query requires 2 LLM API calls (generation + summarization)

### Functional Limitations

1. **No Write Operations** — Cannot INSERT, UPDATE, DELETE data (by design for safety)
2. **No Database Admin** — Cannot CREATE/ALTER/DROP tables or manage schema
3. **No Transactions** — Each query is independent; no multi-statement transactions
4. **No Stored Procedures** — Cannot call or create database functions/procedures
5. **No Advanced SQL** — Limited support for CTEs, recursive queries, or vendor-specific features

### Production Readiness

This is a **prototype/demo application**. It lacks:

- Authentication and authorization
- Comprehensive input validation
- Production-grade error handling
- Performance optimization (query caching, connection pooling)
- Monitoring and alerting
- Data privacy controls
- Compliance features (audit logs, data retention)

**Do not deploy this application to production environments without significant hardening.**

---

## 🗺️ Roadmap

### Short-Term (Next 2-4 Weeks)

- [ ] Add `sqlglot` for robust SQL parsing and validation
- [ ] Implement query result caching with Redis
- [ ] Add request/response logging for debugging
- [ ] Create more comprehensive test suite (integration tests)
- [ ] Support for multiple database connections (PostgreSQL, MySQL)
- [ ] Add user feedback mechanism (thumbs up/down on queries)

### Mid-Term (1-3 Months)

- [ ] Implement JWT-based authentication
- [ ] Add role-based access control (RBAC)
- [ ] Create admin dashboard for monitoring query activity
- [ ] Support for custom schema uploads (connect your own database)
- [ ] Query history and favoriting
- [ ] Export results (CSV, Excel, JSON)
- [ ] Scheduled/saved queries

### Long-Term (3-6 Months)

- [ ] Multi-tenancy support for SaaS deployment
- [ ] Advanced analytics (query performance metrics, cost tracking)
- [ ] Natural language chart generation (NL → SQL → Visualization)
- [ ] Slack/Teams bot integration
- [ ] Streaming results for large datasets
- [ ] Support for NoSQL databases (MongoDB NL queries)
- [ ] Fine-tuned model for SQL generation (better accuracy, lower cost)

### Research & Experiments

- [ ] Compare different LLMs (Claude, Llama, Gemini) for SQL generation accuracy
- [ ] Experiment with chain-of-thought prompting for complex queries
- [ ] Implement self-correction loop (validate → fix → retry)
- [ ] Add semantic search over database content
- [ ] Explore vector embeddings for schema/query similarity matching

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues

If you find a bug or have a feature request:

1. Check [existing issues](https://github.com/Prady089/SQL_Query_Craft/issues) to avoid duplicates
2. Open a new issue with:
   - Clear, descriptive title
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Your environment (OS, Python version, etc.)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add/update tests as needed
5. Ensure tests pass (`pytest`)
6. Commit with clear messages (`git commit -m 'Add amazing feature'`)
7. Push to your fork (`git push origin feature/amazing-feature`)
8. Open a Pull Request with description of changes

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions/classes
- Write tests for new features
- Update README if adding new functionality
- Keep commits atomic and well-described

### Code Review Process

- PRs require at least one approval
- CI must pass (tests, linting)
- Maintainer will review within 3-5 business days

---

## 💼 Commercial Opportunities

SQL Query Craft can be extended into viable commercial products:

### Product Ideas

#### 1. **BI Dashboard Assistant**
Embed natural language query into existing BI tools (Tableau, Power BI, Looker).

**Revenue Model:** Per-seat SaaS subscription ($15-50/user/month)

#### 2. **Data Analyst Copilot**
AI assistant for data teams that generates SQL, explains queries, and suggests optimizations.

**Revenue Model:** Team plans ($199-999/month for 5-50 users)

#### 3. **Customer-Facing Analytics**
White-label solution for SaaS companies to offer NL querying to end customers.

**Revenue Model:** Usage-based pricing ($0.10-0.50 per query) + platform fee

#### 4. **Slack/Teams Data Bot**
Conversational bot for querying company databases from chat platforms.

**Revenue Model:** Flat rate per workspace ($99-499/month)

#### 5. **Industry-Specific Solutions**
Vertical SaaS for healthcare (EHR queries), finance (trading data), retail (inventory).

**Revenue Model:** Enterprise contracts ($10k-100k/year) + custom integrations

### Monetization Strategies

| Strategy | Description | Target Customer | Pricing Range |
|----------|-------------|-----------------|---------------|
| **SaaS Subscription** | Hosted multi-tenant platform | SMBs, Mid-Market | $49-999/month |
| **Enterprise Licensing** | On-premise deployment with support | Large Enterprises | $50k-500k/year |
| **Usage-Based** | Pay per query or API call | Developers, Startups | $0.01-1.00/query |
| **Freemium** | Free tier + paid pro features | Individual users | $0-49/month |
| **White-Label** | Licensed to resellers/integrators | System Integrators | Rev share or flat fee |

### Market Opportunity

- **Total Addressable Market (TAM):** $10B+ (Business Intelligence + Data Analytics market)
- **Target Segments:** 
  - Data analysts tired of repetitive SQL queries
  - Business users wanting self-service analytics
  - Companies reducing dependency on BI teams
- **Competitive Advantage:** 
  - AI-native solution (not retrofit into legacy tools)
  - Open-source foundation builds trust
  - Extensible architecture for custom integrations

### Next Steps for Commercialization

1. **Validate Product-Market Fit** — Interview 20-50 potential customers
2. **Build MVP Features** — Authentication, multi-tenancy, billing integration
3. **Pricing Research** — Run pricing surveys to find optimal price points
4. **Go-to-Market** — Content marketing (blog, tutorials) + Product Hunt launch
5. **Pilot Program** — Offer free/discounted access to 5-10 design partners
6. **Fundraising** — Seed round ($500k-2M) to scale team and marketing

---

## 📄 License

This project is provided as-is for educational and evaluation purposes.

**Before deploying or commercializing**, add an appropriate open-source license:

- **MIT License** — Permissive, allows commercial use
- **Apache 2.0** — Includes patent grant
- **GPL v3** — Copyleft, requires derivative works to be open-source
- **Proprietary** — Closed source with custom terms

To add a license, create a `LICENSE` file in the repository root.

**Recommended for this project:** MIT License (developer-friendly, widely adopted)

---

## 📞 Support & Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/Prady089/SQL_Query_Craft/issues)
- **Discussions:** [Ask questions or share ideas](https://github.com/Prady089/SQL_Query_Craft/discussions)
- **Email:** Contact repository owner for commercial inquiries

---

## 🙏 Acknowledgments

Built with:
- **FastAPI** by Sebastián Ramírez
- **Gradio** by Hugging Face
- **OpenAI API** for GPT models
- **SQLite** by D. Richard Hipp

Inspired by the growing need for democratized data access and natural language interfaces.

---

**⭐ If you find this project useful, please star the repository!**

---

*Last Updated: January 2026*
