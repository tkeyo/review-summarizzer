from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from app.llm.review_summarizer import summarize_reviews_sync
from app.llm.language import SupportedLanguage


class Review(BaseModel):
    review: str = Field(..., description="A single user review.")

class SummarizeRequest(BaseModel):
    reviews: List[Review]
    output_language: SupportedLanguage = Field(..., description="The desired output language for the summary.")

class SummarizeResponse(BaseModel):
    summary: str
    metadata: dict = Field(
        default_factory=lambda: {
            "input_language": None,
            "output_language": None,
            "timestamp": datetime.utcnow().isoformat()
        },
        description="Metadata about the summarization request."
    )

router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse, tags=["summarize"])
def summarize_reviews(request: SummarizeRequest) -> SummarizeResponse:
    """Summarize a list of user reviews using the optimized DSPy summarizer.

    Args:
        request (SummarizeRequest): The request containing user reviews and output language.

    Returns:
        SummarizeResponse: The summary of the reviews in the requested language.

    Raises:
        HTTPException: If the LLM service is unavailable or returns an error.
    """
    # Format reviews as markdown list
    reviews_md = "\n\n".join(f"# User review {i+1}\n{r.review}" for i, r in enumerate(request.reviews))
    try:
        summary = summarize_reviews_sync(reviews_md, language=request.output_language)
        return SummarizeResponse(
            summary=summary,
            metadata={
                "input_language": request.output_language.value,
                "output_language": request.output_language.value,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM service unavailable: {str(e)}")