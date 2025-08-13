# Refactored Styling Architecture

## Overview
The PyQt6 application now uses a comprehensive, centralized styling system that eliminates hardcoded values and provides consistent, maintainable design patterns.

## Architecture Components

### 1. Core Styling Classes

#### Colors
- **Primary palette**: Blue theme with hover/pressed states
- **Success palette**: Green theme for positive actions
- **Background/Surface**: Neutral grays for layouts
- **Text colors**: Primary, secondary, muted text hierarchy
- **Border colors**: Light to lighter border variations

#### Typography
- **Font family**: 'Segoe UI', Arial, sans-serif
- **Font sizes**: Relative em units (0.75em, 1em, 1.25em)
- **Font weights**: Normal (500), Semibold (600), Bold (700)

#### Spacing System
- **XS to XXXL**: 0.375em to 2.1875em (6px to 35px equivalent)
- **Consistent scaling**: All based on 16px base font size
- **Relative units**: Scales with system font changes

#### UIDimensions
- **Dialog dimensions**: 37.5em x 34.375em (600x550px equivalent)
- **Component sizing**: Standardized widths and heights
- **Layout values**: Form spacing and margins

### 2. StyleSheets Class - Component Definitions

#### Core Components
- `dialog()`: Base dialog styling
- `input_field()`: Standardized input field appearance
- `label()`: Consistent label styling
- `combo_box()`: Complete dropdown styling with hover states

#### Button Variants
- `primary_button()`: Standard primary action buttons
- `primary_button_wide()`: Extended width for longer text
- `success_button()`: Success/confirmation actions

#### Layout Components
- `tab_widget()`: Tab interface styling
- `form_layout()`: Form spacing and margins

### 3. WidgetStyles Class - Application Methods

#### Button Appliers
```python
WidgetStyles.apply_primary_button(button)        # Standard primary button
WidgetStyles.apply_primary_button_wide(button)   # Wide primary button
WidgetStyles.apply_success_button(button)        # Success button
```

#### Layout Appliers
```python
WidgetStyles.apply_form_layout(layout)           # Form spacing/margins
WidgetStyles.apply_dialog_dimensions(dialog)     # Standard dialog size
WidgetStyles.apply_combo_sizing(combo)           # Combo box dimensions
```

#### Specialized Appliers
```python
WidgetStyles.apply_title_label(label)            # Title styling
WidgetStyles.apply_language_label(label)         # Language selector label
WidgetStyles.apply_dialog_style(dialog)          # Complete dialog styling
```

## Refactoring Benefits

### 1. Consistency
- All components use the same color palette
- Standardized spacing and typography
- Consistent interaction patterns (hover, focus, pressed states)

### 2. Maintainability
- Single source of truth for all styling
- Easy to update colors/fonts globally
- Clear separation between styling logic and UI logic

### 3. Scalability
- Relative units scale with system preferences
- Easy to add new component variants
- Consistent patterns for new widgets

### 4. Accessibility
- Better contrast ratios
- Scalable fonts for vision accessibility
- Consistent focus indicators

## Usage Patterns

### Before Refactoring
```python
# Hardcoded values scattered throughout code
layout.setSpacing(20)
layout.setContentsMargins(30, 20, 30, 20)
button.setStyleSheet("background-color: #0d6efd; padding: 16px 32px; ...")
```

### After Refactoring
```python
# Centralized, semantic styling
WidgetStyles.apply_form_layout(layout)
WidgetStyles.apply_primary_button(button)
```

## Component Guidelines

### Adding New Components
1. Define styles in `StyleSheets` class
2. Create applier method in `WidgetStyles` class
3. Use existing color/spacing constants
4. Follow relative unit patterns

### Customizing Existing Components
1. Check if variant already exists (e.g., `primary_button_wide`)
2. Create new variant if needed
3. Extend existing base styles when possible
4. Document new patterns

## File Structure
```
src/ui/styles.py              # Core styling system
login_dialog.py               # Refactored to use centralized styles
styling_architecture.md       # This documentation
styling_conversion_reference.md # Pixel to em conversion reference
```

## Migration Status

### ✅ Completed
- login_dialog.py: Fully refactored to use centralized styling
- Core styling system: Complete with relative units
- Button variants: Standard and wide primary buttons
- Layout management: Centralized spacing and dimensions

### 🔄 Next Steps
- Apply centralized styling to remaining dialogs:
  - main_window.py
  - person_dialog.py
  - assessment_dialog.py
  - consultation_dialog.py
  - change_password_dialog.py

### 📋 Future Enhancements
- Dark/light theme support
- Custom color scheme options
- Dynamic font size adjustment
- High contrast accessibility themes
