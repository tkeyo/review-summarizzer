import os
import glob
import re
import dspy
from app.llm.language import SupportedLanguage

# Path to the optimized summarizer
OPTIMIZED_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../prompt/v1-optimized_summarizer.json'))

# Placeholder for OpenAI API key (replace with your actual key or set as env var)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure dspy with the OpenAI model
_dspy_lm = dspy.LM('openai/gpt-4.1-nano', api_key=OPENAI_API_KEY)
dspy.configure(lm=_dspy_lm)

class SummarizeSignature(dspy.Signature):
    """Summarize the provided user reviews.
    # Role
    You are an expert review summarizer. Your job is to create top-notch summaries of user reviews.
    # Instructions
    - Summarize the provided reviews
    - Extract key information about what users like, dislike and potential idiosyncracies of the product that users reported
    - Provide the summary in the specified language
    """
    reviews = dspy.InputField(desc="All user reviews as a markdown list.")
    language = dspy.InputField(desc="The language code for the output summary (cs = czech or sk = slovak).")
    summary = dspy.OutputField(desc="A factual summary of user reviews.")

class SummaryStylerSignature(dspy.Signature):
    """Style the provided summary to optimize user engagement.
    # Role
    You are an expert in copy writing - specifically - writing engaging user review summaries.

    # Instructions
    - Make the provided information in the user summaries engaging and informative.
    - Provide the summary in the specified language.
    """
    reviews_summary = dspy.InputField(desc="Summarized user reviews.")
    language = dspy.InputField(desc="The language code for the output summary (cs = czech or sk = slovak).")
    summary = dspy.OutputField(desc="A persuasive summary of the reviews in the specified language.")

class ReviewSummarizer(dspy.Module):
    """DSPy module for summarizing user reviews to maximize purchase intent."""
    def __init__(self) -> None:
        self.summarize = dspy.Predict(SummarizeSignature)
        self.stylize = dspy.Predict(SummaryStylerSignature)

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
        summary = self.summarize(reviews=reviews, language=lang_code)
        stylized_summary = self.stylize(reviews_summary=summary.summary, language=lang_code)
        return stylized_summary

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