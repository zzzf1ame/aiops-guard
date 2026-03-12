# 📖 AIOpsGuard Usage Guide

## 🎯 Overview

AIOpsGuard is a lightweight Python library for monitoring LLM calls with automatic cost tracking and performance metrics.

## 🚀 Installation

```bash
pip install tiktoken rich
```

## 📚 Basic Usage

### 1. Simple Decorator

```python
from aiops_guard import AIOpsGuard, get_global_tracker

@AIOpsGuard(agent_name="MyAgent", model_name="gpt-4")
def my_llm_function(prompt: str) -> str:
    # Your LLM call here
    return llm_response

# Use normally
result = my_llm_function("Hello, AI!")

# Print summary
tracker = get_global_tracker()
tracker.print_summary()
```

### 2. Functional Decorator

```python
from aiops_guard import track_llm_call

@track_llm_call(agent_name="Agent1", model_name="gpt-3.5-turbo")
def another_function(prompt: str) -> str:
    return response
```

### 3. Class Methods

```python
class MyAgent:
    @AIOpsGuard(agent_name="MyAgent", model_name="gpt-4")
    def process(self, text: str) -> str:
        return processed_text
```

## 🎨 Features

### Supported Models

- OpenAI: gpt-4, gpt-4-turbo, gpt-3.5-turbo
- Anthropic: claude-3-opus, claude-3-sonnet, claude-3-haiku
- Auto-detection for model variants

### Metrics Tracked

- Input/Output tokens
- USD cost (real-time pricing)
- Execution time
- Success/failure status
- Per-agent statistics
- Per-model statistics

### Summary Reports

```python
tracker = get_global_tracker()

# Full report with tables
tracker.print_summary(show_agents=True, show_models=True)

# Get raw data
summary = tracker.get_summary()
agent_stats = tracker.get_agent_summary()
model_stats = tracker.get_model_summary()
```

## 💡 Advanced Usage

### Custom Tracker

```python
from aiops_guard import CallTracker, AIOpsGuard

# Create custom tracker
my_tracker = CallTracker()

@AIOpsGuard(
    agent_name="Agent1",
    model_name="gpt-4",
    tracker=my_tracker
)
def my_function(prompt: str) -> str:
    return response

# Use custom tracker
my_tracker.print_summary()
```

### Export Data

```python
# Export to dictionary
data = tracker.export_to_dict()

# Save to JSON
import json
with open('metrics.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Clear Tracking

```python
# Clear all tracked calls
tracker.clear()
```

## 📊 Output Examples

The library generates beautiful terminal reports with:
- Overall statistics table
- Per-agent breakdown
- Per-model breakdown
- Cost projections (hourly/daily/monthly/yearly)

## 🔧 Integration Examples

### With OpenAI

```python
import openai
from aiops_guard import AIOpsGuard

@AIOpsGuard(agent_name="ChatBot", model_name="gpt-4")
def chat(message: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content
```

### With LangChain

```python
from langchain.llms import OpenAI
from aiops_guard import AIOpsGuard

@AIOpsGuard(agent_name="LangChainAgent", model_name="gpt-3.5-turbo")
def langchain_call(prompt: str) -> str:
    llm = OpenAI(model_name="gpt-3.5-turbo")
    return llm(prompt)
```

## 🎯 Best Practices

1. Use descriptive agent names
2. Specify correct model names for accurate pricing
3. Print summaries periodically in long-running applications
4. Export metrics for analysis
5. Monitor cost projections

## 📈 Cost Optimization Tips

- Use the summary to identify expensive agents
- Compare model costs in the per-model breakdown
- Monitor the cost projections
- Optimize prompts based on token usage

## 🐛 Troubleshooting

### Import Errors
```bash
pip install --upgrade tiktoken rich
```

### Token Counting Issues
The library uses tiktoken for accurate token counting. If a model is not recognized, it falls back to cl100k_base encoding.

### Cost Calculation
Costs are based on current pricing as of the library version. Update the ModelPricing class for custom pricing.

## 📄 License

MIT License - See LICENSE file for details
