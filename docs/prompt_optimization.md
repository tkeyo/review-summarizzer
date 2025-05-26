# Prompt Optimization and Review Summarization

This document provides detailed information about the prompt optimization process and the review summarization implementation in the project, focusing on the conceptual framework and technical details.

## Review Summarizer Module (`app/llm/review_summarizer.py`)

The review summarizer is implemented using DSPy, a framework that separates interface ("what should the LM do?") from implementation ("how do we tell it to do that?"). This separation is achieved through DSPy signatures, which define the structure and behavior of LLM interactions.

### Core Components

1. **SummarizeSignature**
   - A DSPy signature that defines the input/output structure for review summarization
   - Inputs:
     - `reviews`: User reviews as a markdown list
     - `language`: Target language code (cs = Czech, sk = Slovak)
   - Output:
     - `summary`: A factual summary of the reviews
   - Role and Instructions:
     - Expert review summarizer role
     - Instructions for extracting key information
     - Guidelines for handling likes, dislikes, and product idiosyncrasies

2. **SummaryStylerSignature**
   - A DSPy signature for making summaries more engaging
   - Inputs:
     - `reviews_summary`: The factual summary from SummarizeSignature
     - `language`: Target language code
   - Output:
     - `summary`: A persuasive, engaging summary
   - Role and Instructions:
     - Expert copywriter role
     - Focus on engagement and informativeness
     - Language-specific styling guidelines

3. **ReviewSummarizer**
   - Main DSPy module that combines summarization and styling
   - Uses a two-step process:
     1. Generate factual summary
     2. Style the summary for engagement
   - Supports both string and enum language inputs
   - Loads optimized prompts from `prompt/v1-optimized_summarizer.json`

### Usage Example

```python
from app.llm.review_summarizer import summarize_reviews_sync
from app.llm.language import SupportedLanguage

reviews = """
- Great product quality
- Fast shipping
- Could be cheaper
"""

summary = summarize_reviews_sync(reviews, SupportedLanguage.CZECH)
```

## Prompt Optimization Process

The optimization process uses DSPy's MIPROv2 optimizer, which implements a sophisticated approach to prompt engineering through systematic experimentation and evaluation.

### Optimization Framework

1. **Signature-Based Design**
   - DSPy signatures define the interface between components
   - Adapters map signatures to prompts
   - Optimization occurs at the signature level
   - Multi-stage modules can be optimized end-to-end

2. **Training Data Structure**
   - Example format:
     ```json
     {
       "reviews": [
         "Room was clean and spacious.",
         "Excellent location, but noisy at night.",
         "Staff was helpful and check-in was quick."
       ],
       "language": "cs",
       "reference": "Uživatelé oceňují čistotu hotelu. Přilehlé ulice jsou hlučné."
     }
     ```
   - Diverse examples across domains
   - Language-specific reference summaries
   - Balanced positive and negative aspects

3. **Judge Metric Implementation**
   - Uses LLM as judge for evaluation
   - Output: 0 or 1

### Optimization Steps

1. **Bootstrap Few-Shot Examples**
   - Generates multiple sets of demonstrations through iterative refinement
   - Each demonstration set is created by:
     - Running the current program on training examples
     - Evaluating outputs using the judge metric
     - Selecting successful examples for few-shot learning
   - These demonstrations help the model understand the task better

2. **Instruction Generation and Refinement**
   - Creates instruction candidates by analyzing:
     - Successful few-shot examples
     - Program structure and signatures
     - Task requirements and constraints
   - Each instruction candidate is evaluated on:
     - Training set performance
     - Validation set performance
     - Judge's binary evaluation (0 or 1)
   - Instructions are refined based on performance

3. **Program Optimization**
   - The optimizer tunes the entire program end-to-end
   - All intermediate modules are optimized simultaneously
   - Optimization process:
     - Evaluates the final output of the system
     - Adjusts prompts and instructions
     - Maintains checkpointing for resumable optimization
     - Tracks performance metrics and costs

4. **Iterative Refinement**
   - The process is inherently iterative:
     - Start with initial program structure
     - Run optimization
     - Evaluate results
     - Adjust program, data, or metrics
     - Repeat until desired performance is achieved
   - Key aspects to iterate on:
     - Program structure and complexity
     - Training data quality and quantity
     - Evaluation metrics
     - Optimization parameters

### Technical Implementation

1. **Optimizer Configuration**
   ```python
   optimizer = MIPROv2(
       num_trials=20,
       num_fewshot_candidates=6,
       num_instruct_candidates=3,
       valset_size=3
   )
   ```

2. **Checkpointing**
   - Saves optimization progress
   - Allows resuming from previous state
   - Maintains history of successful prompts

3. **Observability**
   - Tracks:
     - Prompt evolution
     - Performance metrics
     - Cost management
     - Success/failure rates

## Best Practices

1. **Prompt Engineering**
   - Keep prompts clear and specific
   - Include examples in the target language
   - Consider cultural nuances
   - Use role-based instructions
   - Maintain consistent formatting

2. **Optimization Strategy**
   - Start with diverse training data
   - Use systematic evaluation
   - Implement checkpointing
   - Monitor cost and performance
   - Iterate based on results

3. **Deployment Considerations**
   - Version control prompt templates
   - Monitor performance in production
   - Implement fallback strategies
   - Track usage patterns
   - Regular re-optimization

## References

- [DSPy Documentation](https://dspy.ai/)
- [DSPy Optimizers](https://dspy.ai/learn/optimization/optimizers/)
- [DSPy Classification Tutorial](https://dspy.ai/tutorials/classification_finetuning/)
- [DSPy Roadmap](https://dspy.ai/roadmap/) 