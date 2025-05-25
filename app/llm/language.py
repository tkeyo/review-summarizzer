from enum import Enum

class SupportedLanguage(str, Enum):
    """Supported languages for review summarization."""
    CZECH = "cs"
    SLOVAK = "sk" 