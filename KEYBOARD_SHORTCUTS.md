# Keyboard Shortcuts - Psychological Records

## Quick Reference Card

### Navigation Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+1** | Go to Patients Tab |
| **Ctrl+2** | Go to Add Patient Tab |
| **Ctrl+3** | Go to Checkup Tab |
| **Ctrl+4** | Go to Session Tab |

### Action Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+N** | New Patient |
| **Ctrl+R** | Refresh List |
| **Ctrl+E** | Export PDF |
| **Ctrl+T** | Toggle Theme (Light/Dark) |
| **F5** | Refresh List (Alt) |

### General Shortcuts

| Shortcut | Action |
|----------|--------|
| **Tab** | Next Field |
| **Shift+Tab** | Previous Field |
| **Enter** | Activate Button |
| **Esc** | Close Dialog |
| **Space** | Activate Checkbox/Button |

## Workflow Examples

### Adding a New Patient
1. Press **Ctrl+2** (or **Ctrl+N**)
2. Type patient name
3. Press **Tab**
4. Type CNP
5. Press **Enter** or click "Add Patient"

### Creating a Checkup
1. Select patient in Patients tab
2. Click "New Checkup" button
3. Fill in the form
4. Press **Enter** to save

### Quick PDF Export
1. Select patient in Patients tab
2. Press **Ctrl+E**
3. Check status bar for file location

## Tips for Efficient Usage

1. **Use Ctrl+1-4** to quickly switch between main sections
2. **Press F5** to refresh after making changes elsewhere
3. **Use Tab** to navigate forms without using the mouse
4. **Memorize Ctrl+N and Ctrl+E** for the most common actions
5. **Press Ctrl+T** to toggle between light and dark themes

## Customization

To add or modify keyboard shortcuts, edit the `_setup_shortcuts()` method in `src/ui/unified_main_window.py`:

```python
def _setup_shortcuts(self) -> None:
    """Set up keyboard shortcuts for quick navigation."""
    QShortcut(QKeySequence("Ctrl+1"), self, lambda: self.tabs.setCurrentIndex(0))
    # Add more shortcuts here...
```

---

**Note:** Print this page and keep it near your workstation for quick reference!

