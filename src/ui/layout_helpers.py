"""
Enhanced layout helpers for improved UI visibility and spacing.
This module provides utilities to create well-spaced, readable layouts.
"""

from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QScrollArea, QWidget, QFrame, QGroupBox)
from PyQt6.QtCore import Qt
from .styles import UIDimensions, WidgetStyles


class LayoutManager:
    """Provides enhanced layout management with improved spacing and visibility."""
    
    @staticmethod
    def create_form_layout(spacing=None, margins=None):
        """Create a form layout with improved spacing and margins."""
        layout = QFormLayout()
        
        # Apply enhanced spacing
        spacing = spacing or UIDimensions.FORM_SPACING_PX
        layout.setVerticalSpacing(spacing)
        layout.setHorizontalSpacing(spacing // 2)
        
        # Apply enhanced margins
        if margins is None:
            layout.setContentsMargins(
                UIDimensions.FORM_MARGIN_H_PX,
                UIDimensions.FORM_MARGIN_V_PX,
                UIDimensions.FORM_MARGIN_H_PX,
                UIDimensions.FORM_MARGIN_V_PX
            )
        else:
            layout.setContentsMargins(*margins)
            
        return layout
    
    @staticmethod
    def create_vertical_layout(spacing=None, margins=None):
        """Create a vertical layout with improved spacing."""
        layout = QVBoxLayout()
        
        spacing = spacing or UIDimensions.SECTION_SPACING_PX
        layout.setSpacing(spacing)
        
        if margins is None:
            layout.setContentsMargins(
                UIDimensions.FORM_MARGIN_H_PX,
                UIDimensions.FORM_MARGIN_V_PX,
                UIDimensions.FORM_MARGIN_H_PX,
                UIDimensions.FORM_MARGIN_V_PX
            )
        else:
            layout.setContentsMargins(*margins)
            
        return layout
    
    @staticmethod
    def create_horizontal_layout(spacing=None, margins=None):
        """Create a horizontal layout with improved spacing."""
        layout = QHBoxLayout()
        
        spacing = spacing or UIDimensions.BUTTON_SPACING_PX
        layout.setSpacing(spacing)
        
        if margins is None:
            layout.setContentsMargins(
                UIDimensions.FORM_MARGIN_H_PX,
                UIDimensions.FORM_MARGIN_V_PX,
                UIDimensions.FORM_MARGIN_H_PX,
                UIDimensions.FORM_MARGIN_V_PX
            )
        else:
            layout.setContentsMargins(*margins)
            
        return layout
    
    @staticmethod
    def create_scrollable_area(content_widget, min_width=None, min_height=None):
        """Create a scrollable area with proper content sizing."""
        scroll_area = QScrollArea()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Set minimum sizes if provided
        if min_width:
            scroll_area.setMinimumWidth(min_width)
        if min_height:
            scroll_area.setMinimumHeight(min_height)
            
        # Apply styling for better visibility
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        return scroll_area
    
    @staticmethod
    def create_section_group(title, content_layout=None):
        """Create a grouped section with title and content."""
        group_box = QGroupBox(title)
        
        if content_layout is None:
            content_layout = LayoutManager.create_vertical_layout()
            
        group_box.setLayout(content_layout)
        
        # Apply enhanced styling
        group_box.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 1.1em;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 0.5em;
                padding-top: 1em;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 0.5em;
                padding: 0.25em 0.5em;
                background-color: white;
                border-radius: 4px;
            }}
        """)
        
        return group_box, content_layout
    
    @staticmethod
    def add_stretch_to_layout(layout, stretch_factor=1):
        """Add stretch to a layout for better space distribution."""
        if hasattr(layout, 'addStretch'):
            layout.addStretch(stretch_factor)
    
    @staticmethod
    def create_button_row(buttons, alignment=Qt.AlignmentFlag.AlignRight):
        """Create a horizontal layout for buttons with proper spacing."""
        button_layout = LayoutManager.create_horizontal_layout(
            spacing=UIDimensions.BUTTON_SPACING_PX,
            margins=(0, 0, 0, 0)
        )
        
        # Add stretch before buttons if right-aligned
        if alignment == Qt.AlignmentFlag.AlignRight:
            button_layout.addStretch()
            
        for button in buttons:
            button_layout.addWidget(button)
            
        # Add stretch after buttons if left-aligned
        if alignment == Qt.AlignmentFlag.AlignLeft:
            button_layout.addStretch()
            
        return button_layout


class TabContentHelper:
    """Helper for creating well-structured tab content."""
    
    @staticmethod
    def create_tab_content(main_layout_type='vertical'):
        """Create a properly structured tab content widget."""
        content_widget = QWidget()
        
        if main_layout_type == 'vertical':
            main_layout = LayoutManager.create_vertical_layout()
        elif main_layout_type == 'horizontal':
            main_layout = LayoutManager.create_horizontal_layout()
        else:  # form
            main_layout = LayoutManager.create_form_layout()
            
        content_widget.setLayout(main_layout)
        
        # Apply tab content padding
        WidgetStyles.apply_tab_content_padding(content_widget)
        
        return content_widget, main_layout
    
    @staticmethod
    def wrap_in_scroll_area(content_widget, min_height=300):
        """Wrap content in a scroll area if needed."""
        return LayoutManager.create_scrollable_area(
            content_widget, 
            min_height=min_height
        )


class ResponsiveLayout:
    """Provides responsive layout capabilities."""
    
    @staticmethod
    def create_responsive_form(fields, columns=1):
        """Create a responsive form that adapts to different sizes."""
        if columns == 1:
            return LayoutManager.create_form_layout()
        
        # For multi-column layouts
        main_layout = LayoutManager.create_horizontal_layout()
        
        fields_per_column = len(fields) // columns
        remainder = len(fields) % columns
        
        start_idx = 0
        for col in range(columns):
            column_layout = LayoutManager.create_form_layout()
            
            # Calculate how many fields in this column
            fields_in_col = fields_per_column + (1 if col < remainder else 0)
            end_idx = start_idx + fields_in_col
            
            # Add fields to this column
            for i in range(start_idx, end_idx):
                if i < len(fields):
                    label, widget = fields[i]
                    column_layout.addRow(label, widget)
            
            main_layout.addLayout(column_layout)
            start_idx = end_idx
            
        return main_layout
