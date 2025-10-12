# Development Guide

This guide covers development, testing, and publishing of the `aiusage` package.

## Package Structure

```
aiusage/
├── src/aiusage/           # Source code
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
   cd aiusage
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
pytest --cov=aiusage --cov-report=html
```

### Code Formatting

Format code with ruff:
```bash
ruff format src/aiusage/ tests/
```

### Linting

Check code quality:
```bash
ruff check src/aiusage/ tests/
```

Auto-fix issues:
```bash
ruff check --fix src/aiusage/ tests/
```

### Type Checking

Run mypy for comprehensive type checking:
```bash
mypy -p aiusage
```

The project uses strict type checking with:
- Type hints on all functions
- TypedDict for structured return types
- Proper type narrowing for JSON parsing
- Custom type stubs in `typings/` directory (if needed)

All runtime dependencies have inline type hints (marked with `py.typed`):
- `cyclopts` - CLI framework
- `platformdirs` - Cross-platform config directories
- `attrs` - Classes without boilerplate
- `rich` - Terminal formatting
- `pytest` - Testing framework

#### IDE Configuration

The project includes configuration for VSCode/Cursor:
- **`.vscode/settings.json`**: Configures Pylance, mypy, ruff, and pytest
- **`.vscode/extensions.json`**: Recommends required extensions
- **`pyrightconfig.json`**: Standalone Pyright/Pylance configuration
- **`mypy.ini`**: mypy configuration (strict mode)
- **`pyproject.toml`**: Contains `[tool.pyright]` section

Both Pylance (VSCode's default) and mypy are configured to:
- Use strict type checking mode
- Search the `typings/` directory for custom stubs
- Include `src/` in the Python path
- Report comprehensive type errors

### Testing the CLI

After installing in editable mode, you can test the CLI:
```bash
aiusage 24 35
```

Or with the Python module:
```bash
python -m aiusage.cli 24 35
```

## Building the Package

Build the package for distribution:
```bash
uv build
```

This creates:
- `dist/aiusage-0.1.0.tar.gz` (source distribution)
- `dist/aiusage-0.1.0-py3-none-any.whl` (wheel)

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

Also update in `src/aiusage/__init__.py`:
```python
__version__ = "0.2.0"
```

## Adding New Features

1. Write the feature code in `src/aiusage/`
2. Add tests in `tests/`
3. Run tests and linting
4. Update documentation in README.md
5. Commit changes

## Dependencies

### Runtime Dependencies

The package has minimal runtime dependencies:
- `platformdirs>=4.0.0` - Cross-platform config directory management
- `cyclopts>=3.0.0` - Modern CLI framework with type hints

All dependencies include inline type hints (PEP 561 compliant with `py.typed` markers).

### Development Dependencies

Development dependencies are listed in `requirements-development.piptools` and `pyproject.toml`:
- **Testing**: `pytest`, `pytest-cov`, `pytest-clarity`
- **Code Quality**: `ruff` (linting and formatting), `mypy` (type checking)
- **AI Tools**: `pyrefly` (AI-powered code analysis and refactoring)

## Pre-commit Checklist

Before committing:
- [ ] All tests pass: `pytest`
- [ ] Code is formatted: `ruff format src/aiusage/ tests/`
- [ ] No linting errors: `ruff check src/aiusage/ tests/`
- [ ] Type checking passes: `mypy -p aiusage`
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
cd aiusage
pytest
```

### CLI Not Found
Reinstall the package:
```bash
uv pip uninstall aiusage
uv pip install -e .
```

