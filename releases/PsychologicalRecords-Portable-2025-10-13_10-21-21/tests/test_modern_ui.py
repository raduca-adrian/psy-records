"""
Simple test script for the modern UI system.
This script verifies that all components can be imported and basic functionality works.
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_imports():
    """Test if all modern UI components can be imported."""
    print("🧪 Testing imports...")
    
    try:
        from src.ui.modern_qss import ModernQSS, ResponsiveStyleManager
        print("✓ modern_qss imports successful")
    except ImportError as e:
        print(f"✗ modern_qss import failed: {e}")
        return False
    
    try:
        from src.ui.responsive_layout import ResponsiveWidget, FlexibleLayout, ResponsiveBreakpoints
        print("✓ responsive_layout imports successful")
    except ImportError as e:
        print(f"✗ responsive_layout import failed: {e}")
        return False
    
    print("✓ All modern UI components imported successfully")
    return True

def test_responsive_breakpoints():
    """Test responsive breakpoint functionality."""
    print("📱 Testing responsive breakpoints...")
    
    try:
        from src.ui.responsive_layout import ResponsiveBreakpoints
        
        # Test breakpoint detection
        test_cases = [
            (400, "xs"),
            (600, "sm"), 
            (800, "md"),
            (1000, "lg"),
            (1400, "xl")
        ]
        
        for width, expected in test_cases:
            result = ResponsiveBreakpoints.get_size_class(width)
            if result == expected:
                print(f"✓ Width {width}px -> {result} (expected {expected})")
            else:
                print(f"✗ Width {width}px -> {result} (expected {expected})")
                return False
        
        print("✓ Responsive breakpoints working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Responsive breakpoints test failed: {e}")
        return False

def test_qss_system():
    """Test QSS stylesheet system."""
    print("🎨 Testing QSS system...")
    
    try:
        from src.ui.modern_qss import ModernQSS
        
        # Test stylesheet generation
        qss_light = ModernQSS.get_complete_stylesheet("light")
        qss_dark = ModernQSS.get_complete_stylesheet("dark")
        
        if len(qss_light) > 1000 and len(qss_dark) > 1000:
            print("✓ QSS stylesheets generated successfully")
            print(f"  Light theme: {len(qss_light)} characters")
            print(f"  Dark theme: {len(qss_dark)} characters")
            return True
        else:
            print("✗ QSS stylesheets too short, may be incomplete")
            return False
            
    except Exception as e:
        print(f"✗ QSS system test failed: {e}")
        return False

def test_modern_ui_creation():
    """Test creating modern UI components without showing them."""
    print("🏗️ Testing modern UI component creation...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from src.ui.responsive_layout import ResponsiveWidget, FlexibleLayout
        
        # Create minimal application if needed
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Test ResponsiveWidget creation
        widget = ResponsiveWidget()
        if widget is not None:
            print("✓ ResponsiveWidget created successfully")
        else:
            print("✗ ResponsiveWidget creation failed")
            return False
        
        # Test FlexibleLayout creation
        layout = FlexibleLayout()
        if layout is not None:
            print("✓ FlexibleLayout created successfully")
        else:
            print("✗ FlexibleLayout creation failed")
            return False
        
        print("✓ Modern UI components created successfully")
        return True
        
    except Exception as e:
        print(f"✗ Modern UI creation test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("🚀 Starting Modern UI System Tests")
    print("=" * 50)
    
    tests = [
        ("Component Imports", test_imports),
        ("Responsive Breakpoints", test_responsive_breakpoints),
        ("QSS System", test_qss_system),
        ("UI Component Creation", test_modern_ui_creation),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            result = test_func()
            results[test_name] = "PASSED" if result else "FAILED"
        except Exception as e:
            results[test_name] = f"ERROR: {e}"
            print(f"✗ {test_name}: ERROR - {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status_icon = "✓" if result == "PASSED" else "✗"
        print(f"{status_icon} {test_name}: {result}")
        if result == "PASSED":
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Modern UI system is ready for use.")
        return True
    else:
        print("⚠️  Some tests failed. Review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
