"""
Theme management system for the PyQt6 application.
Handles dark/light mode switching and persistence.
"""

import os
import json
from typing import Optional, Callable, List
from ..ui.styles import ThemeMode, colors

class ThemeManager:
    """Manages theme settings across the entire application"""
    
    SETTINGS_FILE = 'settings.json'
    DEFAULT_THEME = ThemeMode.LIGHT
    
    def __init__(self):
        self._theme_change_callbacks: List[Callable] = []
        self._current_theme = self.DEFAULT_THEME
        
        # Load theme preference
        self.load_theme_preference()
    
    def load_theme_preference(self) -> ThemeMode:
        """Load saved theme preference from settings file."""
        try:
            if os.path.exists(self.SETTINGS_FILE):
                with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    saved_theme = settings.get('theme', self.DEFAULT_THEME.value)
                    
                    # Convert string to ThemeMode enum
                    if saved_theme == ThemeMode.DARK.value:
                        self._current_theme = ThemeMode.DARK
                    else:
                        self._current_theme = ThemeMode.LIGHT
                    
                    # Update the global color system
                    colors.set_theme(self._current_theme)
                    return self._current_theme
        except Exception as e:
            print(f"Failed to load theme preference: {e}")
        
        # Fallback to default
        self._current_theme = self.DEFAULT_THEME
        colors.set_theme(self.DEFAULT_THEME)
        return self.DEFAULT_THEME
    
    def save_theme_preference(self, theme: ThemeMode) -> bool:
        """Save theme preference to settings file."""
        try:
            settings = {}
            if os.path.exists(self.SETTINGS_FILE):
                with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            
            settings['theme'] = theme.value
            with open(self.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Failed to save theme preference: {e}")
            return False
    
    def change_theme(self, theme: ThemeMode) -> bool:
        """Change the application theme and notify all registered components."""
        try:
            # Update the global color system
            colors.set_theme(theme)
            self._current_theme = theme
            
            # Save to settings
            self.save_theme_preference(theme)
            
            # Notify all registered callbacks
            for callback in self._theme_change_callbacks:
                try:
                    callback(theme)
                except Exception as e:
                    print(f"Error in theme change callback: {e}")
            
            return True
        except Exception as e:
            print(f"Failed to change theme: {e}")
            return False
    
    def toggle_theme(self) -> ThemeMode:
        """Toggle between light and dark themes."""
        new_theme = ThemeMode.DARK if self._current_theme == ThemeMode.LIGHT else ThemeMode.LIGHT
        self.change_theme(new_theme)
        return new_theme
    
    def get_current_theme(self) -> ThemeMode:
        """Get the current theme."""
        return self._current_theme
    
    def is_dark_mode(self) -> bool:
        """Check if current theme is dark mode."""
        return self._current_theme == ThemeMode.DARK
    
    def register_theme_change_callback(self, callback: Callable[[ThemeMode], None]):
        """Register a callback to be called when theme changes."""
        if callback not in self._theme_change_callbacks:
            self._theme_change_callbacks.append(callback)
    
    def unregister_theme_change_callback(self, callback: Callable[[ThemeMode], None]):
        """Unregister a theme change callback."""
        if callback in self._theme_change_callbacks:
            self._theme_change_callbacks.remove(callback)

# Global theme manager instance
_theme_manager = None

def get_theme_manager() -> ThemeManager:
    """Get the global theme manager instance."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager

def get_current_theme() -> ThemeMode:
    """Get the current theme."""
    return get_theme_manager().get_current_theme()

def is_dark_mode() -> bool:
    """Check if current theme is dark mode."""
    return get_theme_manager().is_dark_mode()

def toggle_theme() -> ThemeMode:
    """Toggle between light and dark themes."""
    return get_theme_manager().toggle_theme()

def set_theme(theme: ThemeMode) -> bool:
    """Set the current theme."""
    return get_theme_manager().change_theme(theme)
