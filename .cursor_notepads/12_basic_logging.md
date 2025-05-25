# Implementing Basic Logging

## Problem
The application currently lacks structured logging, making it difficult to:
- Monitor application behavior
- Debug issues
- Track API usage
- Monitor performance

## Solution Steps

1. **Create Logging Configuration**:
   - Set up logging configuration in `app/main.py`
   - Define log formats and handlers
   - Configure log levels

2. **Implement Logging in Key Areas**:
   - Add logging to API endpoints
   - Log LLM operations
   - Add request/response logging
   - Log configuration loading

## Implementation Details

### 1. Create `app/logger.py`:
```python
import logging
import sys
from pathlib import Path
from typing import Any, Dict

def setup_logging(
    log_level: str = "INFO",
    log_file: Path | None = None,
) -> None:
    """
    Set up logging configuration for the application.
    
    Args:
        log_level: The logging level to use
        log_file: Optional path to log file
    """
    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create handlers
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=handlers,
        force=True
    )

    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
```

### 2. Update `app/main.py`:
```python
from fastapi import FastAPI
from app.routers import health, summarize
from app.logger import setup_logging
from app.config import settings

# Set up logging
setup_logging(
    log_level=settings.LOG_LEVEL,
    log_file=settings.LOG_FILE
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Review Summarizer API")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Review Summarizer API")

app.include_router(health.router)
app.include_router(summarize.router)
```

### 3. Update `app/routers/summarize.py`:
```python
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.llm.review_summarizer import summarize_reviews_async

logger = logging.getLogger(__name__)

# ... existing model definitions ...

@router.post("/summarize", response_model=SummarizeResponse, tags=["summarize"])
async def summarize_reviews(request: SummarizeRequest) -> SummarizeResponse:
    """Summarize a list of user reviews using the optimized DSPy summarizer."""
    logger.info(f"Received summarization request with {len(request.reviews)} reviews")
    
    reviews_md = "\n\n".join(f"# User review {i+1}\n{r.review}" 
                            for i, r in enumerate(request.reviews))
    try:
        logger.debug("Calling LLM summarizer")
        summary = await summarize_reviews_async(reviews_md)
        logger.info("Successfully generated summary")
        return SummarizeResponse(summary=summary)
    except Exception as e:
        logger.error(f"LLM summarization failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=502, 
                          detail=f"LLM summarization failed: {e}")
```

### 4. Update `app/llm/review_summarizer.py`:
```python
import logging
from app.config import settings

logger = logging.getLogger(__name__)

# ... existing imports and code ...

async def summarize_reviews_async(reviews_md: str) -> str:
    """Call the DSPy summarizer asynchronously."""
    logger.debug("Starting async summarization")
    try:
        result: dspy.Prediction = await run_in_threadpool(summarizer, reviews=reviews_md)
        logger.debug("Successfully completed summarization")
        return result.summary
    except Exception as e:
        logger.error(f"Error in summarization: {str(e)}", exc_info=True)
        raise
```

## Configuration Updates

Add to `app/config.py`:
```python
class Settings(BaseSettings):
    # ... existing settings ...
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path | None = None
```

## Testing

1. **Test Log Levels**:
```python
# In your test file
import logging
from app.logger import setup_logging

def test_log_levels():
    setup_logging(log_level="DEBUG")
    logger = logging.getLogger(__name__)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
```

2. **Test File Logging**:
```python
from pathlib import Path

def test_file_logging():
    log_file = Path("test.log")
    setup_logging(log_file=log_file)
    logger = logging.getLogger(__name__)
    logger.info("Test message")
    assert log_file.exists()
    log_file.unlink()  # Clean up
```

## Notes
- Log levels should be configurable via environment variables
- Consider adding log rotation for file logging
- Add structured logging (JSON format) for production
- Consider adding request ID tracking for better traceability
- Add performance metrics logging
- Consider integrating with a log aggregation service 