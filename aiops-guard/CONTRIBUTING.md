# Contributing to AIOpsGuard

First off, thank you for considering contributing to AIOpsGuard! 🎉

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues. When you create a bug report, include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples
- Describe the behavior you observed and what you expected
- Include Python version and OS information

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- Use a clear and descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful
- List any similar features in other projects

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests
3. Ensure the test suite passes
4. Make sure your code follows the style guidelines
5. Write a clear commit message

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/aiops-guard.git
cd aiops-guard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black mypy pytest pytest-cov
```

## Style Guidelines

### Python Style

- Follow PEP 8
- Use Black for code formatting
- Use type hints for all functions
- Write docstrings for all public functions (Google style)

```python
def example_function(param: str) -> int:
    """
    Brief description of function.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
    return len(param)
```

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests

Examples:
```
Add cost projection feature
Fix token counting for Claude models
Update documentation for new API
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

```bash
# Run tests
python test_aiops_guard.py

# Run with pytest (if available)
pytest tests/ -v

# Check coverage
pytest --cov=aiops_guard tests/
```

### Documentation

- Update README.md if needed
- Update USAGE.md for new features
- Add examples for new functionality
- Update ARCHITECTURE.md for design changes

## Project Structure

```
aiops-guard/
├── aiops_guard/          # Main package
│   ├── __init__.py      # Package exports
│   ├── guard.py         # Decorator implementation
│   ├── tracker.py       # Metrics tracking
│   └── models.py        # Data models
├── examples/            # Usage examples
├── docs/                # Documentation
├── tests/               # Test files
└── README.md            # Main documentation
```

## Adding New Features

### Adding a New Model

1. Update `ModelPricing` in `models.py`:
```python
class ModelPricing:
    NEW_MODEL_INPUT: float = 5.00
    NEW_MODEL_OUTPUT: float = 15.00
```

2. Update `get_pricing()` method:
```python
@classmethod
def get_pricing(cls, model_name: str):
    if "new-model" in model_lower:
        return (cls.NEW_MODEL_INPUT, cls.NEW_MODEL_OUTPUT)
```

3. Add tests
4. Update documentation

### Adding New Metrics

1. Update `CallMetrics` dataclass in `models.py`
2. Update tracking logic in `guard.py`
3. Update aggregation in `tracker.py`
4. Update report generation
5. Add tests

## Release Process

1. Update version in `setup.py` and `__init__.py`
2. Update CHANGELOG.md
3. Create release tag
4. Build and publish to PyPI

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
