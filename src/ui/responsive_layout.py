"""
Responsive Layout Manager for the Psychological Records application.
Provides adaptive layouts based on screen size and orientation.
"""

from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, 
                           QSizePolicy, QWidget, QScrollArea, QSplitter, QLabel)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt6.QtGui import QResizeEvent
from enum import Enum
from typing import List, Tuple, Optional, Dict, Any

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


class ResponsiveGridLayout(QGridLayout):
    """Grid layout that adapts to screen size and properly aligns items."""
    
    def __init__(self, columns=None, parent=None):
        super().__init__(parent)
        self.target_columns = columns or {}  # Size class -> column count mapping
        self.current_size_class = "md"
        self.items_data = []  # Store items with their grid properties
        
        # Default column configuration
        self.default_columns = {
            "xs": 1,  # Mobile: single column
            "sm": 2,  # Small tablet: two columns
            "md": 3,  # Tablet: three columns
            "lg": 4,  # Desktop: four columns
            "xl": 5   # Large desktop: five columns
        }
        
        # Configure default spacing and margins
        self.setSpacing(16)
        self.setContentsMargins(16, 16, 16, 16)
    
    def set_column_configuration(self, config: Dict[str, int]):
        """Set custom column configuration for different size classes."""
        self.target_columns.update(config)
        self._relayout()
    
    def add_grid_item(self, widget: QWidget, weight: int = 1, 
                      min_width: int = 200, preferred_width: int = 300):
        """Add an item to the grid with responsive properties."""
        item_data = {
            'widget': widget,
            'weight': weight,
            'min_width': min_width,
            'preferred_width': preferred_width,
            'original_size_policy': widget.sizePolicy()
        }
        self.items_data.append(item_data)
        
        # Set size policy for grid items
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        widget.setMinimumWidth(min_width)
        
        self._relayout()
    
    def remove_grid_item(self, widget: QWidget):
        """Remove an item from the grid."""
        self.items_data = [item for item in self.items_data if item['widget'] != widget]
        self.removeWidget(widget)
        self._relayout()
    
    def adapt_to_size_class(self, size_class: str):
        """Adapt the grid layout to the specified size class."""
        if size_class != self.current_size_class:
            self.current_size_class = size_class
            self._relayout()
            self._update_spacing()
    
    def _get_column_count(self) -> int:
        """Get the appropriate column count for current size class."""
        columns = self.target_columns.get(
            self.current_size_class, 
            self.default_columns.get(self.current_size_class, 3)
        )
        return max(1, min(columns, len(self.items_data)))
    
    def _relayout(self):
        """Recalculate and apply grid layout."""
        if not self.items_data:
            return
        
        # Clear current layout
        for i in reversed(range(self.count())):
            item = self.takeAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)
        
        # Calculate grid dimensions
        columns = self._get_column_count()
        total_items = len(self.items_data)
        rows = (total_items + columns - 1) // columns
        
        # Place items in grid
        for index, item_data in enumerate(self.items_data):
            widget = item_data['widget']
            row = index // columns
            col = index % columns
            
            # Set column stretch based on weight
            self.setColumnStretch(col, item_data['weight'])
            
            # Add widget to grid
            self.addWidget(widget, row, col)
            
            # Update widget properties based on size class
            self._update_widget_properties(widget, item_data)
        
        # Set row stretch for equal row heights
        for row in range(rows):
            self.setRowStretch(row, 1)
    
    def _update_widget_properties(self, widget: QWidget, item_data: Dict[str, Any]):
        """Update widget properties based on current size class."""
        if self.current_size_class in ["xs", "sm"]:
            # Mobile/small tablet: full width, smaller margins
            widget.setMinimumWidth(item_data['min_width'] // 2)
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        else:
            # Desktop: preferred width, larger margins
            widget.setMinimumWidth(item_data['min_width'])
            widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    
    def _update_spacing(self):
        """Update spacing based on size class."""
        spacing_map = {
            "xs": 8,   # Minimal spacing on mobile
            "sm": 12,  # Small spacing on small tablets
            "md": 16,  # Default spacing
            "lg": 20,  # Larger spacing on desktop
            "xl": 24   # Maximum spacing on large screens
        }
        
        spacing = spacing_map.get(self.current_size_class, 16)
        self.setSpacing(spacing)
        
        # Update margins
        margin = spacing
        self.setContentsMargins(margin, margin, margin, margin)


class GridResponsiveWidget(ResponsiveWidget):
    """Widget that uses responsive grid layout for its children."""
    
    def __init__(self, columns=None, parent=None):
        super().__init__(parent)
        self.grid_layout = ResponsiveGridLayout(columns, self)
        self.setLayout(self.grid_layout)
    
    def add_grid_item(self, widget: QWidget, weight: int = 1, 
                      min_width: int = 200, preferred_width: int = 300):
        """Add an item to the responsive grid."""
        self.grid_layout.add_grid_item(widget, weight, min_width, preferred_width)
    
    def remove_grid_item(self, widget: QWidget):
        """Remove an item from the responsive grid."""
        self.grid_layout.remove_grid_item(widget)
    
    def set_column_configuration(self, config: Dict[str, int]):
        """Set custom column configuration."""
        self.grid_layout.set_column_configuration(config)
    
    def adapt_to_layout_mode(self, mode):
        """Adapt to layout mode changes."""
        size_class = ResponsiveBreakpoints.get_size_class(self.width())
        self.grid_layout.adapt_to_size_class(size_class)


class FlexGridLayout(QGridLayout):
    """Advanced grid layout with flexible column and row management."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.flex_items = []  # Store items with flex properties
        self.column_weights = {}  # Column weight configuration
        self.row_weights = {}     # Row weight configuration
        self.auto_columns = True  # Automatically determine columns
        self.max_columns = 6      # Maximum columns for auto mode
        
        # Set default properties
        self.setSpacing(16)
        self.setContentsMargins(16, 16, 16, 16)
    
    def add_flex_item(self, widget: QWidget, flex_grow: float = 1.0, 
                      flex_shrink: float = 1.0, flex_basis: int = 200,
                      align_h: str = "stretch", align_v: str = "center"):
        """Add a flexible item to the grid.
        
        Args:
            widget: Widget to add
            flex_grow: How much the item should grow (relative to other items)
            flex_shrink: How much the item should shrink (relative to other items)
            flex_basis: Initial size preference in pixels
            align_h: Horizontal alignment ("left", "center", "right", "stretch")
            align_v: Vertical alignment ("top", "center", "bottom", "stretch")
        """
        flex_item = {
            'widget': widget,
            'flex_grow': flex_grow,
            'flex_shrink': flex_shrink,
            'flex_basis': flex_basis,
            'align_h': align_h,
            'align_v': align_v,
            'min_width': flex_basis // 2,
            'preferred_width': flex_basis
        }
        
        self.flex_items.append(flex_item)
        self._configure_widget_alignment(widget, align_h, align_v)
        self._relayout_flex()
    
    def remove_flex_item(self, widget: QWidget):
        """Remove a flexible item from the grid."""
        self.flex_items = [item for item in self.flex_items if item['widget'] != widget]
        self.removeWidget(widget)
        self._relayout_flex()
    
    def set_column_weights(self, weights: Dict[int, float]):
        """Set weights for specific columns."""
        self.column_weights.update(weights)
        self._apply_weights()
    
    def set_row_weights(self, weights: Dict[int, float]):
        """Set weights for specific rows."""
        self.row_weights.update(weights)
        self._apply_weights()
    
    def set_auto_columns(self, enabled: bool, max_columns: int = 6):
        """Enable/disable automatic column management."""
        self.auto_columns = enabled
        self.max_columns = max_columns
        self._relayout_flex()
    
    def _configure_widget_alignment(self, widget: QWidget, align_h: str, align_v: str):
        """Configure widget alignment and size policy."""
        # Horizontal size policy
        if align_h == "stretch":
            h_policy = QSizePolicy.Policy.Expanding
        elif align_h in ["left", "right"]:
            h_policy = QSizePolicy.Policy.Fixed
        else:  # center
            h_policy = QSizePolicy.Policy.Preferred
        
        # Vertical size policy
        if align_v == "stretch":
            v_policy = QSizePolicy.Policy.Expanding
        elif align_v in ["top", "bottom"]:
            v_policy = QSizePolicy.Policy.Fixed
        else:  # center
            v_policy = QSizePolicy.Policy.Preferred
        
        widget.setSizePolicy(h_policy, v_policy)
    
    def _relayout_flex(self):
        """Recalculate and apply flexible grid layout."""
        if not self.flex_items:
            return
        
        # Clear current layout
        for i in reversed(range(self.count())):
            item = self.takeAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)
        
        # Calculate optimal grid dimensions
        if self.auto_columns:
            columns = self._calculate_optimal_columns()
        else:
            columns = self.max_columns
        
        # Place items and apply flex properties
        for index, flex_item in enumerate(self.flex_items):
            widget = flex_item['widget']
            row = index // columns
            col = index % columns
            
            # Calculate size based on flex properties
            self._apply_flex_sizing(widget, flex_item, columns)
            
            # Add to grid with alignment
            alignment = self._get_qt_alignment(flex_item['align_h'], flex_item['align_v'])
            self.addWidget(widget, row, col, alignment)
            
            # Set column stretch based on flex_grow
            current_stretch = self.columnStretch(col)
            new_stretch = max(current_stretch, int(flex_item['flex_grow'] * 100))
            self.setColumnStretch(col, new_stretch)
        
        # Apply custom weights
        self._apply_weights()
    
    def _calculate_optimal_columns(self) -> int:
        """Calculate the optimal number of columns based on items and space."""
        total_items = len(self.flex_items)
        
        if total_items <= 2:
            return min(total_items, 2)
        elif total_items <= 6:
            return min(total_items, 3)
        elif total_items <= 12:
            return min(total_items // 2, 4)
        else:
            return min(self.max_columns, 5)
    
    def _apply_flex_sizing(self, widget: QWidget, flex_item: Dict[str, Any], columns: int):
        """Apply flex sizing properties to a widget."""
        basis = flex_item['flex_basis']
        grow = flex_item['flex_grow']
        shrink = flex_item['flex_shrink']
        
        # Calculate minimum and preferred widths
        min_width = max(basis // 2, int(basis * shrink))
        preferred_width = int(basis * grow)
        
        widget.setMinimumWidth(min_width)
        if preferred_width > min_width:
            widget.resize(preferred_width, widget.height())
    
    def _get_qt_alignment(self, align_h: str, align_v: str) -> Qt.AlignmentFlag:
        """Convert alignment strings to Qt alignment flags."""
        h_align = {
            "left": Qt.AlignmentFlag.AlignLeft,
            "center": Qt.AlignmentFlag.AlignHCenter,
            "right": Qt.AlignmentFlag.AlignRight,
            "stretch": Qt.AlignmentFlag.AlignHCenter
        }.get(align_h, Qt.AlignmentFlag.AlignHCenter)
        
        v_align = {
            "top": Qt.AlignmentFlag.AlignTop,
            "center": Qt.AlignmentFlag.AlignVCenter,
            "bottom": Qt.AlignmentFlag.AlignBottom,
            "stretch": Qt.AlignmentFlag.AlignVCenter
        }.get(align_v, Qt.AlignmentFlag.AlignVCenter)
        
        return h_align | v_align
    
    def _apply_weights(self):
        """Apply custom column and row weights."""
        for col, weight in self.column_weights.items():
            self.setColumnStretch(col, int(weight * 100))
        
        for row, weight in self.row_weights.items():
            self.setRowStretch(row, int(weight * 100))
