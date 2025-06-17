# AGENTS Instructions

This repository hosts a minimal FastAPI server that uses `llama.cpp` and a few static assets for a lightweight assistant. Keep contributions focused and easy to review.

## Style and Conventions

- **Python**
  - Follow PEP8 with 4 space indentation.
  - Add type hints and docstrings to public functions when practical.
  - Prefer the standard library over extra dependencies.

- **JavaScript**
  - Use 2 spaces for indentation.
  - Use `camelCase` for function and variable names.

## Testing

Run the test suite before committing:

```bash
pytest -q
```

If tests fail because of missing system dependencies (e.g. `llama_cpp` binaries), mock them as done in `tests/` or explain in the PR.

## Pull Request Guidelines

- Provide a clear summary of changes and reference any relevant issues.
- Include a short section listing the commands you executed to test the changes.
- Keep the PR focused on a single topic.
