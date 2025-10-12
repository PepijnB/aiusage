# Type Stubs Directory

This directory is reserved for custom type stub files (`.pyi`) for third-party libraries that don't provide inline type hints.

## Current Status

All runtime dependencies in this project have inline type hints (PEP 561 compliant):
- ✅ `cyclopts` - has `py.typed`
- ✅ `platformdirs` - has `py.typed`
- ✅ `attrs` - has `py.typed`
- ✅ `rich` - has `py.typed`
- ✅ `pytest` - has `py.typed`
- ✅ `docstring_parser` - has `py.typed`

## Adding Custom Stubs

If you need to add custom type stubs for a library:

1. Create a directory matching the package name: `typings/packagename/`
2. Add stub files: `typings/packagename/__init__.pyi`
3. mypy will automatically discover stubs in this directory

Example stub file structure:
```
typings/
└── somelibrary/
    ├── __init__.pyi
    └── submodule.pyi
```

## Resources

- [PEP 561 - Distributing and Packaging Type Information](https://peps.python.org/pep-0561/)
- [mypy documentation on stub files](https://mypy.readthedocs.io/en/stable/stubs.html)
- [typeshed repository](https://github.com/python/typeshed)

