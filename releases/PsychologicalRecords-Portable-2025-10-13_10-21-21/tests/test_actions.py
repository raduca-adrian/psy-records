#!/usr/bin/env python3
"""
Test script to verify action buttons in table widgets
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QVBoxLayout, 
                           QWidget, QPushButton, QHBoxLayout, QTableWidgetItem)
from PyQt6.QtCore import Qt

class TestActionsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Action Buttons Test")
        self.setGeometry(100, 100, 800, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create test table
        table = QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(3)
        
        # Set headers
        headers = ["Name", "Date", "Description", "Actions"]
        table.setHorizontalHeaderLabels(headers)
        
        # Configure table
        header = table.horizontalHeader()
        header.setVisible(True)
        header.setMinimumHeight(40)
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)
        header.setSectionResizeMode(1, header.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, header.ResizeMode.Stretch)
        header.setSectionResizeMode(3, header.ResizeMode.Fixed)
        header.resizeSection(3, 180)  # Actions column width
        
        # Set row height
        table.verticalHeader().setDefaultSectionSize(50)
        table.verticalHeader().setVisible(False)
        
        # Add test data with action buttons
        for row in range(3):
            # Add data items
            table.setItem(row, 0, QTableWidgetItem(f"Item {row + 1}"))
            table.setItem(row, 1, QTableWidgetItem("2025-08-16"))
            table.setItem(row, 2, QTableWidgetItem(f"Description for item {row + 1}"))
            
            # Create action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(8, 4, 8, 4)
            actions_layout.setSpacing(6)
            
            edit_btn = QPushButton("✏️ Edit")
            edit_btn.setStyleSheet("""
                QPushButton { 
                    min-width: 70px; 
                    max-width: 80px;
                    padding: 8px 12px; 
                    font-size: 12px;
                    background-color: #0d6efd !important;
                    color: white !important;
                    border: 2px solid #0d6efd !important;
                    border-radius: 6px;
                    font-weight: 600;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7 !important;
                    border-color: #0b5ed7 !important;
                }
            """)
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_item(r))
            
            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setStyleSheet("""
                QPushButton { 
                    min-width: 70px; 
                    max-width: 80px;
                    padding: 8px 12px; 
                    font-size: 12px; 
                    background-color: #dc3545 !important;
                    color: white !important;
                    border: 2px solid #dc3545 !important;
                    border-radius: 6px;
                    font-weight: 600;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #bb2d3b !important;
                    border-color: #bb2d3b !important;
                }
            """)
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_item(r))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            
            table.setCellWidget(row, 3, actions_widget)
        
        # Apply table styling
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                gridline-color: #dee2e6;
            }
            QHeaderView::section {
                background-color: #0d6efd;
                color: white;
                padding: 12px 8px;
                border: none;
                border-right: 1px solid #495057;
                font-weight: 700;
                font-size: 14px;
                min-height: 40px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QTableWidget QWidget {
                background-color: transparent;
            }
        """)
        
        layout.addWidget(table)
    
    def edit_item(self, row):
        print(f"Edit button clicked for row {row}")
    
    def delete_item(self, row):
        print(f"Delete button clicked for row {row}")

def main():
    app = QApplication(sys.argv)
    window = TestActionsWindow()
    window.show()
    
    print("Action buttons test window created.")
    print("You should see:")
    print("1. Blue 'Edit' buttons in the Actions column")
    print("2. Red 'Delete' buttons in the Actions column")
    print("3. Both buttons should be clearly visible and clickable")
    print("4. Buttons should respond to hover effects")
    
    return app, window

if __name__ == "__main__":
    app, window = main()
    sys.exit(app.exec())
