# Implementing Asynchronous Calls

## Problem
The current implementation in `app/routers/summarize.py` uses a synchronous call to `summarize_reviews_sync` within an async endpoint, which blocks the FastAPI event loop.

## Solution Steps

1. **Modify `app/llm/review_summarizer.py`**:
   - Add new async function `summarize_reviews_async`
   - Use `fastapi.concurrency.run_in_threadpool` for the DSPy call
   - Keep the sync version for testing purposes

2. **Update `app/routers/summarize.py`**:
   - Change the import to use the async version
   - Update the endpoint to await the async call
   - Add proper error handling and logging

## Implementation Details

### 1. Update `app/llm/review_summarizer.py`:
```python
from fastapi.concurrency import run_in_threadpool
from typing import Awaitable

# ... existing imports and code ...

async def summarize_reviews_async(reviews_md: str) -> str:
    """
    Call the DSPy summarizer asynchronously using a thread pool.

    Args:
        reviews_md (str): All user reviews as a markdown list.

    Returns:
        str: The persuasive summary of the reviews.
    """
    result: dspy.Prediction = await run_in_threadpool(summarizer, reviews=reviews_md)
    return result.summary
```

### 2. Update `app/routers/summarize.py`:
```python
from app.llm.review_summarizer import summarize_reviews_async  # Update import

@router.post("/summarize", response_model=SummarizeResponse, tags=["summarize"])
async def summarize_reviews(request: SummarizeRequest) -> SummarizeResponse:
    reviews_md = "\n\n".join(f"# User review {i+1}\n{r.review}" 
                            for i, r in enumerate(request.reviews))
    try:
        summary = await summarize_reviews_async(reviews_md)  # Use await
    except Exception as e:
        raise HTTPException(status_code=502, 
                          detail=f"LLM summarization failed: {e}")
    return SummarizeResponse(summary=summary)
```

## Testing
1. Test the async endpoint with multiple concurrent requests
2. Verify that the event loop isn't blocked
3. Ensure error handling works as expected

## Notes
- The async implementation allows the application to handle multiple requests concurrently
- The thread pool prevents blocking the event loop during the LLM call
- Error handling remains important for production reliability 