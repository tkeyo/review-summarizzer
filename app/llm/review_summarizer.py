import os
import dspy

# Path to the optimized summarizer
OPTIMIZED_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../prompt/optimized_summarizer.json'))

# Placeholder for OpenAI API key (replace with your actual key or set as env var)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure dspy with the OpenAI model
_dspy_lm = dspy.LM('openai/gpt-4.1-nano', api_key=OPENAI_API_KEY)
dspy.configure(lm=_dspy_lm)

class SummarizeSignature(dspy.Signature):
    """Summarize the provided user reviews to maximize purchase intent.
    # Role
    You are an expert review summarizer. You know what makes people tick and buy when they read a review summary.
    # Instructions
    - Summarize the provided reviews
    - Adjust the format so that people are more likely to purchase
    """
    reviews = dspy.InputField(desc="All user reviews as a markdown list.")
    summary = dspy.OutputField(desc="A persuasive summary of the reviews.")


class ReviewSummarizer(dspy.Module):
    """DSPy module for summarizing user reviews to maximize purchase intent."""
    def __init__(self) -> None:
        self.summarize = dspy.Predict(SummarizeSignature)

    def forward(self, reviews: str) -> dspy.Prediction:
        """
        Summarize the provided reviews.

        Args:
            reviews (str): All user reviews as a markdown list.

        Returns:
            dspy.Prediction: The prediction containing the summary.
        """
        return self.summarize(reviews=reviews)

# Singleton instance of the summarizer
summarizer = ReviewSummarizer()
summarizer.load(path=OPTIMIZED_PATH)

def summarize_reviews_sync(reviews_md: str) -> str:
    """
    Call the DSPy summarizer synchronously.

    Args:
        reviews_md (str): All user reviews as a markdown list.

    Returns:
        str: The persuasive summary of the reviews.
    """
    result = summarizer(reviews=reviews_md)
    return result.summary 