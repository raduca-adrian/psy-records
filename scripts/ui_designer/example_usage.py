"""
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
