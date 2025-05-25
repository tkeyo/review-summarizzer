import os
import dspy
from app.llm.language import SupportedLanguage

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
    - Provide the summary in the specified language
    """
    reviews = dspy.InputField(desc="All user reviews as a markdown list.")
    language = dspy.InputField(desc="The language code for the output summary (cs = czech or sk = slovak).")
    summary = dspy.OutputField(desc="A persuasive summary of the reviews in the specified language.")


class ReviewSummarizer(dspy.Module):
    """DSPy module for summarizing user reviews to maximize purchase intent."""
    def __init__(self) -> None:
        self.summarize = dspy.Predict(SummarizeSignature)

    def forward(self, reviews: str, language: str | SupportedLanguage) -> dspy.Prediction:
        """
        Summarize the provided reviews in the specified language.

        Args:
            reviews (str): All user reviews as a markdown list.
            language (str | SupportedLanguage): The desired output language code.

        Returns:
            dspy.Prediction: The prediction containing the summary.
        """
        # Handle both string and enum inputs
        lang_code = language.value if isinstance(language, SupportedLanguage) else language
        return self.summarize(reviews=reviews, language=lang_code)

# Singleton instance of the summarizer
summarizer = ReviewSummarizer()
summarizer.load(path=OPTIMIZED_PATH)

def summarize_reviews_sync(reviews_md: str, language: SupportedLanguage) -> str:
    """
    Call the DSPy summarizer synchronously.

    Args:
        reviews_md (str): All user reviews as a markdown list.
        language (SupportedLanguage): The desired output language.

    Returns:
        str: The persuasive summary of the reviews in the specified language.
    """
    result = summarizer(reviews=reviews_md, language=language)
    return result.summary 