# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-03-13

### Added
- ⚡ **Async/await support** - Native support for asynchronous functions
- 🛡️ **Exception handling** - Robust error handling for unknown models and edge cases
- 📝 **Production-ready** - Fallback pricing for unknown models prevents crashes
- 📚 **Async examples** - New `examples/async_example.py` demonstrating async usage
- 🎯 **"Why This Matters"** section in README explaining production monitoring importance
- 🧪 **Exception handling tests** - New `test_exception_handling.py` for edge cases

### Changed
- Improved `ModelPricing.get_pricing()` with try-except for unknown models
- Enhanced `calculate_cost()` with exception handling to prevent crashes
- Updated README with real-world impact examples and use cases
- Reorganized README with "Why This Matters" section at the top
- Added async support to feature list
- Updated roadmap to reflect completed features

### Fixed
- Prevents crashes when using unsupported model names
- Graceful fallback to GPT-3.5 pricing for unknown models
- Handles empty or malformed model names without errors

## [0.1.0] - 2024-03-11

### Added
- Initial release of AIOpsGuard
- Class-based decorator for LLM call monitoring
- Functional decorator support
- Token counting using tiktoken
- Automatic cost calculation for OpenAI and Anthropic models
- Execution time tracking
- Multi-agent support
- Beautiful terminal reports using Rich library
- Per-agent statistics
- Per-model statistics
- Cost projections (hourly, daily, monthly, yearly)
- Error handling and failure tracking
- Global tracker instance
- Custom tracker support
- Export to dictionary functionality
- Comprehensive documentation
- Usage examples
- Architecture documentation
- Type hints throughout codebase

### Supported Models
- OpenAI: GPT-4, GPT-4 Turbo, GPT-3.5 Turbo (all variants)
- Anthropic: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku

### Documentation
- README.md with quick start guide
- USAGE.md with detailed usage instructions
- ARCHITECTURE.md with system design
- OUTPUT_EXAMPLE.md with sample outputs
- Basic and multi-agent examples
- Contributing guidelines
- MIT License

## [Unreleased]

### Planned Features
- [ ] Database persistence
- [ ] Web dashboard
- [ ] Alert thresholds
- [ ] Custom pricing configuration
- [ ] Batch operation support
- [ ] Historical trend analysis
- [ ] Export to JSON/CSV
- [ ] Integration with monitoring tools
- [ ] PyPI package publication

---

[0.2.0]: https://github.com/zzzflame/aiops-guard/releases/tag/v0.2.0
[0.1.0]: https://github.com/zzzflame/aiops-guard/releases/tag/v0.1.0
