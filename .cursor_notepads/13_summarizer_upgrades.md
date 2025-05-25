# Review Summarizer Language Support Implementation

## Overview
Add language control to the review summarizer to allow users to specify the output language for summaries.

## Requirements

### API Changes
- Add required `output_language` parameter to the API endpoint
- Support only Czech (`cs`) and Slovak (`sk`) languages
- Validate language parameter using type-safe approach (enum)
- Return metadata about input and output languages in the response

### Response Structure
```python
class SummarizationResponse:
    summary: str
    metadata: dict = {
        "input_language": str,  # "cs" or "sk"
        "output_language": str,  # "cs" or "sk"
        "timestamp": datetime
    }
```

### Implementation Details
- Use enum for language validation
- Maintain same summarization style regardless of language
- Include language metadata in response
- No need for input language detection (input == output)

### Testing Requirements
- Basic test cases for both languages
- Input validation tests
- Response structure validation

### Documentation
- Update API documentation with new parameter
- Provide examples for both languages
- Document supported language codes

## Example Usage
```python
# Request
{
    "reviews": ["review1", "review2"],
    "output_language": "cs"  # or "sk"
}

# Response
{
    "summary": "Summarized text in requested language",
    "metadata": {
        "input_language": "cs",
        "output_language": "cs",
        "timestamp": "2024-03-21T10:00:00Z"
    }
}
```

## Notes
- Internal application - no need for extensive error handling
- No performance optimizations required
- No monitoring or logging needed
- No cultural considerations required