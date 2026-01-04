import os
import sqlite3
import textwrap
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

DB_PATH = "demo.db"
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is required.")

client = OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI(title="NL to SQL Demo")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCHEMA = """
Tables:
customers(id INTEGER PK, name TEXT, email TEXT, city TEXT)
products(id INTEGER PK, name TEXT, price REAL)
orders(id INTEGER PK, customer_id INTEGER FK->customers.id, total REAL, created_at TEXT ISO8601)
order_items(id INTEGER PK, order_id INTEGER FK->orders.id, product_id INTEGER FK->products.id, quantity INTEGER, line_total REAL)
"""

FEW_SHOTS = """
User: top 5 customers by total spend
SQL: SELECT c.name, SUM(o.total) AS spend\n     FROM customers c JOIN orders o ON o.customer_id = c.id\n     GROUP BY c.name\n     ORDER BY spend DESC\n     LIMIT 5;

User: orders placed in the last 30 days
SQL: SELECT * FROM orders\n     WHERE date(created_at) >= date('now', '-30 day')\n     ORDER BY date(created_at) DESC\n     LIMIT 50;

User: average item quantity per order
SQL: SELECT ROUND(AVG(oi.quantity), 2) AS avg_qty\n     FROM order_items oi;

User: revenue by city
SQL: SELECT c.city, ROUND(SUM(o.total), 2) AS revenue\n     FROM customers c JOIN orders o ON o.customer_id = c.id\n     GROUP BY c.city\n     ORDER BY revenue DESC\n     LIMIT 10;
"""

class Query(BaseModel):
    question: str


def build_prompt(question: str) -> str:
    return textwrap.dedent(
        f"""
        You generate a single SQLite SELECT statement for analytics over the provided schema.
        Rules:
        - One statement only; no DDL/DML.
        - Use SQLite syntax.
        - Include a LIMIT clause (at most 50 rows).
        - Do not guess columns/tables not in schema.
        - If a question is ambiguous, pick the simplest reasonable interpretation.
        - Output ONLY the SQL statement, nothing else.

        Schema:
        {SCHEMA}

        Examples:
        {FEW_SHOTS}

        User: {question}
        SQL:
        """
    )


def validate_sql(sql: str) -> None:
    upper = sql.upper()
    banned = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "ATTACH", "PRAGMA"]
    if any(word in upper for word in banned):
        raise ValueError("Only SELECT queries are allowed.")
    # crude multi-statement guard: allow trailing semicolon only
    body = sql.strip()
    if body.count(";") > 1:
        raise ValueError("Multiple statements are not allowed.")

def generate_natural_language_summary(question: str, rows: list) -> str:
    """Convert raw SQL results to natural language insights."""
    if not rows:
        return "No data found matching your query."
    
    # Format rows as readable text
    rows_text = "\n".join([str(row) for row in rows])
    
    summary_prompt = f"""
    User asked: {question}
    
    Query results:
    {rows_text}
    
    Provide a clear, concise natural language summary of these results that highlights key insights. 
    Make it conversational and easy to understand. Do not repeat the raw data format."""
    
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": summary_prompt}],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()


def run_sql(sql: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(sql)
        rows = cur.fetchall()
    return [dict(row) for row in rows]


@app.post("/chat")
def chat(q: Query):
    prompt = build_prompt(q.question)
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        sql_raw = resp.choices[0].message.content.strip()
        # Remove markdown code fences if present
        if sql_raw.startswith("```"):
            lines = sql_raw.split("\n")
            sql_raw = "\n".join(lines[1:-1]) if len(lines) > 2 else sql_raw
            sql_raw = sql_raw.strip()
        
        # Clean up: remove trailing semicolon, add one back
        sql = sql_raw.rstrip().rstrip(";") + ";"
        
        validate_sql(sql)
        rows = run_sql(sql)
        
        # Generate natural language summary
        summary = generate_natural_language_summary(q.question, rows)
        
    except HTTPException:
        raise
    except Exception as exc:
        # Include the generated SQL in error for debugging
        sql_debug = sql if 'sql' in locals() else sql_raw if 'sql_raw' in locals() else 'N/A'
        raise HTTPException(status_code=400, detail=f"SQL error: {exc}\nGenerated SQL: {sql_debug}") from exc
    return {"sql": sql, "summary": summary, "raw_data": rows}


@app.get("/health")
def health():
    return {"status": "ok", "db": os.path.exists(DB_PATH)}
