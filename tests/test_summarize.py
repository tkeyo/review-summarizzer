import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_summarize_reviews() -> None:
    """Test the /summarize endpoint with sample reviews."""
    payload = {
        "reviews": [
            {"review": "Great product!"},
            {"review": "Fast shipping."}
        ]
    }
    response = client.post("/summarize", json=payload)
    assert response.status_code == 200