import dspy

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