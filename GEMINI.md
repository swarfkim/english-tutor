# English Tutor Project

## Project Structure
- `english_tutor/`: Main package containing indices, views, and components.
- `diag_unix.py`: Unix-based database diagnostic script.
- `diagnose_db.py`: Database connection diagnostic script.
- `rxconfig.py`: Reflex configuration.
- `pyproject.toml`: Project dependencies and metadata.

## Type Safety
- The project uses `ty` for type checking.
- Run `ty check` to verify type safety.
- **Convention**: Use modern Python 3.10+ type hints:
  - Use `list`, `dict`, `set` instead of `typing.List`, `typing.Dict`, `typing.Set`.
  - Use the `|` operator for `Union` and `Optional` (e.g., `str | int`, `str | None`).
  - Avoid `typing.List`, `typing.Dict`, `typing.Set`, `typing.Union`, `typing.Optional`.

## Database
- Uses PGlite for local development (`pgdata`, `pgdata_diag`, etc.).
