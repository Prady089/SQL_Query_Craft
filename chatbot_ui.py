import os
import requests
import gradio as gr

API_URL = os.environ.get("API_URL", "http://localhost:8000/chat")

SCHEMA_MD = """
### Schema (SQLite)

**customers**
- id INTEGER (PK)
- name TEXT
- email TEXT
- city TEXT

**products**
- id INTEGER (PK)
- name TEXT
- price REAL

**orders**
- id INTEGER (PK)
- customer_id INTEGER (FK -> customers.id)
- total REAL
- created_at TEXT (ISO8601)

**order_items**
- id INTEGER (PK)
- order_id INTEGER (FK -> orders.id)
- product_id INTEGER (FK -> products.id)
- quantity INTEGER
- line_total REAL
"""


SAMPLE_PROMPTS = [
    "Top 5 customers by total spend",
    "Which product sold the most in the last 3 months",
    "Revenue by city",
    "Average order value",
    "Orders placed in the last 30 days",
]


def ask(question: str) -> tuple[str, str]:
    resp = requests.post(API_URL, json={"question": question})
    if resp.status_code != 200:
        return f"Error: {resp.text}", ""
    data = resp.json()
    sql = data.get("sql", "")
    summary = data.get("summary", "No summary available")
    return sql, summary


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Natural Language to SQL") as demo:
        gr.Markdown("""# Natural Language to SQL
Prompted with OpenAI → SQLite demo. Chat on the first tab; schema reference on the second.""")
        with gr.Tabs():
            with gr.Tab("Chat"):
                question_input = gr.Textbox(lines=2, label="Question", placeholder="e.g., top 5 customers by spend")
                
                gr.Markdown("### Sample Prompts")
                with gr.Row():
                    btn1 = gr.Button(SAMPLE_PROMPTS[0])
                    btn2 = gr.Button(SAMPLE_PROMPTS[1])
                    btn3 = gr.Button(SAMPLE_PROMPTS[2])
                with gr.Row():
                    btn4 = gr.Button(SAMPLE_PROMPTS[3])
                    btn5 = gr.Button(SAMPLE_PROMPTS[4])
                
                # Place Ask button directly below sample prompts for easy access
                submit_btn = gr.Button("Ask", variant="primary")
                sql_output = gr.Code(label="Generated SQL", language="sql", lines=4)
                summary_output = gr.Textbox(lines=10, label="Insights (Natural Language)")
                
                # Wire up sample prompt buttons
                btn1.click(fn=ask, inputs=gr.Textbox(value=SAMPLE_PROMPTS[0], visible=False), outputs=[sql_output, summary_output])
                btn2.click(fn=ask, inputs=gr.Textbox(value=SAMPLE_PROMPTS[1], visible=False), outputs=[sql_output, summary_output])
                btn3.click(fn=ask, inputs=gr.Textbox(value=SAMPLE_PROMPTS[2], visible=False), outputs=[sql_output, summary_output])
                btn4.click(fn=ask, inputs=gr.Textbox(value=SAMPLE_PROMPTS[3], visible=False), outputs=[sql_output, summary_output])
                btn5.click(fn=ask, inputs=gr.Textbox(value=SAMPLE_PROMPTS[4], visible=False), outputs=[sql_output, summary_output])
                
                # Wire up Ask button and Enter key
                submit_btn.click(fn=ask, inputs=question_input, outputs=[sql_output, summary_output])
                question_input.submit(fn=ask, inputs=question_input, outputs=[sql_output, summary_output])
            with gr.Tab("Schema"):
                gr.Markdown(SCHEMA_MD)
    return demo


def main():
    ui = build_ui()
    ui.launch()


if __name__ == "__main__":
    main()
