# 🛡️ AIOpsGuard

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Lightweight Python library for monitoring LLM calls with automatic cost tracking**

[Features](#-features) •
[Quick Start](#-quick-start) •
[Documentation](#-documentation) •
[Examples](#-examples) •
[Contributing](#-contributing)

</div>

---

## 🎯 Why AIOpsGuard?

Stop wondering how much your LLM calls cost! AIOpsGuard provides:

- 💰 **Real-time cost tracking** - Know exactly what you're spending
- 📊 **Beautiful reports** - Terminal dashboards with Rich
- ⚡ **Zero overhead** - Minimal performance impact
- 🎯 **Zero config** - Just add a decorator
- 🤖 **Multi-agent ready** - Track multiple agents separately

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

More examples in [examples/](examples/) directory.

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

### Code Style

```bash
black aiops_guard/
mypy aiops_guard/
```

## 🗺️ Roadmap

- [ ] Async function support
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

## 📞 Support

- 🐛 [Issues](https://github.com/yourusername/aiops-guard/issues)
- 💬 [Discussions](https://github.com/yourusername/aiops-guard/discussions)
- 📧 Email: support@aiopsguard.dev

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/aiops-guard&type=Date)](https://star-history.com/#yourusername/aiops-guard&Date)

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/aiops-guard?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/aiops-guard?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/aiops-guard?style=social)

---

<div align="center">

**Made with ❤️ for the LLM community**

[⬆ Back to Top](#️-aiopsguard)

</div>
