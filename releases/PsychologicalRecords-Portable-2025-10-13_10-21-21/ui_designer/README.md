# PyQt6 Designer Integration

This directory contains tools and resources for editing the Psychological Records application UI using Qt Designer.

## 📁 Directory Structure

```
ui_designer/
├── forms/                    # UI form files
│   ├── main_window.ui       # Main application window
│   ├── person_dialog.ui     # Add/Edit person dialog
│   ├── medical_records_window.ui  # Medical records window
│   ├── login_dialog.ui      # Login dialog
│   └── *_ui.py             # Generated Python files
├── resources/               # UI resources (icons, images)
├── designer_styles.py       # Clean style definitions
├── ui_tools.py             # Conversion and management tools
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Install Required Tools
```bash
pip install pyqt6-tools
```

### 2. Open Qt Designer
```bash
cd ui_designer
python ui_tools.py designer
```

### 3. Edit Forms
- Open any `.ui` file in Qt Designer
- Make your visual changes
- Save the file

### 4. Generate Python Code
```bash
python ui_tools.py convert
```

### 5. Apply Styles in Code
```python
from ui_designer.designer_styles import StyleApplicator

# Apply styles to widgets
StyleApplicator.apply_primary_button(my_button)
StyleApplicator.apply_input_field(my_line_edit)
StyleApplicator.apply_table(my_table)
```

## 🎨 Available UI Forms

### Main Window (`main_window.ui`)
- Main application layout
- Search functionality
- Action buttons
- People table
- Theme toggle

### Person Dialog (`person_dialog.ui`)
- Add/Edit person form
- Name, CNP, contact information
- Notes field
- Save/Cancel buttons

### Medical Records Window (`medical_records_window.ui`)
- Patient header information
- Assessment and session tabs
- Action buttons
- Data tables

### Login Dialog (`login_dialog.ui`)
- Secure authentication
- Username/password fields
- Language selection
- Setup button

## 🎯 Style System

### Pre-defined Styles
The `designer_styles.py` module provides ready-to-use styles:

- **Buttons**: Primary, Success, Secondary
- **Inputs**: Line edits, Text areas, Combo boxes
- **Tables**: Data tables with headers
- **Frames**: Cards, Headers
- **Labels**: Titles, Subtitles, Info text
- **Dialogs**: Complete dialog styling

### Color Palette
- **Light Theme**: Professional blue and gray palette
- **Dark Theme**: Modern dark interface colors
- **Consistent**: All colors follow design system

### Usage Examples
```python
# Apply button styles
StyleApplicator.apply_primary_button(save_button)
StyleApplicator.apply_secondary_button(cancel_button)

# Apply form styles
StyleApplicator.apply_input_field(name_edit)
StyleApplicator.apply_text_area(notes_edit)

# Apply layout styles
StyleApplicator.apply_card_frame(form_frame)
StyleApplicator.apply_header_frame(header_frame)
```

## 🛠️ Tools and Commands

### UI Tools Script (`ui_tools.py`)

```bash
# Open Qt Designer
python ui_tools.py designer

# Convert all .ui files to Python
python ui_tools.py convert

# Create example usage file
python ui_tools.py example
```

### Manual Conversion
```bash
# Convert specific file
pyuic6 -o output.py input.ui

# Convert with resource file
pyrcc6 -o resources.py resources.qrc
```

## 📝 Workflow

### 1. Design Phase
1. Open Qt Designer
2. Create or edit .ui files
3. Use standard Qt widgets
4. Set object names for programmatic access
5. Save changes

### 2. Code Generation
1. Run conversion tool
2. Python files generated automatically
3. Style helper methods added
4. Import statements included

### 3. Integration
1. Import generated UI classes
2. Create widget instances
3. Apply styles using StyleApplicator
4. Connect signals and slots

### 4. Testing
1. Run application
2. Verify visual appearance
3. Test functionality
4. Iterate as needed

## 🎨 Qt Designer Tips

### Widget Naming Convention
- Use descriptive names: `save_btn`, `name_edit`, `people_table`
- Follow snake_case convention
- Include widget type in name

### Layout Best Practices
- Use layouts for responsive design
- Set minimum/maximum sizes appropriately
- Use spacers for flexible spacing
- Group related widgets in frames

### Form Design
- Consistent spacing and margins
- Logical tab order
- Appropriate widget sizes
- Clear visual hierarchy

## 🔧 Customization

### Adding New Styles
1. Edit `designer_styles.py`
2. Add new style constants
3. Update `StyleApplicator` class
4. Use in your forms

### Custom Widgets
1. Create widget in Designer
2. Set custom properties
3. Apply styles programmatically
4. Handle events in Python code

### Theme Support
- Light and dark themes included
- Easy theme switching
- Consistent color palette
- Automatic style application

## 🚀 Integration with Main App

### Using Designer Forms
```python
from ui_designer.forms.main_window_ui import Ui_MainWindow
from ui_designer.designer_styles import StyleApplicator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.apply_styles()
        
    def apply_styles(self):
        StyleApplicator.apply_primary_button(self.ui.add_person_btn)
        StyleApplicator.apply_table(self.ui.people_table)
        # ... more style applications
```

### Benefits
- ✅ Visual design with Qt Designer
- ✅ Clean separation of UI and logic
- ✅ Consistent styling system
- ✅ Easy maintenance and updates
- ✅ Professional appearance
- ✅ Theme support included

## 📚 Resources

- [Qt Designer Manual](https://doc.qt.io/qt-6/qtdesigner-manual.html)
- [PyQt6 Documentation](https://doc.qt.io/qtforpython/)
- [Qt Stylesheets Reference](https://doc.qt.io/qt-6/stylesheet-reference.html)

## 🔗 Integration

This Designer system is fully compatible with the existing Psychological Records application. You can gradually migrate existing forms to use Designer files while maintaining all functionality.
