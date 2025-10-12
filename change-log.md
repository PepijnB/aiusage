# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) (YYYY.MM.DD format).

## [Unreleased]

### Added
- 

### Changed
- 

### Deprecated
- 

### Removed
- 

### Fixed
- 

### Security
-

---

## [2025.10.12] - 2025-10-12

**Initial Release** 🎉

A smart command-line tool for tracking AI credit consumption across billing cycles. Designed for AI-powered development tools like Cursor, GitHub Copilot, and other subscription-based AI services.

### Added
- Real-time usage analysis comparing credit usage against billing cycle progress
- Color-coded feedback (green for conserving, red for warnings)
- Smart projections predicting remaining credits at renewal
- Flexible billing cycle support for any renewal day of the month
- Persistent configuration storage using `platformdirs` for platform-appropriate user config directory
- Interactive prompts for renewal day and percentage when no command-line arguments provided
- Ability to save renewal day for future use with opt-in confirmation
- Automatic loading of saved renewal day when running with only percentage argument
- `--version` and `-v` flags to display current version
- Version display in output header
- Privacy-first design: no web services, no logins, no data collection—runs entirely offline
- Comprehensive test coverage for configuration and core functionality
- Files: `src/aiusage/cli.py`, `src/aiusage/config.py`, `src/aiusage/core.py`, `tests/test_config.py`, `tests/test_core.py`

### Notes
- Minimal dependencies: only platformdirs and cyclopts required
- Python 3.13+ required for modern type hints
- Works on macOS, Linux, and Windows

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
