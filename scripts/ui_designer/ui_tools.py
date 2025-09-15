"""
UI Designer Integration Script
This script helps convert .ui files to Python and apply styles automatically.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ui_designer.designer_styles import StyleApplicator

def convert_ui_to_py(ui_file_path, output_path=None):
    """Convert a .ui file to Python using pyuic6"""
    
    if output_path is None:
        # Generate output path by replacing .ui with .py
        output_path = ui_file_path.replace('.ui', '_ui.py')
    
    try:
        # Try to use pyuic6 from virtual environment first
        venv_pyuic6 = project_root / '.venv' / 'Scripts' / 'pyuic6.exe'
        if venv_pyuic6.exists():
            cmd = [str(venv_pyuic6), '-o', output_path, ui_file_path]
        else:
            # Fallback to system pyuic6
            cmd = ['pyuic6', '-o', output_path, ui_file_path]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully converted {ui_file_path} to {output_path}")
            return True
        else:
            print(f"❌ Error converting {ui_file_path}: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ pyuic6 not found. Install with: pip install pyqt6-tools")
        return False

def convert_all_forms():
    """Convert all .ui files in the forms directory"""
    
    forms_dir = Path(__file__).parent / "forms"
    
    if not forms_dir.exists():
        print("❌ Forms directory not found")
        return
    
    ui_files = list(forms_dir.glob("*.ui"))
    
    if not ui_files:
        print("❌ No .ui files found in forms directory")
        return
    
    print(f"Found {len(ui_files)} .ui files to convert:")
    
    for ui_file in ui_files:
        print(f"\n🔄 Converting {ui_file.name}...")
        
        # Convert to Python
        output_file = forms_dir / f"{ui_file.stem}_ui.py"
        success = convert_ui_to_py(str(ui_file), str(output_file))
        
        if success:
            # Add style application helper to the generated file
            add_style_helper(output_file)

def add_style_helper(py_file_path):
    """Add style application helper methods to generated Python file"""
    
    try:
        with open(py_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add import for StyleApplicator
        import_line = "from ui_designer.designer_styles import StyleApplicator\n"
        
        if "class Ui_" in content:
            # Find the class definition
            lines = content.split('\n')
            
            # Add import at the top (after existing imports)
            import_inserted = False
            for i, line in enumerate(lines):
                if line.startswith('from PyQt6') and not import_inserted:
                    lines.insert(i, import_line)
                    import_inserted = True
                    break
            
            # Add style application method to the class
            for i, line in enumerate(lines):
                if line.strip().startswith('def retranslateUi('):
                    # Insert the apply_styles method before retranslateUi
                    style_method = [
                        "",
                        "    def apply_styles(self):",
                        "        \"\"\"Apply designer-friendly styles to widgets\"\"\"",
                        "        # Apply styles using StyleApplicator",
                        "        # Example usage:",
                        "        # StyleApplicator.apply_primary_button(self.save_btn)",
                        "        # StyleApplicator.apply_input_field(self.name_edit)",
                        "        # StyleApplicator.apply_table(self.table_widget)",
                        "        pass",
                        ""
                    ]
                    
                    for j, style_line in enumerate(style_method):
                        lines.insert(i + j, style_line)
                    break
            
            # Write back the modified content
            with open(py_file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            print(f"✅ Added style helper to {py_file_path}")
            
    except Exception as e:
        print(f"⚠️ Could not add style helper to {py_file_path}: {e}")

def create_example_usage():
    """Create example usage file showing how to use the generated forms"""
    
    example_content = '''"""
Example usage of generated UI forms with style application
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from ui_designer.forms.main_window_ui import Ui_MainWindow
from ui_designer.forms.person_dialog_ui import Ui_PersonDialog
from ui_designer.designer_styles import StyleApplicator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.apply_styles()
        
    def apply_styles(self):
        """Apply styles to the main window"""
        # Apply styles to buttons
        StyleApplicator.apply_primary_button(self.ui.add_person_btn)
        StyleApplicator.apply_secondary_button(self.ui.refresh_btn)
        
        # Apply styles to inputs
        StyleApplicator.apply_input_field(self.ui.search_field)
        StyleApplicator.apply_combo_box(self.ui.language_selector)
        
        # Apply styles to frames and tables
        StyleApplicator.apply_header_frame(self.ui.header_frame)
        StyleApplicator.apply_card_frame(self.ui.content_frame)
        StyleApplicator.apply_table(self.ui.people_table)
        
        # Apply styles to labels
        StyleApplicator.apply_title_label(self.ui.title_label)

class PersonDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PersonDialog()
        self.ui.setupUi(self)
        self.apply_styles()
        
    def apply_styles(self):
        """Apply styles to the person dialog"""
        # Apply dialog style
        StyleApplicator.apply_dialog_style(self)
        
        # Apply styles to buttons
        StyleApplicator.apply_primary_button(self.ui.save_btn)
        StyleApplicator.apply_secondary_button(self.ui.cancel_btn)
        
        # Apply styles to form elements
        StyleApplicator.apply_input_field(self.ui.name_edit)
        StyleApplicator.apply_input_field(self.ui.cnp_edit)
        StyleApplicator.apply_input_field(self.ui.phone_edit)
        StyleApplicator.apply_input_field(self.ui.email_edit)
        StyleApplicator.apply_text_area(self.ui.notes_edit)
        
        # Apply styles to frame and labels
        StyleApplicator.apply_card_frame(self.ui.form_frame)
        StyleApplicator.apply_title_label(self.ui.title_label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
'''
    
    example_file = Path(__file__).parent / "example_usage.py"
    with open(example_file, 'w', encoding='utf-8') as f:
        f.write(example_content)
    
    print(f"✅ Created example usage file: {example_file}")

def open_designer():
    """Open Qt Designer with the forms directory"""
    try:
        forms_dir = Path(__file__).parent / "forms"
        os.chdir(forms_dir)
        
        # Try PySide6 designer first (most reliable)
        venv_designer = project_root / '.venv' / 'Scripts' / 'pyside6-designer.exe'
        if venv_designer.exists():
            subprocess.Popen([str(venv_designer)])
            print("🎨 Opening Qt Designer (PySide6)...")
        else:
            # Try PyQt6 tools as fallback
            venv_qt_tools = project_root / '.venv' / 'Scripts' / 'pyqt6-tools.exe'
            if venv_qt_tools.exists():
                subprocess.Popen([str(venv_qt_tools), 'designer'])
                print("🎨 Opening Qt Designer (PyQt6 tools)...")
            else:
                # System fallback
                subprocess.Popen(['designer'])
                print("🎨 Opening Qt Designer (system)...")
        
        print(f"📁 Working directory: {forms_dir}")
        print("\n📝 To edit forms:")
        print("1. Open any .ui file in the forms directory")
        print("2. Make your changes in Qt Designer")
        print("3. Save the file")
        print("4. Run this script again to regenerate Python files")
        
    except FileNotFoundError:
        print("❌ Qt Designer not found.")
        print("💡 Install with: pip install PySide6")
        print("💡 Or install Qt Creator from: https://www.qt.io/download")
    except Exception as e:
        print(f"❌ Error opening Qt Designer: {e}")

def main():
    """Main function"""
    
    print("🎨 PyQt6 Designer Integration Tool")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "convert":
            convert_all_forms()
        elif command == "designer":
            open_designer()
        elif command == "example":
            create_example_usage()
        else:
            print("❌ Unknown command")
            print_usage()
    else:
        print_usage()

def print_usage():
    """Print usage information"""
    
    print("\n📖 Usage:")
    print("python ui_tools.py convert   - Convert all .ui files to Python")
    print("python ui_tools.py designer  - Open Qt Designer")
    print("python ui_tools.py example   - Create example usage file")
    
    print("\n🛠️ Workflow:")
    print("1. Run 'python ui_tools.py designer' to open Qt Designer")
    print("2. Edit .ui files in Qt Designer")
    print("3. Run 'python ui_tools.py convert' to generate Python files")
    print("4. Use StyleApplicator in your code to apply styles")
    
    print("\n📁 Directory Structure:")
    print("ui_designer/")
    print("├── forms/           # .ui files and generated .py files")
    print("├── designer_styles.py  # Style definitions")
    print("├── ui_tools.py      # This script")
    print("└── example_usage.py # Example implementation")

if __name__ == "__main__":
    main()
