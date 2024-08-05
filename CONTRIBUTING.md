# Contributing to AuditAgent

Thank you for your interest in contributing to AuditAgent! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/AuditAgent.git
   cd AuditAgent
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable names

Format code before committing:
```bash
black src/ examples/ tests/
```

## Testing

Run tests before submitting a pull request:
```bash
pytest tests/ -v --cov=src
```

## Submitting Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Run tests and linting
4. Commit with descriptive messages
5. Push to your fork
6. Create a pull request

## Areas for Contribution

- New vulnerability detectors
- Additional analysis tool integrations
- Performance improvements
- Documentation enhancements
- Bug fixes
- Test coverage improvements

## Questions?

Open an issue for discussion before starting work on major features.
