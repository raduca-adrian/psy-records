---
name: psych-records-architecture
description: Understands the Psychological Records app architecture (core, ui, utils, database, and translations) and applies project-specific patterns when modifying or adding features. Use when editing src/, tests/, data/, or docs for this application.
---

# Psychological Records Architecture

## When to use this skill

Use this skill whenever you:

- Modify code under `src/`, `tests/`, or `scripts/`
- Change how the database, encryption, or data files work
- Update PyQt6 UI code, dialogs, or window layouts
- Work on translations, locales, or language-related behavior
- Touch PDF export or reporting logic that depends on the core model

## High-level architecture

The project is a secure, multilingual medical records application built with PyQt6 and an encrypted SQLite database.

Key directories (see `docs/README.md` for details):

- `src/core/` – core business logic, database access, encryption, models
- `src/ui/` – PyQt6 windows, dialogs, and presentation logic
- `src/utils/` – helper utilities (PDF generation, theming, translation, etc.)
- `locales/` – translation JSON files (e.g. `locales/ro/translations.json`)
- `tests/` – unit and integration tests
- `data/` – encrypted database and related data files

When making changes, keep business logic in `src/core/` and keep `src/ui/` focused on presentation, wiring, and user interaction.

## Database and security

Primary database logic lives in `src/core/database.py` (and historical variants in `releases/.../src/core/database.py` that can serve as reference).

When editing or extending database-related code:

- Prefer using the existing database helper functions instead of introducing raw `sqlite3` usage in UI code
- Preserve encryption and key-handling patterns; never store secrets or keys in plain text
- Keep all paths to real patient data under `data/` and avoid hardcoding absolute file system paths
- Be conservative about adding logging around database operations; never log sensitive fields (names, diagnoses, notes, passwords)
- If a change affects schema or migrations, add or update tests that cover both old and new paths

## UI and layout patterns

Core UI components live under `src/ui/` (for example, `unified_main_window.py` and the add/edit dialogs).

When changing UI code:

- Follow existing PyQt6 patterns: signals/slots for communication, avoid heavy business logic directly in widgets
- Keep long-running operations out of the main thread where possible to avoid freezing the UI
- Respect the modern, material-inspired styling described in:
  - `docs/MATERIAL_DESIGN_THEME.md`
  - `docs/MODERN_UI_IMPLEMENTATION_SUMMARY.md`
  - `docs/VISUAL_GUIDE.md`
- Keep widget naming and layout consistent with existing dialogs (e.g. `add_patient_dialog.py`, `edit_checkup_dialog.py`)
- For new dialogs or windows, mirror the structure of the closest existing file to stay consistent with the rest of the app

## Translations and multilingual behavior

The app is multilingual (English/Romanian) and uses translation helpers:

- `src/utils/app_translator.py`
- Translation JSONs under `locales/*/translations.json`
- Additional language utilities (see older versions under `releases/.../src/utils/` for reference)

When adding or changing user-facing text:

- Do not hardcode user-visible strings directly in UI code; route them through the translation system
- Update the relevant entries in `locales/en/translations.json` and `locales/ro/translations.json`
- Ensure new text keys are descriptive and consistent with existing naming
- If dialogs gain or lose fields, also check any tests that assert on visible labels or window titles

## Testing guidelines

When you change core logic, database behavior, or UI flows:

- Add or update tests in `tests/` alongside similar existing tests (e.g. `test_unified_window.py`, `test_diacritics.py`, `test_simple_diacritics.py`)
- Prefer small, focused tests that exercise a single behavior
- For UI-related behavior, test high-level outcomes (e.g. whether the correct data is saved or the correct text is displayed) rather than PyQt internals

Before proposing large refactors or feature additions, quickly scan the docs in `docs/` (especially `UNIFIED_WINDOW_APPLICATION.md`, `UI_IMPROVEMENTS_V0.4.md`, and related UI/PDF docs) to align with the intended design.

