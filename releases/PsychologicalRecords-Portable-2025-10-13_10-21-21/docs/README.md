# Psychological Records Application

A secure, multilingual medical records management system built with PyQt6 and SQLite encryption.

## Features

- **Secure Database**: All data is encrypted using advanced encryption algorithms
- **Multi-language Support**: Interface available in English and Romanian
- **Medical Records Management**: Complete patient record system
- **Psychological Assessments**: Comprehensive assessment tools
- **Consultation Notes**: Detailed consultation management
- **PDF Export**: Generate professional reports
- **User Management**: Secure login with password protection

## Requirements

- Python 3.8 or higher
- PyQt6
- cryptography
- reportlab

## Installation

### Option 1: From Source

```bash
git clone https://github.com/your-repo/psychological-records.git
cd psychological-records
pip install -r requirements.txt
python main.py
```

### Option 2: Using Setup

```bash
pip install -e .
psychological-records
```

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Building Executables

The project includes build scripts for creating distributable executables:

### PyInstaller (Recommended)
```bash
cd scripts
.\build_pyinstaller.bat
```

### cx_Freeze
```bash
cd scripts  
.\build_cx_freeze.bat
```

### NSIS Installer (Windows)
```bash
cd scripts
.\build_nsis_installer.bat
```

### Build All
```bash
cd scripts
.\build_all.bat
```

## Project Structure

```
psychological-records/
├── src/
│   ├── core/          # Core business logic
│   ├── ui/            # User interface components
│   └── utils/         # Utility functions
├── config/            # Build configurations
├── scripts/           # Build and deployment scripts
├── docs/              # Documentation
├── assets/            # Icons and static resources
├── locales/           # Translation files
├── tests/             # Test files
├── data/              # Database and data files
└── main.py            # Application entry point
```

## Code Quality

This project follows PEP 8 standards and uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **pre-commit** for git hooks

## Security

- All database files are encrypted
- Password-protected access
- Secure data transmission
- No plain-text storage of sensitive information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact: support@psychologicalrecords.com
