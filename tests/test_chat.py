from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/chat/", json={"query": "What is AI?"})
    assert response.status_code == 200
    json_data = response.json()
    assert "answer" in json_data
