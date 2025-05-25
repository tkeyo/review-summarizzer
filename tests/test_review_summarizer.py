import os
import pytest
from unittest.mock import patch, MagicMock
from app.llm import review_summarizer
from app.llm.language import SupportedLanguage

def test_review_summarizer_instantiation() -> None:
    """Test that ReviewSummarizer can be instantiated and has a summarize attribute."""
    module = review_summarizer.ReviewSummarizer()
    assert hasattr(module, 'summarize')
    assert callable(module.forward)

@patch('app.llm.review_summarizer.summarizer')
def test_summarize_reviews_sync(mock_summarizer: MagicMock) -> None:
    """Test summarize_reviews_sync returns the summary from the DSPy module."""
    mock_result = MagicMock()
    mock_result.summary = "This is a summary."
    mock_summarizer.return_value = mock_result
    reviews_md = "# User review 1\nGreat!"
    summary = review_summarizer.summarize_reviews_sync(reviews_md, SupportedLanguage.CZECH)
    assert summary == "This is a summary."
    mock_summarizer.assert_called_once_with(reviews=reviews_md, language=SupportedLanguage.CZECH)

@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="OPENAI_API_KEY not set; skipping live LLM test.")
def test_summarize_reviews_sync_llm() -> None:
    """Test summarize_reviews_sync with a real LLM call (requires OPENAI_API_KEY)."""
    reviews_md = "# User review 1\nThis product is fantastic!"
    summary = review_summarizer.summarize_reviews_sync(reviews_md, SupportedLanguage.CZECH)
    assert isinstance(summary, str)
    assert len(summary.strip()) > 0