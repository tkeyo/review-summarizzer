from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import os
import asyncio
from app.signatures.review_summarizer import summarize_reviews_sync


class Review(BaseModel):
    review: str = Field(..., description="A single user review.")

class SummarizeRequest(BaseModel):
    reviews: List[Review]

class SummarizeResponse(BaseModel):
    summary: str

router = APIRouter()


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
        summary = summarize_reviews_sync(reviews_md)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM summarization failed: {e}")
    return SummarizeResponse(summary=summary)