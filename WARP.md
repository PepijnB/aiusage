# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

**aiusage** is a smart command-line tool for tracking AI credit consumption across billing cycles. It helps developers avoid overages by comparing credit usage to time progress through renewal cycles, with color-coded feedback and usage projections.

## Common Development Commands

### Environment Setup

```bash
# Install in editable mode
uv pip install -e .

# Install development dependencies
uv pip install pytest ruff
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=aiusage --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run specific test function
pytest tests/test_core.py::test_calculate_progress_basic
```

### Code Quality

```bash
# Check code quality
ruff check src/aiusage/ tests/

# Auto-fix issues and format code
ruff check --fix src/aiusage/ tests/
ruff format src/aiusage/ tests/

# Format only
ruff format src/aiusage/ tests/

# Type checking
mypy -p aiusage
```

### CLI Testing

```bash
# Test the CLI after editable install
aiusage 15 45  # Renewal on 15th, 45% used
aiusage 25     # Default renewal (1st), 25% used

# Or run via module
python -m aiusage.cli 15 45
```

### Building and Publishing

```bash
# Build package
uv build

# Publish to TestPyPI (for testing)
uv publish --repository testpypi

# Publish to PyPI
uv publish
```

## Architecture Overview

### Module Structure

The project follows a clean separation between core logic and CLI presentation:

```
src/aiusage/
├── __init__.py      # Package exports and version
├── core.py          # Pure calculation functions
└── cli.py           # Command-line interface and output formatting
```

### Core Components

**`core.py`** - Pure calculation logic with zero dependencies:
- `calculate_progress()`: Main function that calculates usage ratios, projections, and status
- `ordinal_suffix()`: Utility for formatting day numbers (1st, 2nd, 3rd, etc.)
- Handles complex billing cycle calculations across month boundaries
- Returns structured data dictionary with all metrics

**`cli.py`** - Command-line interface and presentation:
- Argument parsing with flexible parameter order (day/percentage or percentage only)
- ANSI color coding for visual feedback (green=conserving, red=warning)
- Formatted output with emoji indicators and clear status messages
- Entry point defined as `aiusage = aiusage.cli:main` in pyproject.toml

### Key Design Principles

- **Zero runtime dependencies**: Uses only Python 3.13+ standard library
- **Pure function design**: Core logic is testable and side-effect free  
- **Clear separation**: CLI never imports presentation logic into core calculations
- **Smart argument handling**: Flexible command-line argument order detection
- **Color-coded feedback**: Immediate visual status indication

### Testing Strategy

Tests focus on the core calculation logic with known dates and scenarios:
- Boundary conditions (month transitions, leap years)
- Different billing cycle scenarios (before/after renewal day)
- Status categorization (conserving/on-track/using-too-fast)
- Projection accuracy with various usage rates

## Project Characteristics

- **Python 3.13+** required (uses modern type hints)
- **UV-first workflow** for dependency management, building, and publishing  
- **Ruff** for linting and formatting (120 char line length, single quotes)
- **pytest** for testing with coverage reporting
- **src/ layout** for proper import isolation and packaging
- **CLI-focused** with global command installation via pip/uv