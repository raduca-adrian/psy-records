#!/usr/bin/env python3
"""
Create a distribution zip package for the Psychological Records application.
"""

import os
import sys
import zipfile
import shutil
from datetime import datetime
from pathlib import Path

def create_distribution():
    """Create a zip distribution package."""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}")
    
    # Create timestamp for the distribution
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dist_name = f"PsychologicalRecords-Portable-{timestamp}"
    dist_path = project_root / "releases" / dist_name
    
    # Create the distribution directory
    dist_path.mkdir(parents=True, exist_ok=True)
    print(f"Creating distribution in: {dist_path}")
    
    # Files and directories to include in the distribution
    include_items = [
        # Core application files
        "src/",
        "run_unified.py",
        "run.py",
        
        # Configuration and data
        "requirements.txt",
        "setup.py",
        "pyproject.toml",
        "MANIFEST.in",
        
        # Assets
        "assets/",
        "locales/",
        
        # Documentation
        "docs/",
        "*.md",
        
        # Configuration files
        "settings.json",
        "config/",
        
        # Scripts (excluding build scripts)
        "scripts/ui_designer/",
        "scripts/create_icon.py",
        "scripts/create_simple_icon.py",
        "scripts/run_tests.py",
        
        # Tests
        "tests/",
    ]
    
    # Files and directories to exclude
    exclude_patterns = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".git",
        ".gitignore",
        "build/",
        "dist/",
        "*.egg-info/",
        ".pytest_cache/",
        "releases/",
        "*.log",
        "*.tmp",
        "*.temp",
        "data/secure_app.db.enc",  # Exclude encrypted database
        "data/Report_*.pdf",  # Exclude report files
        "scripts/build_*.bat",
        "scripts/test_*.bat",
        "scripts/run_app.bat",
        "scripts/PsychologicalRecords.spec",
    ]
    
    def should_exclude(file_path):
        """Check if a file should be excluded."""
        file_path_str = str(file_path)
        for pattern in exclude_patterns:
            if pattern.endswith("/"):
                if file_path_str.startswith(pattern[:-1]):
                    return True
            elif pattern.startswith("*"):
                if file_path_str.endswith(pattern[1:]):
                    return True
            else:
                if pattern in file_path_str:
                    return True
        return False
    
    # Copy files and directories
    copied_items = []
    
    for item in include_items:
        item_path = project_root / item
        
        if item_path.is_file():
            if not should_exclude(item_path):
                dest_path = dist_path / item_path.name
                shutil.copy2(item_path, dest_path)
                copied_items.append(str(item_path))
                print(f"Copied file: {item_path}")
        
        elif item_path.is_dir():
            dest_dir = dist_path / item_path.name
            if not should_exclude(item_path):
                shutil.copytree(item_path, dest_dir, ignore=shutil.ignore_patterns(
                    "__pycache__", "*.pyc", "*.pyo", "*.pyd", ".git", ".gitignore"
                ))
                copied_items.append(str(item_path))
                print(f"Copied directory: {item_path}")
    
    # Create a README for the distribution
    readme_content = f"""# Psychological Records - Portable Distribution

Version: 0.5.0
Distribution Date: {timestamp}

## Quick Start

1. **Prerequisites**: Python 3.8+ with PyQt6 installed
2. **Installation**: 
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python run_unified.py
   ```

## Features

- Secure medical records management
- Multi-language support (English/Romanian)
- Modern Material Design UI
- PDF report generation
- Encrypted database storage
- Unified single-window interface

## System Requirements

- Python 3.8 or higher
- PyQt6
- Windows 10/11 (recommended)
- 100MB free disk space

## Documentation

See the `docs/` folder for detailed documentation including:
- Installation guide
- User manual
- Development documentation
- UI improvements and features

## Support

For issues or questions, please refer to the documentation in the `docs/` folder.

---
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    readme_path = dist_path / "README.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"Created README: {readme_path}")
    
    # Create a simple launcher script
    launcher_content = """@echo off
echo Starting Psychological Records...
python run_unified.py
pause
"""
    
    launcher_path = dist_path / "run_app.bat"
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print(f"Created launcher: {launcher_path}")
    
    # Create the zip file
    zip_path = project_root / "releases" / f"{dist_name}.zip"
    print(f"Creating zip file: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_path):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(dist_path)
                zipf.write(file_path, arc_path)
                print(f"Added to zip: {arc_path}")
    
    print(f"\nDistribution created successfully!")
    print(f"Zip file: {zip_path}")
    print(f"Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")
    print(f"Contents: {len(copied_items)} items")
    
    return zip_path

if __name__ == "__main__":
    try:
        zip_path = create_distribution()
        print(f"\n[SUCCESS] Distribution package created: {zip_path}")
    except Exception as e:
        print(f"[ERROR] Error creating distribution: {e}")
        sys.exit(1)
