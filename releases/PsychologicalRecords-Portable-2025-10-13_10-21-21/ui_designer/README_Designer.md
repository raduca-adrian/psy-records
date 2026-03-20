# Qt Designer Integration Guide

## 🎨 Qt Designer Setup Complete!

Your PyQt6 application now has full Qt Designer integration for visual UI editing.

## Quick Start

### 1. Launch Qt Designer
```bash
# Option 1: Double-click the batch file
ui_designer/open_designer.bat

# Option 2: Use the Python script
python ui_designer/ui_tools.py designer

# Option 3: Direct command
.venv/Scripts/pyside6-designer.exe
```

### 2. Open Existing UI Files
Navigate to `ui_designer/forms/` and open any `.ui` file:
- `main_window.ui` - Main application window
- `person_dialog.ui` - Add/Edit person form
- `medical_records_window.ui` - Medical records interface
- `login_dialog.ui` - Login screen

### 3. Edit and Convert
After editing in Designer:
```bash
# Convert all UI files to Python classes
ui_designer/convert_ui.bat

# Or convert individually
python ui_designer/ui_tools.py convert forms/main_window.ui
```

## File Structure
```
ui_designer/
├── forms/           # .ui files (edit these in Designer)
├── generated/       # Generated Python UI classes
├── designer_styles.py  # Professional styling system
├── ui_tools.py      # Conversion and management tools
├── convert_ui.bat   # Batch convert all UI files
└── open_designer.bat  # Launch Designer
```

## Professional Styling

Your UI files integrate with the professional styling system:

```python
from ui_designer.designer_styles import StyleApplicator
from ui_designer.generated.main_window_ui import Ui_MainWindow

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Apply professional styling
        StyleApplicator.apply_window_style(self)
        StyleApplicator.apply_button_style(self.add_person_btn)
        StyleApplicator.apply_table_style(self.people_table)
```

## Theme Integration

The styling system supports your existing dark/light theme:

```python
# In your theme change handler
def on_theme_changed(self):
    StyleApplicator.apply_window_style(self)
    # Styles automatically adapt to current theme
```

## Tips for Designer

1. **Widget Names**: Use descriptive object names (e.g., `add_person_btn` instead of `pushButton`)
2. **Layouts**: Always use layouts for responsive design
3. **Size Policies**: Set appropriate size policies for proper scaling
4. **Properties**: Set minimum/maximum sizes where needed
5. **Spacing**: Use consistent spacing (8px, 16px, 24px)

## Converting Back to PyQt6

The generated code uses PySide6 imports. To use with PyQt6:

1. Run the conversion script:
```bash
python ui_tools.py convert_to_pyqt6 generated/main_window_ui.py
```

2. Or manually replace imports:
- `PySide6` → `PyQt6`
- `QCoreApplication.translate` → `QApplication.translate`

## Integration with Current App

To use Designer forms in your existing application:

1. Create a hybrid class:
```python
from ui_designer.generated.main_window_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect signals
        self.ui.add_person_btn.clicked.connect(self.add_person)
        
        # Apply styling
        from ui_designer.designer_styles import StyleApplicator
        StyleApplicator.apply_window_style(self)
```

2. Or inherit both classes:
```python
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Your existing code here
```

## Workflow Summary

1. **Edit** → Open `.ui` files in Qt Designer
2. **Convert** → Run `convert_ui.bat` to generate Python classes
3. **Style** → Use `StyleApplicator` for professional appearance
4. **Integrate** → Import generated classes in your application
5. **Theme** → Styling automatically adapts to your theme system

🎉 **You're all set!** Your PyQt6 application now has full visual UI editing capabilities with professional styling and theme support.
