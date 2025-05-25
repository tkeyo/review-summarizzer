import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.llm.language import SupportedLanguage

client = TestClient(app)

@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="OPENAI_API_KEY not set; skipping live LLM test.")
def test_summarize_reviews() -> None:
    """Test the /summarize endpoint with sample reviews."""
    payload = {
        "reviews": [
            {"review": "Great product!"},
            {"review": "Fast shipping."}
        ],
        "output_language": "cs"
    }
    response = client.post("/summarize", json=payload)
    assert response.status_code == 200
    assert "summary" in response.json()
    assert "metadata" in response.json()
    assert response.json()["metadata"]["output_language"] == "cs"

@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="OPENAI_API_KEY not set; skipping live LLM test.")
def test_summarize_reviews_czech() -> None:
    """Test the /summarize endpoint with Czech language."""
    payload = {
        "reviews": [
            {"review": "Great product!"},
            {"review": "Fast shipping."}
        ],
        "output_language": "cs"
    }
    response = client.post("/summarize", json=payload)
    assert response.status_code == 200
    assert "summary" in response.json()
    assert "metadata" in response.json()
    assert response.json()["metadata"]["output_language"] == "cs"

@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="OPENAI_API_KEY not set; skipping live LLM test.")
def test_summarize_reviews_slovak() -> None:
    """Test the /summarize endpoint with Slovak language."""
    payload = {
        "reviews": [
            {"review": "Great product!"},
            {"review": "Fast shipping."}
        ],
        "output_language": "sk"
    }
    response = client.post("/summarize", json=payload)
    assert response.status_code == 200
    assert "summary" in response.json()
    assert "metadata" in response.json()
    assert response.json()["metadata"]["output_language"] == "sk"

def test_summarize_reviews_invalid_language() -> None:
    """Test the /summarize endpoint with invalid language."""
    payload = {
        "reviews": [
            {"review": "Great product!"},
            {"review": "Fast shipping."}
        ],
        "output_language": "invalid"
    }
    response = client.post("/summarize", json=payload)
    assert response.status_code == 422  # Validation error

def test_summarize_reviews_empty() -> None:
    """Test the /summarize endpoint with empty reviews list."""
    payload = {
        "reviews": [],
        "output_language": "cs"
    }
    response = client.post("/summarize", json=payload)
    assert response.status_code == 200
    assert "summary" in response.json()
    assert "metadata" in response.json()