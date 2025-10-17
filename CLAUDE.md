# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **TIDAL Downloader Next Generation (tidal-dl-ng)**, a Python application for downloading music and videos from TIDAL. The project provides both a command-line interface (CLI) and a graphical user interface (GUI). It supports multithreaded and multi-chunked downloads, metadata embedding, and various audio quality levels up to HiRes Lossless.

**Key Technologies:**
- Python 3.12
- Poetry for dependency management
- PySide6 (Qt6) for GUI
- Typer for CLI
- Rich for CLI progress/output
- tidalapi for TIDAL API integration
- ffmpeg for media processing

## Architecture

### Entry Points
- **CLI**: `tidal_dl_ng/cli.py` - Command-line interface using Typer
- **GUI**: `tidal_dl_ng/gui.py` - Qt-based graphical interface using PySide6

### Core Components

**Download System (`tidal_dl_ng/download.py`)**
- `Download` class is the main download orchestrator
- Handles segment-based downloading with concurrent workers
- Manages file merging, decryption, metadata writing, and playlist creation
- Supports both tracks and videos with quality settings
- Uses `ThreadPoolExecutor` for concurrent segment downloads
- Implements skip-existing logic and symlink support

**Configuration (`tidal_dl_ng/config.py`)**
- `Settings` class: User preferences (singleton pattern)
- `Tidal` class: TIDAL session and authentication (singleton pattern)
- `HandlingApp` class: Application-level event management (abort/run events)
- Config files stored in platform-specific directories

**API Integration (`tidal_dl_ng/api.py`)**
- Contains TIDAL API keys (loads from GitHub gist)
- Provides helper functions for API key management

**Metadata (`tidal_dl_ng/metadata.py`)**
- Writes ID3 tags to audio files using mutagen
- Handles lyrics, cover art, and replay gain metadata

**GUI (`tidal_dl_ng/gui.py`)**
- `MainWindow` class: Main Qt window with search, queue, and download functionality
- Uses Qt signals/slots for threading
- `Worker` class (`tidal_dl_ng/worker.py`): Qt thread wrapper
- Qt Designer UI files in `tidal_dl_ng/ui/` (compiled to Python)

### Helper Modules (`tidal_dl_ng/helper/`)
- `decorator.py`: Singleton metaclass
- `decryption.py`: File decryption for protected streams
- `exceptions.py`: Custom exceptions
- `gui.py`: GUI-specific helpers (models, filters)
- `path.py`: Path formatting and sanitization
- `tidal.py`: TIDAL API helpers (media instantiation, formatting)
- `wrapper.py`: Logger wrapper for Rich integration

### Data Models (`tidal_dl_ng/model/`)
- `cfg.py`: Configuration and settings data classes
- `downloader.py`: Download-related data structures
- `gui_data.py`: GUI-specific data models
- `meta.py`: Metadata structures

## Development Commands

### Installation
```bash
# Install Poetry
pipx install --upgrade poetry

# Install dependencies (including GUI support)
poetry install --all-extras --with dev,docs

# Activate virtual environment
poetry shell
```

### Testing
```bash
# Run tests with pytest
poetry run pytest --doctest-modules
```

### Code Quality
```bash
# Run all quality checks (ruff, pre-commit, deptry)
make check

# Individual tools
poetry run pre-commit run -a
poetry run deptry .
```

### Building
```bash
# Build Python wheel
make build

# Build GUI for macOS
make gui-macos-dmg

# Build GUI for Windows
make gui-windows

# Build GUI for Linux
make gui-linux
```

### GUI Development
```bash
# Launch Qt Designer with custom widgets
PYSIDE_DESIGNER_PLUGINS=tidal_dl_ng/ui pyside6-designer

# Convert .ui files to Python (run after modifying .ui files)
pyside6-uic tidal_dl_ng/ui/main.ui -o tidal_dl_ng/ui/main.py
```

### Documentation
```bash
# Build and serve docs
make docs

# Test docs build
make docs-test
```

## Coding Standards

### Python Style (from .github/copilot-instructions.md)
- Use snake_case for variables/functions, CamelCase for classes
- Follow PEP 8, PEP 484 (type hints), PEP 492 (async/await), PEP 498 (f-strings), PEP 572 (walrus operator)
- Use modern built-in generics: `list`, `dict`, `set` (not `List`, `Dict`, `Set` from typing)
- Prefix private class members with underscore
- Use ALL_CAPS for constants
- Always use type annotations for function parameters, return types, and variables
- Write Google-style docstrings for all modules, classes, functions, and methods
- Use try/except blocks for error handling with contextual logging
- Use blank lines for better code organization

### Tools Configuration
- **Ruff**: Line length 120, various linters enabled (see pyproject.toml)
- **Black**: Line length 120, Python 3.12 target
- **mypy**: Strict type checking enabled
- **isort**: Black-compatible profile

### Important Files to Exclude from Black/Editing
- `tidal_dl_ng/ui/main.py` - Auto-generated from Qt Designer
- `tidal_dl_ng/ui/dialog_version.py` - Auto-generated from Qt Designer

## Common Workflows

### Adding New Download Features
1. Modify `Download` class in `download.py` for core functionality
2. Update CLI commands in `cli.py` if needed
3. Update GUI in `gui.py` if needed
4. Add settings to `model/cfg.py` if configuration is required
5. Update file path formatting in `helper/path.py` if needed

### Adding New Settings
1. Add field to `Settings` class in `model/cfg.py`
2. Add to `HelpSettings` for CLI help text
3. Update `DialogPreferences` in `dialog.py` for GUI
4. Update `settings_management` in `cli.py` for CLI access

### GUI Modifications
1. Edit `.ui` files with Qt Designer
2. Run `pyside6-uic` to convert to Python
3. Connect signals/slots in `gui.py`
4. Test with `tidal-dl-ng gui` or `poetry run python tidal_dl_ng/gui.py`

## Key Patterns

### Singleton Pattern
Configuration classes use `SingletonMeta` to ensure single instances throughout the app lifetime.

### Threading Pattern
- GUI uses Qt's `QThreadPool` with custom `Worker` class
- Downloads use Python's `ThreadPoolExecutor` for concurrent segment downloads
- Event-based control with `HandlingApp.event_abort` and `event_run`

### Progress Reporting
- CLI: Rich `Progress` bars
- GUI: Qt signals emitting progress percentages
- Both use same `Download` class with conditional progress routing

### File Path Handling
All paths go through `path_file_sanitize()` to ensure OS compatibility and length limits.

## Testing Notes

- Test files are in `tests/` directory
- Use pytest for running tests
- Tests should cover download logic, path formatting, and configuration

## Known TODOs in Code
- Proper logging implementation (many TODOs in code)
- Use pathlib.Path everywhere consistently
- Set appropriate client string for video downloads
- Compute download speed display
- macOS code signing for GUI builds

## Important Configuration Paths
- Settings: Platform-specific (e.g., `~/.config/tidal-dl-ng/settings.json` on Linux)
- Token storage: Same directory as settings
- Default download path: User's home directory

## Dependencies
- Core: requests, mutagen, dataclasses-json, pathvalidate, m3u8, python-ffmpeg, pycryptodome, tidalapi
- CLI: typer, rich, coloredlogs
- GUI: pyside6, pyqtdarktheme-fork (optional)
- Build: nuitka (for standalone executables)
