from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import os
import dspy
import concurrent.futures
import asyncio
from app.signatures import SummarizeSignature

# Path to the optimized summarizer
OPTIMIZED_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../prompt/optimized_summarizer.json'))

class Review(BaseModel):
    review: str = Field(..., description="A single user review.")

class SummarizeRequest(BaseModel):
    reviews: List[Review]

class SummarizeResponse(BaseModel):
    summary: str

router = APIRouter()

# Placeholder for OpenAI API key (replace with your actual key or set as env var)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure dspy with the OpenAI model
dspy_lm = dspy.LM('openai/gpt-4o-mini', api_key=OPENAI_API_KEY)
dspy.configure(lm=dspy_lm)

# Load the optimized summarizer
class ReviewSummarizer(dspy.Module):
    def __init__(self):
        self.summarize = dspy.Predict(SummarizeSignature)
    def forward(self, reviews: str):
        return self.summarize(reviews=reviews)

summarizer = ReviewSummarizer()
summarizer.load(path=OPTIMIZED_PATH)

def summarize_reviews_sync(reviews_md: str) -> str:
    """Call the DSPy summarizer synchronously."""
    result = summarizer(reviews=reviews_md)
    return result.summary

@router.post("/summarize", response_model=SummarizeResponse, tags=["summarize"])
async def summarize_reviews(request: SummarizeRequest) -> SummarizeResponse:
    """Summarize a list of user reviews using the optimized DSPy summarizer.

    Args:
        request (SummarizeRequest): The request containing user reviews.

    Returns:
        SummarizeResponse: The summary of the reviews.
    """
    # Format reviews as markdown list
    reviews_md = "\n\n".join(f"# User review {i+1}\n{r.review}" for i, r in enumerate(request.reviews))
    try:
        # Run the blocking LLM call in a thread pool to keep FastAPI async
        with concurrent.futures.ThreadPoolExecutor() as executor:
            summary = await asyncio.get_event_loop().run_in_executor(
                executor, summarize_reviews_sync, reviews_md
            )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM summarization failed: {e}")
    return SummarizeResponse(summary=summary) 