# Material Design Theme System

## Overview

The Psychological Records application now features a comprehensive Material Design theme system with support for both **Light** and **Dark** modes. The implementation follows Google's Material Design guidelines for colors, typography, spacing, and elevation.

## Features

### 🎨 Dual Theme Support

#### Light Theme
- **Background**: `#FAFAFA` - Soft gray background
- **Surface**: `#FFFFFF` - Pure white surfaces
- **Primary**: `#2196F3` - Material Blue
- **Accent**: `#4CAF50` - Material Green
- **Text**: Dark gray to black tones

#### Dark Theme  
- **Background**: `#121212` - Near black background
- **Surface**: `#1E1E1E` - Dark gray surfaces
- **Primary**: `#64B5F6` - Light blue
- **Accent**: `#81C784` - Light green
- **Text**: White to light gray tones

### 🔄 Theme Toggle

The theme can be toggled in multiple ways:

1. **Status Bar Button**: Click the theme toggle button in the bottom-right corner
2. **Keyboard Shortcut**: Press `Ctrl+T`
3. **Persistent**: Your theme preference is automatically saved and restored

### 📐 Material Design Components

All UI components follow Material Design specifications:

#### Buttons
- **Elevation**: Raised with shadow effects
- **States**: Hover, pressed, and disabled states
- **Types**: Primary, secondary, and text buttons
- **Typography**: Uppercase text with letter spacing

#### Cards
- **Rounded corners**: 8px radius
- **Elevation**: Level 2 shadow
- **Padding**: 20px consistent spacing

#### Inputs
- **Outlined style**: 1px border, 2px on focus
- **Focus color**: Primary blue
- **Rounded corners**: 4px radius
- **Placeholder text**: Hint color

#### Tables
- **Header**: Bold, uppercase text with bottom border
- **Selection**: Highlighted background
- **Hover**: Subtle background change
- **Gridlines**: Divider color

#### Tabs
- **Indicator**: 3px bottom border on active tab
- **Hover**: Background color change
- **Icons**: Emoji icons for visual identification
- **Spacing**: Generous padding (12px × 24px)

## Color Palette

### Light Theme Colors

```python
Primary: #2196F3      # Material Blue
  - Dark: #1976D2
  - Light: #BBDEFB

Accent: #4CAF50       # Material Green
  - Dark: #388E3C
  - Light: #C8E6C9

Background: #FAFAFA   # Light gray
Surface: #FFFFFF      # White
Card: #FFFFFF         # White

Text:
  - Primary: #212121    # Almost black
  - Secondary: #757575  # Medium gray
  - Disabled: #BDBDBD   # Light gray
  - Hint: #9E9E9E       # Placeholder

Borders: #E0E0E0      # Light gray
Divider: #EEEEEE      # Very light gray
```

### Dark Theme Colors

```python
Primary: #64B5F6      # Light Blue
  - Dark: #42A5F5
  - Light: #90CAF9

Accent: #81C784       # Light Green
  - Dark: #66BB6A
  - Light: #A5D6A7

Background: #121212   # Near black
Surface: #1E1E1E      # Dark gray
Card: #2C2C2C         # Medium gray

Text:
  - Primary: #FFFFFF    # White
  - Secondary: #B0B0B0  # Light gray
  - Disabled: #6B6B6B   # Medium gray
  - Hint: #808080       # Dim gray

Borders: #404040      # Dark gray
Divider: #333333      # Very dark gray
```

## Typography

### Font Sizes
- **H1**: 28px, weight 600
- **H2**: 22px, weight 600
- **H3**: 18px, weight 600
- **Body**: 14px, weight 400
- **Button**: 14px, weight 500, uppercase

### Font Weights
- **Regular**: 400
- **Medium**: 500
- **Semi-bold**: 600
- **Bold**: 700

### Letter Spacing
- **Headers**: 0.5px
- **Buttons**: 0.5px
- **Table Headers**: 0.5px

## Spacing

Following the 4px baseline grid:

- **Micro**: 4px
- **Small**: 8px
- **Medium**: 12px
- **Large**: 16px
- **XL**: 20px
- **XXL**: 24px

## Elevation System

Material Design uses elevation to create depth and hierarchy:

- **Level 0**: No shadow (flat surface)
- **Level 2**: Card elevation (standard)
- **Level 8**: Raised components
- **Level 24**: Dialogs and modals

### Implementation

```python
from src.utils.material_elevation import apply_card_elevation

# Apply to any widget
apply_card_elevation(my_widget, dark_mode=False)
```

## Component States

### Interactive Elements

All interactive elements have clear visual feedback:

1. **Default**: Normal state
2. **Hover**: Color lightens/darkens slightly
3. **Pressed**: Deeper color, slight position shift
4. **Disabled**: Grayed out appearance
5. **Focus**: Primary color border

### Example: Button States

```css
Default: #2196F3
Hover: #1976D2
Pressed: #0D47A1 (with 1px shift)
Disabled: #BDBDBD
```

## Keyboard Shortcut Update

The theme toggle has been added to keyboard shortcuts:

| Shortcut | Action |
|----------|--------|
| **Ctrl+T** | Toggle theme (Light ⇄ Dark) |

## Usage

### In Code

```python
# Toggle theme programmatically
window.toggle_theme()

# Apply specific theme
window.apply_theme("dark")
window.apply_theme("light")

# Check current theme
if window.current_theme == "dark":
    print("Dark mode active")
```

### Theme Persistence

The theme preference is automatically saved using `QSettings`:

```python
settings = QSettings('PsychologicalRecords', 'UnifiedApp')
theme = settings.value('theme', 'light')  # Default to light
```

## Customization

### Modifying Colors

Edit `src/utils/material_theme.py`:

```python
# Light theme colors
LIGHT_THEME = MaterialColors(
    primary="#YOUR_COLOR",
    # ... other colors
)

# Dark theme colors
DARK_THEME = MaterialColors(
    primary="#YOUR_COLOR",
    # ... other colors
)
```

### Adding New Components

To style a new component:

1. Add styles to `get_material_stylesheet()` in `material_theme.py`
2. Use both light and dark theme colors
3. Include all states (hover, pressed, disabled, focus)

### Creating Custom Themes

You can create additional theme variants:

```python
# In material_theme.py
BLUE_THEME = MaterialColors(
    primary="#1E88E5",
    accent="#00ACC1",
    # ... define all colors
)

# Update get_material_stylesheet to support new theme
def get_material_stylesheet(theme: Literal["light", "dark", "blue"]):
    if theme == "blue":
        colors = BLUE_THEME
    # ...
```

## Best Practices

### When Designing New UI

1. **Use semantic colors**: primary, accent, surface, etc.
2. **Follow elevation hierarchy**: Higher importance = higher elevation
3. **Maintain consistency**: Use existing component patterns
4. **Test both themes**: Ensure readability in light and dark
5. **Use proper spacing**: Follow the 4px grid
6. **Provide feedback**: All interactions should have visual response

### Accessibility

- **Contrast ratio**: Maintained at WCAG AA standards
- **Focus indicators**: Clear visual focus on all interactive elements
- **Color independence**: Information not conveyed by color alone
- **Keyboard navigation**: Full keyboard support

## Technical Implementation

### File Structure

```
src/
├── utils/
│   ├── material_theme.py        # Theme system and stylesheets
│   ├── material_elevation.py    # Elevation/shadow effects
│   └── ...
└── ui/
    └── unified_main_window.py   # Main window with theme support
```

### Key Methods

#### `get_material_stylesheet(theme)`
Generates complete stylesheet for given theme

#### `apply_elevation(widget, level, dark_mode)`
Applies shadow effect to widget based on elevation level

#### `apply_theme(theme)`
Applies theme to entire application

#### `toggle_theme()`
Switches between light and dark themes

## Performance

- **Instant switching**: Theme changes apply immediately
- **No flickering**: Smooth transition between themes
- **Cached stylesheets**: Generated once per theme
- **Lightweight**: Minimal performance impact

## Browser Compatibility

Not applicable (desktop Qt application)

## Future Enhancements

Potential improvements:

1. **Animation**: Smooth color transitions when switching themes
2. **Auto-switching**: Time-based auto-switch to dark mode
3. **System theme**: Follow OS theme preference
4. **Custom themes**: User-defined color schemes
5. **Theme preview**: Preview before applying
6. **Export/Import**: Share custom themes

## References

- [Material Design Guidelines](https://material.io/design)
- [Material Color System](https://material.io/design/color/)
- [Material Elevation](https://material.io/design/environment/elevation.html)
- [Material Typography](https://material.io/design/typography/)

## Version History

- **v0.3.0**: Material Design theme system with light/dark modes
- **v0.2.0**: Basic unified window application
- **v0.1.0**: Original dialog-based application

---

**🎨 Design System Status**: Complete and Production-Ready

**Last Updated**: October 12, 2025

