# 🛡️ AIOpsGuard

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Lightweight Python library for monitoring LLM calls with automatic cost tracking**

[Features](#-features) •
[Quick Start](#-quick-start) •
[Why This Matters](#-why-this-matters) •
[Documentation](#-documentation) •
[Examples](#-examples)

</div>

---

## 📸 Live Output

See [docs/SCREENSHOTS.md](docs/SCREENSHOTS.md) for complete output examples with beautiful Rich formatting.

*Add a screenshot by running `python test_aiops_guard.py` and capturing the terminal output*

## 🎯 Why This Matters

In production environments, **unmonitored AI calls are a financial risk**:

- 💸 A single misconfigured loop can cost thousands in API fees
- 🔍 Without tracking, you can't optimize model selection or prompt efficiency  
- 📊 Teams need visibility into which agents/features drive costs
- ⚠️ Silent failures in LLM calls can go unnoticed for days

**AIOpsGuard solves this** by providing zero-config monitoring that tracks every call, calculates real costs, and alerts you to issues before they impact your budget.

### Real-World Impact

```python
# Before: No visibility into costs
response = openai.ChatCompletion.create(...)  # How much did this cost? 🤷

# After: Full transparency
@AIOpsGuard(agent_name="CustomerSupport", model_name="gpt-4")
def handle_support_ticket(ticket: str) -> str:
    return openai.ChatCompletion.create(...)  # ✅ Tracked, costed, monitored
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Zero-config decorator** | Just wrap your functions |
| 💰 **Automatic cost tracking** | Real-time USD cost calculation |
| ⏱️ **Performance monitoring** | Execution time tracking |
| 📊 **Beautiful reports** | Rich terminal output with tables |
| 🔢 **Token counting** | Accurate via tiktoken |
| 🤖 **Multi-agent support** | Track multiple agents |
| 📈 **Cost projections** | Daily/monthly estimates |
| 🎨 **Type-safe** | Full type hints |
| 🔌 **Framework agnostic** | Works with any LLM library |
| ⚡ **Async support** | Native async/await compatibility |
| 🛡️ **Production-ready** | Exception handling & fallbacks |

## 🚀 Quick Start

### Installation

```bash
pip install tiktoken rich
```

### Basic Usage

```python
from aiops_guard import AIOpsGuard, get_global_tracker

# Decorate your LLM function
@AIOpsGuard(agent_name="my_agent", model_name="gpt-4")
def call_llm(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Use normally
result = call_llm("What is the meaning of life?")

# Print beautiful summary
tracker = get_global_tracker()
tracker.print_summary()
```

### Output Example

```
╭──────────────────────────────────────────────────────────────────╮
│ 🛡️  AIOpsGuard Summary Report                                    │
╰──────────────────────────────────────────────────────────────────╯

                  📊 Overall Statistics
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                         ┃                Value ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Calls                    │                   10 │
│ Total Cost                     │              $0.0016 │
│ Success Rate                   │                90.0% │
│ Total Tokens                   │                  162 │
│ Avg Time/Call                  │                0.05s │
└────────────────────────────────┴──────────────────────┘

        💰 Cost Projections
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Period          ┃ Estimated Cost ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Per Day         │        $272.15 │
│ Per Month (30d) │       $8164.49 │
└─────────────────┴────────────────┘
```

See [docs/SCREENSHOTS.md](docs/SCREENSHOTS.md) for complete output examples including per-agent and per-model breakdowns.

## 📸 Screenshots

### Basic Output
![Output Example](docs/SCREENSHOTS.md)

Complete examples with per-agent and per-model breakdowns available in [docs/SCREENSHOTS.md](docs/SCREENSHOTS.md).

## 🔧 Supported Models

<table>
<tr>
<td>

**OpenAI**
- GPT-4
- GPT-4 Turbo
- GPT-3.5 Turbo

</td>
<td>

**Anthropic**
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3 Haiku

</td>
</tr>
</table>

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Usage Guide](USAGE.md) | Detailed usage instructions |
| [Architecture](docs/ARCHITECTURE.md) | System design and architecture |
| [Screenshots](docs/SCREENSHOTS.md) | Sample outputs and reports |
| [Contributing](CONTRIBUTING.md) | Contribution guidelines |
| [Changelog](CHANGELOG.md) | Version history |

## 🎯 Examples

### Async Support

```python
import asyncio
from aiops_guard import AIOpsGuard

@AIOpsGuard(agent_name="AsyncAgent", model_name="gpt-4")
async def async_llm_call(prompt: str) -> str:
    response = await openai.ChatCompletion.acreate(...)
    return response

# Works seamlessly with async/await
result = await async_llm_call("Analyze this data")
```

### Track Multiple Agents

```python
@AIOpsGuard(agent_name="Researcher", model_name="gpt-4")
def research(query: str) -> str:
    return llm_research(query)

@AIOpsGuard(agent_name="Writer", model_name="gpt-3.5-turbo")
def write(content: str) -> str:
    return llm_write(content)

# Compare performance
tracker.print_summary(show_agents=True)
```

### Custom Tracker

```python
from aiops_guard import CallTracker

my_tracker = CallTracker()

@AIOpsGuard(agent_name="Agent1", tracker=my_tracker)
def my_function(prompt: str) -> str:
    return response
```

### Export Data

```python
# Get summary
summary = tracker.get_summary()

# Export to JSON
import json
data = tracker.export_to_dict()
with open('metrics.json', 'w') as f:
    json.dump(data, f, indent=2)
```

More examples in [examples/](examples/) directory:
- [basic_example.py](examples/basic_example.py) - Simple usage
- [multi_agent_example.py](examples/multi_agent_example.py) - Multiple agents
- [async_example.py](examples/async_example.py) - Async/await support

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Application                      │
│                                                         │
│  @AIOpsGuard(agent_name="Agent1", model="gpt-4")       │
│  def my_llm_call(prompt: str) -> str:                  │
│      return llm_response                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 AIOpsGuard Layer                        │
│                                                         │
│  Decorator → Token Counter → Cost Calculator           │
│                     ↓                                   │
│              Metrics Builder                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              CallTracker (Storage)                      │
│                                                         │
│  • Store metrics  • Aggregate stats  • Summaries       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Rich Console (Reporting)                     │
│                                                         │
│  • Format tables  • Generate reports  • Terminal output │
└─────────────────────────────────────────────────────────┘
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## 📊 What Gets Tracked

- ✅ Input/Output tokens
- ✅ USD costs (input + output)
- ✅ Execution time
- ✅ Success/failure status
- ✅ Per-agent statistics
- ✅ Per-model statistics
- ✅ Cost projections

## 🎯 Use Cases

| Use Case | Description |
|----------|-------------|
| 💻 **Development** | Monitor costs during development |
| 🚀 **Production** | Track real-time costs in production |
| 💰 **Optimization** | Compare and optimize model costs |
| 🤖 **Multi-Agent** | Track individual agent performance |

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

```bash
# Clone repository
git clone https://github.com/yourusername/aiops-guard.git
cd aiops-guard

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_aiops_guard.py

# Run examples
python examples/basic_example.py
```

## 📝 Development

### Running Tests

```bash
python test_aiops_guard.py
```

### Testing Async Support

```bash
python examples/async_example.py
```

### Code Style

```bash
black aiops_guard/
mypy aiops_guard/
```

## 🗺️ Roadmap

- [x] Sync function support
- [x] Async function support
- [x] Exception handling & fallbacks
- [ ] Database persistence
- [ ] Web dashboard
- [ ] Alert thresholds
- [ ] Custom pricing
- [ ] Batch operations
- [ ] Historical analysis
- [ ] PyPI package

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [tiktoken](https://github.com/openai/tiktoken) - OpenAI's token counting
- [rich](https://github.com/Textualize/rich) - Beautiful terminal formatting

Created by **暇格 (Xiage)** - [GitHub](https://github.com/zzzflame)

## 📞 Contact & Support

- 🐛 [Issues](https://github.com/zzzflame/aiops-guard/issues)
- 💬 [Discussions](https://github.com/zzzflame/aiops-guard/discussions)
- 📧 Email: 38222540@qq.com
- 💬 WeChat: xiuzhendaonanxing

## 👨‍💻 Author

**暇格 (Xiage)**

- GitHub: [@zzzflame](https://github.com/zzzflame)
- Email: 38222540@qq.com
- WeChat: xiuzhendaonanxing

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=zzzflame/aiops-guard&type=Date)](https://star-history.com/#zzzflame/aiops-guard&Date)

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/zzzflame/aiops-guard?style=social)
![GitHub forks](https://img.shields.io/github/forks/zzzflame/aiops-guard?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/zzzflame/aiops-guard?style=social)

---

<div align="center">

**Made with ❤️ by 暇格 (Xiage) for the LLM community**

[⬆ Back to Top](#️-aiopsguard)

</div>
