# Implementing Configuration Management

## Problem
Currently, configuration values (API keys, paths) are scattered throughout the codebase and loaded using direct `os.getenv` calls.

## Solution Steps

1. **Create Configuration Module**:
   - Create `app/config.py` using Pydantic's `BaseSettings`
   - Define all configuration parameters
   - Add validation and type checking

2. **Update Existing Code**:
   - Modify `app/llm/review_summarizer.py` to use the new config
   - Remove direct `os.getenv` calls
   - Update any other files using environment variables

## Implementation Details

### 1. Create `app/config.py`:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    """
    Application settings.
    
    Settings are loaded from environment variables.
    A .env file can also be used for local development.
    """
    # API Keys
    OPENAI_API_KEY: str
    
    # Model Paths
    OPTIMIZED_SUMMARIZER_PATH: Path = Path("prompt/optimized_summarizer.json")
    
    # API Settings
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "Review Summarizer"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    
    # Model Settings
    MODEL_NAME: str = "openai/gpt-4.1-nano"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )
    
    @property
    def resolved_summarizer_path(self) -> Path:
        """Get the absolute path to the summarizer model."""
        if not self.OPTIMIZED_SUMMARIZER_PATH.is_absolute():
            project_root = Path(__file__).parent.parent.resolve()
            return project_root / self.OPTIMIZED_SUMMARIZER_PATH
        return self.OPTIMIZED_SUMMARIZER_PATH

# Create singleton instance
settings = Settings()
```

### 2. Update `app/llm/review_summarizer.py`:
```python
from app.config import settings

# Remove direct os.getenv calls
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Remove this

# Use settings instead
_dspy_lm = dspy.LM(settings.MODEL_NAME, api_key=settings.OPENAI_API_KEY)
dspy.configure(lm=_dspy_lm)

# ... rest of the code ...

# Update summarizer loading
summarizer.load(path=str(settings.resolved_summarizer_path))
```

## Environment Variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your-api-key-here
MODEL_NAME=openai/gpt-4.1-nano
```

## Testing
1. Test configuration loading with different environment variables
2. Verify path resolution works correctly
3. Test validation of required fields
4. Ensure .env file loading works

## Notes
- The configuration is now centralized and type-safe
- All settings are validated on startup
- Environment variables can override defaults
- The .env file is optional and should not be committed to version control 