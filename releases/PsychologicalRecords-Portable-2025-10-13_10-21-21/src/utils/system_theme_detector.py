"""
System theme detection for Windows, macOS, and Linux.
Detects whether the OS is using light or dark mode.
"""

import sys
import platform
from typing import Literal


def detect_system_theme() -> Literal["light", "dark"]:
    """
    Detect the current system theme (light or dark).
    
    Returns:
        "light" or "dark" based on system preference
        Falls back to "light" if detection fails
    """
    system = platform.system()
    
    if system == "Windows":
        return _detect_windows_theme()
    elif system == "Darwin":  # macOS
        return _detect_macos_theme()
    elif system == "Linux":
        return _detect_linux_theme()
    else:
        return "light"  # Default fallback


def _detect_windows_theme() -> Literal["light", "dark"]:
    """Detect Windows theme from registry."""
    try:
        import winreg
        
        # Try to read the AppsUseLightTheme registry value
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            
            # Value of 0 means dark mode, 1 means light mode
            return "light" if value == 1 else "dark"
        except FileNotFoundError:
            # If the key doesn't exist, default to light
            return "light"
            
    except ImportError:
        # winreg not available (not on Windows)
        return "light"
    except Exception as e:
        print(f"Error detecting Windows theme: {e}")
        return "light"


def _detect_macos_theme() -> Literal["light", "dark"]:
    """Detect macOS theme using defaults command."""
    try:
        import subprocess
        
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True,
            text=True,
            timeout=1
        )
        
        # If the command succeeds and returns "Dark", use dark mode
        if result.returncode == 0 and "Dark" in result.stdout:
            return "dark"
        else:
            return "light"
            
    except Exception as e:
        print(f"Error detecting macOS theme: {e}")
        return "light"


def _detect_linux_theme() -> Literal["light", "dark"]:
    """
    Detect Linux theme using various methods.
    Tries GTK settings, KDE settings, and environment variables.
    """
    try:
        # Try GTK settings first
        import subprocess
        
        # Try gsettings (GNOME/GTK)
        try:
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
                capture_output=True,
                text=True,
                timeout=1
            )
            
            if result.returncode == 0:
                theme_name = result.stdout.strip().strip("'").lower()
                if "dark" in theme_name:
                    return "dark"
        except:
            pass
        
        # Try reading GTK config file
        import os
        gtk_config_path = os.path.expanduser("~/.config/gtk-3.0/settings.ini")
        if os.path.exists(gtk_config_path):
            try:
                with open(gtk_config_path, 'r') as f:
                    content = f.read().lower()
                    if "dark" in content or "gtk-application-prefer-dark-theme=1" in content:
                        return "dark"
            except:
                pass
        
        # Try KDE settings
        try:
            result = subprocess.run(
                ["kreadconfig5", "--group", "General", "--key", "ColorScheme"],
                capture_output=True,
                text=True,
                timeout=1
            )
            
            if result.returncode == 0 and "dark" in result.stdout.lower():
                return "dark"
        except:
            pass
        
        # Check environment variable
        import os
        theme_env = os.environ.get("GTK_THEME", "").lower()
        if "dark" in theme_env:
            return "dark"
        
    except Exception as e:
        print(f"Error detecting Linux theme: {e}")
    
    return "light"


def should_use_dark_theme() -> bool:
    """
    Convenience function that returns True if dark theme should be used.
    
    Returns:
        True if system is using dark theme, False otherwise
    """
    return detect_system_theme() == "dark"


# For testing
if __name__ == "__main__":
    theme = detect_system_theme()
    print(f"Detected system theme: {theme}")
    print(f"Platform: {platform.system()}")

