# Psychological Records – Agent Guide

This file gives AI coding assistants project-specific context for the **Psychological Records** application: how it is structured, how to run and test it, and important security and privacy constraints.

## Project overview

- **Type**: Secure, multilingual medical records management system
- **Tech stack**: Python (3.8+), PyQt6, encrypted SQLite database, `cryptography`, `reportlab`
- **Key capabilities**: Patient records, psychological assessments, consultation notes, PDF export, user authentication, multi-language UI (English/Romanian)

For more details, see `docs/README.md`.

## Repository layout

High-level structure (simplified from `docs/README.md`):

- `src/core/` – core business logic, database, encryption, domain models
- `src/ui/` – PyQt6 UI components (main window, dialogs, unified window)
- `src/utils/` – utilities (PDF generation, theming, translation, helpers)
- `locales/` – translation files (per-language `translations.json`)
- `docs/` – architecture, UI, and migration documentation
- `scripts/` – build and deployment scripts
- `tests/` – unit and integration tests
- `data/` – encrypted database and data files
- `main.py` / `run_unified.py` – application entry points

When modifying code, keep:

- **Business logic** in `src/core/`
- **Presentation logic** and user interaction in `src/ui/`
- **Cross-cutting helpers** in `src/utils/`

## Running the app

From a development checkout (see `docs/README.md` for details):

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
   - `pip install -e .[dev]` (if available)
3. Run the application:
   - `python main.py`
   - or, if provided for the unified window: `python run_unified.py`

Always assume a Windows environment unless otherwise stated, and favor documented commands over ad-hoc ones.

## Tests and quality checks

The project follows PEP 8 and uses tools such as Black, isort, flake8, and pre-commit hooks.

When changing Python code:

- Prefer running tests with `python -m pytest` (or the project’s `scripts/run_tests.py` if present).
- Keep new tests close to existing ones in `tests/` (e.g. `test_unified_window.py`, `test_diacritics.py`, language and UI tests).
- Maintain import order and formatting consistent with Black and isort.

If you introduce non-trivial behavior in `src/core/` or `src/ui/`, add or update tests to cover it.

## Build and release behavior

Executables and installers are built primarily for Windows:

- Use the batch scripts in `scripts/` as the **preferred entry points**:
  - PyInstaller builds (recommended)
  - cx_Freeze builds
  - NSIS installers
  - “build all” scripts to run the full pipeline
- Treat `config/` as the source of truth for active spec/config files.
- Treat `releases/` as **historical reference** and examples; avoid editing them unless explicitly requested.

When assisting with build issues, start from the documented scripts and then inspect relevant spec/config files instead of inventing new build flows.

## Security and privacy expectations

This is a medical records system; always assume data is sensitive:

- **Do not** log or print personally identifiable information (PII) or detailed medical notes.
- **Do not** store passwords, encryption keys, or secrets in plain text.
- **Do not** weaken or remove database encryption or password checks.
- Favor using existing, audited helpers in `src/core/database.py` and related modules over new ad-hoc crypto or SQL code.
- Avoid suggesting real patient data for tests or examples; use clearly fake/sample data only.

If a requested change might meaningfully impact security (encryption, authentication, access control), call that out explicitly and suggest additional review and testing.

## Project-specific skills

This repository defines Cursor skills under `.cursor/skills/`:

- **`psych-records-architecture`** – Understands the project’s architecture (core/ui/utils, database, translations) and how to apply existing patterns when modifying features or adding new ones.
- **`psych-records-build-and-release`** – Knows how to build, package, and troubleshoot the application using the project’s PyInstaller, cx_Freeze, and NSIS configuration.

AI assistants working on this project should consult these skills whenever they:

- Edit code under `src/`, `tests/`, `data/`, or `scripts/`
- Modify build scripts, spec files, or anything under `config/` or `releases/`

