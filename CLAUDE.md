# CLAUDE Guidelines

## Directory Whitelist
The repository should only contain the following top-level directories:

- `src/`
- `tests/`
- `docs/`
- `.github/`
- `scripts/`

Files or directories outside this whitelist should be removed or relocated into an allowed directory.

## Code Style
- Format Python code with [Black](https://github.com/psf/black).
- Sort imports with [isort](https://pycqa.github.io/isort/).
- Lint using [Flake8](https://flake8.pycqa.org/).
- Type-check with [mypy](http://mypy-lang.org/).
- Follow PEP 8 naming conventions:
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

## Commit Message Format
Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>
```

Examples of `type` include `feat`, `fix`, `docs`, `style`, `refactor`, `test`, and `chore`.

Run `pre-commit run --all-files` before committing to ensure style and type checks pass.
