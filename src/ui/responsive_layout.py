"""
Responsive Layout Manager for the Psychological Records application.
Provides adaptive layouts based on screen size and orientation.
"""

from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, 
                           QSizePolicy, QWidget, QScrollArea, QSplitter)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt6.QtGui import QResizeEvent
from enum import Enum

class LayoutMode(Enum):
    COMPACT = "compact"      # Mobile/small screens
    STANDARD = "standard"    # Desktop/medium screens  
    EXPANDED = "expanded"    # Large screens/wide displays

class ResponsiveWidget(QWidget):
    """Base widget that responds to size changes and layout modes."""
    
    layout_mode_changed = pyqtSignal(LayoutMode)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_layout_mode = LayoutMode.STANDARD
        self.min_compact_width = 600
        self.min_expanded_width = 1200
        
    def resizeEvent(self, event: QResizeEvent):
        """Handle resize events and update layout mode if necessary."""
        super().resizeEvent(event)
        self.update_layout_mode(event.size())
    
    def update_layout_mode(self, size: QSize):
        """Update layout mode based on widget size."""
        width = size.width()
        
        if width < self.min_compact_width:
            new_mode = LayoutMode.COMPACT
        elif width < self.min_expanded_width:
            new_mode = LayoutMode.STANDARD
        else:
            new_mode = LayoutMode.EXPANDED
            
        if new_mode != self.current_layout_mode:
            self.current_layout_mode = new_mode
            self.layout_mode_changed.emit(new_mode)
            self.adapt_to_layout_mode(new_mode)
    
    def adapt_to_layout_mode(self, mode: LayoutMode):
        """Override this method to adapt widget to new layout mode."""
        pass

class ResponsiveContainer(ResponsiveWidget):
    """Container widget that manages responsive layout of child widgets."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_layouts()
        
    def setup_layouts(self):
        """Setup different layouts for different modes."""
        # Main stacked widget to switch between layouts
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create different layout containers
        self.compact_container = QWidget()
        self.standard_container = QWidget()
        self.expanded_container = QWidget()
        
        # Initially show standard layout
        self.main_layout.addWidget(self.standard_container)
        
    def adapt_to_layout_mode(self, mode: LayoutMode):
        """Switch to appropriate layout for the mode."""
        # Clear current layout
        for i in reversed(range(self.main_layout.count())):
            child = self.main_layout.takeAt(i).widget()
            if child:
                child.setParent(None)
        
        # Add appropriate container
        if mode == LayoutMode.COMPACT:
            self.main_layout.addWidget(self.compact_container)
            self.setup_compact_layout()
        elif mode == LayoutMode.STANDARD:
            self.main_layout.addWidget(self.standard_container)
            self.setup_standard_layout()
        else:  # EXPANDED
            self.main_layout.addWidget(self.expanded_container)
            self.setup_expanded_layout()
    
    def setup_compact_layout(self):
        """Setup layout for compact mode (mobile-like)."""
        pass
    
    def setup_standard_layout(self):
        """Setup layout for standard mode (desktop)."""
        pass
    
    def setup_expanded_layout(self):
        """Setup layout for expanded mode (wide screens)."""
        pass

class FlexibleLayout:
    """Utility class for creating flexible, responsive layouts."""
    
    @staticmethod
    def create_header_layout(title_widget, actions_widgets=None, responsive=True):
        """Create a responsive header layout."""
        header_frame = QFrame()
        header_frame.setProperty("class", "header")
        header_layout = QVBoxLayout(header_frame) if responsive else QHBoxLayout(header_frame)
        
        if responsive:
            # Responsive: stack on small screens, side-by-side on large
            title_container = QWidget()
            title_layout = QHBoxLayout(title_container)
            title_layout.addWidget(title_widget)
            title_layout.addStretch()
            
            if actions_widgets:
                actions_container = QWidget()
                actions_layout = QHBoxLayout(actions_container)
                for widget in actions_widgets:
                    actions_layout.addWidget(widget)
                actions_layout.addStretch()
                
                header_layout.addWidget(title_container)
                header_layout.addWidget(actions_container)
            else:
                header_layout.addWidget(title_container)
        else:
            # Fixed horizontal layout
            header_layout.addWidget(title_widget)
            header_layout.addStretch()
            if actions_widgets:
                for widget in actions_widgets:
                    header_layout.addWidget(widget)
        
        return header_frame
    
    @staticmethod
    def create_card_layout(widgets, title=None, max_columns=3):
        """Create a responsive card layout."""
        container = QFrame()
        container.setProperty("class", "card")
        
        if title:
            main_layout = QVBoxLayout(container)
            title_label = QLabel(title)
            title_label.setProperty("class", "subtitle")
            main_layout.addWidget(title_label)
            
            cards_widget = QWidget()
            cards_layout = QGridLayout(cards_widget)
            main_layout.addWidget(cards_widget)
        else:
            cards_layout = QGridLayout(container)
        
        # Arrange widgets in responsive grid
        for i, widget in enumerate(widgets):
            row = i // max_columns
            col = i % max_columns
            cards_layout.addWidget(widget, row, col)
        
        return container
    
    @staticmethod
    def create_sidebar_layout(sidebar_widget, main_widget, sidebar_width=250):
        """Create a responsive sidebar layout."""
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Configure sidebar
        sidebar_widget.setMinimumWidth(200)
        sidebar_widget.setMaximumWidth(400)
        sidebar_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        
        # Configure main area
        main_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        splitter.addWidget(sidebar_widget)
        splitter.addWidget(main_widget)
        splitter.setSizes([sidebar_width, 800])  # Default sizes
        
        return splitter
    
    @staticmethod
    def create_button_group(buttons, orientation=Qt.Orientation.Horizontal, responsive=True):
        """Create a responsive button group."""
        container = QWidget()
        
        if responsive:
            # Use QVBoxLayout for small screens, QHBoxLayout for large screens
            layout = QHBoxLayout(container)  # Default to horizontal
            layout.setSpacing(8)
            
            for button in buttons:
                button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
                layout.addWidget(button)
            
            layout.addStretch()
        else:
            if orientation == Qt.Orientation.Horizontal:
                layout = QHBoxLayout(container)
            else:
                layout = QVBoxLayout(container)
            
            for button in buttons:
                layout.addWidget(button)
        
        return container
    
    @staticmethod
    def create_form_layout(form_items, columns=1):
        """Create a responsive form layout."""
        container = QWidget()
        layout = QGridLayout(container)
        layout.setSpacing(16)
        
        for i, (label, widget) in enumerate(form_items):
            row = i // columns
            col = (i % columns) * 2
            
            if isinstance(label, str):
                from PyQt6.QtWidgets import QLabel
                label_widget = QLabel(label)
                label_widget.setProperty("class", "form-label")
            else:
                label_widget = label
            
            layout.addWidget(label_widget, row, col)
            layout.addWidget(widget, row, col + 1)
        
        return container
    
    @staticmethod
    def make_scrollable(widget, vertical=True, horizontal=False):
        """Make a widget scrollable."""
        scroll_area = QScrollArea()
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        
        if vertical and horizontal:
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        elif vertical:
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        return scroll_area

class ResponsiveBreakpoints:
    """Defines responsive breakpoints for the application."""
    
    # Screen size breakpoints (width in pixels)
    XS = 576   # Extra small devices (phones)
    SM = 768   # Small devices (tablets)
    MD = 992   # Medium devices (small laptops)
    LG = 1200  # Large devices (laptops/desktops)
    XL = 1400  # Extra large devices (large desktops)
    
    @classmethod
    def get_size_class(cls, width):
        """Get size class for given width."""
        if width < cls.XS:
            return "xs"
        elif width < cls.SM:
            return "sm"
        elif width < cls.MD:
            return "md"
        elif width < cls.LG:
            return "lg"
        else:
            return "xl"
    
    @classmethod
    def is_mobile(cls, width):
        """Check if width is considered mobile."""
        return width < cls.SM
    
    @classmethod
    def is_tablet(cls, width):
        """Check if width is considered tablet."""
        return cls.SM <= width < cls.MD
    
    @classmethod
    def is_desktop(cls, width):
        """Check if width is considered desktop."""
        return width >= cls.MD

class LayoutUtils:
    """Utility functions for layout management."""
    
    @staticmethod
    def set_responsive_margins(layout, size_class):
        """Set responsive margins based on size class."""
        if size_class in ["xs", "sm"]:
            margins = (8, 8, 8, 8)
        elif size_class == "md":
            margins = (16, 16, 16, 16)
        else:
            margins = (24, 24, 24, 24)
        
        layout.setContentsMargins(*margins)
    
    @staticmethod
    def set_responsive_spacing(layout, size_class):
        """Set responsive spacing based on size class."""
        if size_class in ["xs", "sm"]:
            spacing = 8
        elif size_class == "md":
            spacing = 12
        else:
            spacing = 16
        
        layout.setSpacing(spacing)
    
    @staticmethod
    def apply_responsive_properties(widget, size_class):
        """Apply responsive properties to a widget."""
        if hasattr(widget, 'layout') and widget.layout():
            LayoutUtils.set_responsive_margins(widget.layout(), size_class)
            LayoutUtils.set_responsive_spacing(widget.layout(), size_class)
