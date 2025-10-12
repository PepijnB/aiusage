# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Persistent configuration storage using `platformdirs` for platform-appropriate user config directory
- Interactive prompts for renewal day and percentage when no command-line arguments provided
- Ability to save renewal day for future use with opt-in confirmation
- Automatic loading of saved renewal day when running with only percentage argument
- `--version` and `-v` flags to display current version
- Version display in output header
- New `config.py` module for configuration management
- Comprehensive test coverage for configuration functionality
- Files: `src/aicheck/config.py`, `tests/test_config.py`

### Changed
- **Refactored CLI to use Cyclopts framework** for better help text, type validation, and cleaner code
- CLI now uses `importlib.metadata` to dynamically get version from `pyproject.toml`
- Interactive mode offers to change saved renewal day if one exists
- Single-argument mode now uses saved renewal day if available
- Commands can be called with or without subcommand name (`aicheck 35` or `aicheck check 35`)
- Files: `src/aicheck/cli.py`, `src/aicheck/__init__.py`, `pyproject.toml`

### Deprecated
- 

### Removed
- 

### Fixed
- 

### Security
-

---

## Template for Future Entries

<!--
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features or capabilities
- Files: `path/to/new/file.ext`, `another/file.ext`

### Changed
- Modifications to existing functionality
- Files: `path/to/modified/file.ext` (summary if many files)

### Deprecated
- Features that will be removed in future versions
- Files affected: `path/to/deprecated/file.ext`

### Removed
- Features or files that were deleted
- Files: `path/to/removed/file.ext`

### Fixed
- Bug fixes and corrections
- Files: `path/to/fixed/file.ext`

### Security
- Security patches or vulnerability fixes
- Files: `path/to/security/file.ext`

### Notes
- Additional context or important information
- Major dependencies updated
- Breaking changes explanation
-->
