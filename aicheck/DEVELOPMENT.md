# Development Guide

This guide covers development, testing, and publishing of the `aicheck` package.

## Package Structure

```
aicheck/
├── src/aicheck/           # Source code
│   ├── __init__.py       # Package initialization
│   ├── core.py           # Core calculation logic
│   ├── cli.py            # Command-line interface
│   └── py.typed          # PEP 561 marker for type hints
├── tests/                # Test suite
│   ├── __init__.py
│   └── test_core.py      # Core function tests
├── pyproject.toml        # Package configuration
├── pytest.ini            # Pytest configuration
├── ruff.toml            # Ruff linter/formatter configuration
├── requirements-development.piptools  # Dev dependencies
├── LICENSE              # MIT License
└── README.md            # User documentation
```

## Setup for Development

1. **Clone and navigate to the package**:
   ```bash
   cd aicheck
   ```

2. **Install in editable mode with uv**:
   ```bash
   uv pip install -e .
   ```

3. **Install development dependencies**:
   ```bash
   uv pip install pytest ruff
   ```

## Development Workflow

### Running Tests

```bash
pytest
```

Run with coverage:
```bash
pytest --cov=aicheck --cov-report=html
```

### Code Formatting

Format code with ruff:
```bash
ruff format src/aicheck/ tests/
```

### Linting

Check code quality:
```bash
ruff check src/aicheck/ tests/
```

Auto-fix issues:
```bash
ruff check --fix src/aicheck/ tests/
```

### Testing the CLI

After installing in editable mode, you can test the CLI:
```bash
aicheck 24 35
```

Or with the Python module:
```bash
python -m aicheck.cli 24 35
```

## Building the Package

Build the package for distribution:
```bash
uv build
```

This creates:
- `dist/aicheck-0.1.0.tar.gz` (source distribution)
- `dist/aicheck-0.1.0-py3-none-any.whl` (wheel)

## Publishing to PyPI

1. **Test on TestPyPI first**:
   ```bash
   uv publish --repository testpypi
   ```

2. **Publish to PyPI**:
   ```bash
   uv publish
   ```

You'll need PyPI credentials or an API token.

## Version Management

Update the version in `pyproject.toml`:
```toml
[project]
version = "0.2.0"
```

Also update in `src/aicheck/__init__.py`:
```python
__version__ = "0.2.0"
```

## Adding New Features

1. Write the feature code in `src/aicheck/`
2. Add tests in `tests/`
3. Run tests and linting
4. Update documentation in README.md
5. Commit changes

## Dependencies

The package has **zero runtime dependencies** - keep it that way!

Development dependencies are listed in `requirements-development.piptools`:
- pytest: Testing framework
- ruff: Linting and formatting

## Pre-commit Checklist

Before committing:
- [ ] All tests pass: `pytest`
- [ ] Code is formatted: `ruff format src/aicheck/ tests/`
- [ ] No linting errors: `ruff check src/aicheck/ tests/`
- [ ] Documentation is updated
- [ ] Version number is bumped (if applicable)

## CI/CD Considerations

For future automation, consider adding:
- `.github/workflows/test.yml` for GitHub Actions
- Automated testing on multiple Python versions
- Automated publishing on tagged releases
- Coverage reporting with codecov

## Troubleshooting

### Import Errors
If you get import errors, make sure the package is installed:
```bash
uv pip install -e .
```

### Tests Failing
Make sure you're in the package directory:
```bash
cd aicheck
pytest
```

### CLI Not Found
Reinstall the package:
```bash
uv pip uninstall aicheck
uv pip install -e .
```

