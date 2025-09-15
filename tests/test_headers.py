#!/usr/bin/env python3
"""
Test script to verify table header visibility
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class TestHeaderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Header Test")
        self.setGeometry(100, 100, 600, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create test table
        table = QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(3)
        
        # Set headers
        headers = ["ID", "Name", "CNP", "Date"]
        table.setHorizontalHeaderLabels(headers)
        
        # Configure header visibility
        header = table.horizontalHeader()
        header.setVisible(True)
        header.setMinimumHeight(40)
        
        # Add some test data
        from PyQt6.QtWidgets import QTableWidgetItem
        for row in range(3):
            for col in range(4):
                item = QTableWidgetItem(f"Row{row}Col{col}")
                table.setItem(row, col, item)
        
        # Apply enhanced header styling
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 8px;
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
                text-align: center;
            }
            QHeaderView::section:hover {
                background-color: #0b5ed7;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
        """)
        
        layout.addWidget(table)

def main():
    app = QApplication(sys.argv)
    window = TestHeaderWindow()
    window.show()
    
    print("Table header test window created.")
    print("Headers should be visible with blue background and white text.")
    print("Check if the headers 'ID', 'Name', 'CNP', 'Date' are clearly visible.")
    
    # Don't start event loop, just show the window
    window.show()
    
    return app, window

if __name__ == "__main__":
    app, window = main()
    sys.exit(app.exec())
