from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app
import pytest

client = TestClient(app)

def test_chat():
  data = {"message": "안녕"}
  response = client.post(
        "/chat",
        json=data,
    )
  assert response.status_code == 200
  content = response.json()
  assert "code" in content
  assert "data" in content

def test_chat_message_empty():
  data = {"message": ""}
  response = client.post(
        "/chat",
        json=data,
    )
  assert response.status_code == 404
  content = response.json()
  assert "code" in content
  assert "msg" in content

@pytest.mark.asyncio
async def test_chat_async():
  async with AsyncClient(base_url="http://localhost:8000") as ac:
    data = {"message": "안녕"}
    response = await ac.post(
          "/chat",
          json=data,
      )
    assert response.status_code == 200
    content = response.json()
    assert "code" in content
    assert "data" in content