---
name: psych-records-build-and-release
description: Knows how to build, package, and distribute the Psychological Records application using the provided scripts and configuration (PyInstaller, cx_Freeze, NSIS) and how to troubleshoot packaging issues. Use when the user asks about builds, installers, or running packaged versions of the app.
---

# Psychological Records Build & Release

## When to use this skill

Use this skill whenever you:

- Build or rebuild Windows executables or installers
- Modify PyInstaller, cx_Freeze, or NSIS configuration
- Adjust versioning, metadata, or distribution layout
- Diagnose issues that only appear in packaged builds

## Standard build commands

The docs (`docs/README.md`) describe the preferred build entry points:

- **PyInstaller (recommended)**:
  - From the project root: run the batch script under `scripts/`
  - Example: `cd scripts` then `.\build_pyinstaller.bat`

- **cx_Freeze**:
  - Example: `cd scripts` then `.\build_cx_freeze.bat`

- **NSIS installer**:
  - Example: `cd scripts` then `.\build_nsis_installer.bat`

- **Build all**:
  - Example: `cd scripts` then `.\build_all.bat`

If the project also includes `build_exe.bat` or `create_distribution.py` at the repo root, treat them as legacy or alternate entry points and prefer the documented scripts unless the user requests otherwise.

## Key configuration files and directories

When reasoning about builds, prefer reading and reusing existing configuration instead of inventing new ones:

- `config/` – current build configuration (e.g. `.spec` files, version info)
- `releases/` – historical packaged versions and reference configs (PyInstaller internals, NSIS scripts, older `src/` snapshots)
- `config/version_info.py` and any `version_info.py` under `releases/.../config/` – version metadata
- `PsychologicalRecords_*.spec` or similar files in `config/` or `releases/.../config/` – PyInstaller spec files

Treat files under `releases/` as reference implementations and examples; avoid editing them unless the user explicitly wants to update a historical release.

## Build behavior and troubleshooting

When helping with build or installer issues:

- Start from the recommended build scripts in `scripts/` rather than invoking PyInstaller or cx_Freeze manually
- If a packaged build is missing resources (icons, translations, data files), check:
  - The spec or setup files for `datas`/`include_files` sections
  - That `locales/`, `assets/`, and `data/` are correctly included
- For runtime errors that do not appear in development:
  - Compare the packaged `src/` layout under `releases/.../` with the current `src/` to spot missing imports or entry points
  - Verify that encryption libraries and DLLs required by SQLite or `cryptography` are bundled

If changing any build script or spec file, keep the commands and paths compatible with Windows and avoid hardcoding user-specific absolute paths.

## Versioning and artifacts

When adjusting versions or creating new releases:

- Keep version information consistent across:
  - `config/version_info.py`
  - Any installer metadata or NSIS scripts
  - The name of release directories under `releases/` (if creating new ones)
- Prefer not to commit large build artifacts unless they are part of an established `releases/` structure
- Document significant build changes (new installer type, changed entry point, etc.) in an appropriate changelog or release note file if one exists (for example `CHANGELOG_V0.4.0.md`)

