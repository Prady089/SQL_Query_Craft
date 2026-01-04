from fastapi.testclient import TestClient
import os

os.environ.setdefault("OPENAI_API_KEY", "test")

from app import app


def test_health():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
