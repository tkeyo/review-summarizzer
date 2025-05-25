# Review Summarizer MVP

A production-ready FastAPI web service that summarizes user reviews using a Large Language Model (LLM) via [DSPy](https://github.com/stanfordnlp/dspy). This project is designed for clarity, modularity, and ease of use, making it ideal for learning and extension.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the Service](#running-the-service)
- [API Endpoints](#api-endpoints)
- [Example Usage](#example-usage)
- [Testing](#testing)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

---

## Features
- **Summarize Reviews:** Accepts a list of user reviews and returns a persuasive summary designed to maximize purchase intent.
- **Health Check:** Simple endpoint to verify the service is running.
- **Async & Threaded:** Efficiently handles LLM calls without blocking the server.
- **Modular Design:** Clean separation of API, logic, and configuration.
- **Type Safety:** Uses Pydantic models for request/response validation.
- **Test Coverage:** Includes example tests for endpoints.

---

## Project Structure

```
app/
  main.py           # FastAPI app initialization and router inclusion
  signatures.py     # DSPy signature for summarization
  routers/
    health.py       # /health endpoint
    summarize.py    # /summarize endpoint (LLM logic)
requirements.txt    # Python dependencies
README.md           # Project documentation
.env                # (Not committed) API keys and secrets
/tests              # Pytest-based unit tests
```

---

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd cursor-test
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or, for development:
   pip install fastapi uvicorn pytest python-dotenv dspy
   ```
4. **Set up environment variables:**
   - Create a `.env` file in the project root:
     ```env
     OPENAI_API_KEY=sk-...YOUR-API-KEY-HERE...
     ```
   - **Never commit your real API keys to version control!**

---

## Running the Service

Start the FastAPI server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

- Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation (Swagger UI).

---

## API Endpoints

### 1. Health Check
- **GET** `/health`
- **Purpose:** Verify the service is running.
- **Response:** `{ "status": "ok" }`

### 2. Summarize Reviews
- **POST** `/summarize`
- **Purpose:** Summarize a list of user reviews using an LLM.
- **Request Body:**
  ```json
  {
    "reviews": [
      { "review": "Great product!" },
      { "review": "Fast shipping." }
    ]
  }
  ```
- **Response:**
  ```json
  {
    "summary": "Great product! Fast shipping."
  }
  ```
- **Error Handling:** Returns HTTP 502 if the LLM call fails.

#### How Summarization Works
- Reviews are formatted as a markdown list.
- The [DSPy](https://github.com/stanfordnlp/dspy) library sends the reviews to an OpenAI LLM (e.g., GPT-4o-mini) using your API key.
- The LLM is prompted to create a persuasive summary to maximize purchase intent.
- The LLM call is run in a thread pool to keep the API responsive.

---

## Example Usage

### Health Check
```bash
curl http://127.0.0.1:8000/health
```

### Summarize Reviews
```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H 'Content-Type: application/json' \
  -d '{"reviews": [{"review": "Great product!"}, {"review": "Fast shipping."}]}'
```

---

## Testing

This project uses `pytest` for unit testing. Example tests are provided for both endpoints.

Run all tests:
```bash
pytest
```

Example test for `/summarize` (see `tests/test_summarize.py`):
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_summarize_reviews():
    payload = {"reviews": [
        {"review": "Great product!"},
        {"review": "Fast shipping."}
    ]}
    response = client.post("/summarize", json=payload)
    assert response.status_code == 200
    assert "summary" in response.json()
```

---

## Environment Variables

- **OPENAI_API_KEY**: Your OpenAI API key for LLM access. Loaded automatically from `.env` using `python-dotenv`.

---

## Troubleshooting
- **Invalid API Key:** Ensure your `.env` file is present and contains a valid `OPENAI_API_KEY`.
- **Dependency Issues:** Double-check your virtual environment and installed packages.
- **LLM Errors:** If the summarization fails, check your API key and network connection. The API will return a 502 error if the LLM call fails.

---

## Contributing
- Follow PEP 8 and use type annotations.
- Add/modify tests for new features.
- Document your code with clear docstrings.

---

## License
MIT License 