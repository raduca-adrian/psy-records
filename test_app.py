#!/usr/bin/env python3
"""
Test script for the Secure Database Application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager

def test_database_functionality():
    """Test basic database functionality"""
    print("Testing Secure Database Application...")
    
    # Initialize database manager
    db = DatabaseManager("test_secure_app.db")
    
    # Test 1: Initialize database
    print("\n1. Testing database initialization...")
    if db.initialize_database("test_password_123"):
        print("✓ Database initialized successfully")
    else:
        print("✗ Database initialization failed")
        return False
    
    # Test 2: Connect to database
    print("\n2. Testing database connection...")
    if db.connect("test_password_123"):
        print("✓ Database connection successful")
    else:
        print("✗ Database connection failed")
        return False
    
    # Test 3: Create user
    print("\n3. Testing user creation...")
    if db.create_user("testuser", "testpass123"):
        print("✓ User created successfully")
    else:
        print("✗ User creation failed")
        return False
    
    # Test 4: Authenticate user
    print("\n4. Testing user authentication...")
    if db.authenticate_user("testuser", "testpass123"):
        print("✓ User authentication successful")
    else:
        print("✗ User authentication failed")
        return False
    
    # Test 5: Add person
    print("\n5. Testing person creation...")
    if db.add_person("John Doe", "1234567890123"):
        print("✓ Person added successfully")
    else:
        print("✗ Person creation failed")
        return False
    
    # Test 6: Get all persons
    print("\n6. Testing person retrieval...")
    persons = db.get_all_persons()
    if persons and len(persons) > 0:
        print(f"✓ Retrieved {len(persons)} person(s)")
        print(f"  Person: {persons[0][1]} (CNP: {persons[0][2]})")
    else:
        print("✗ Person retrieval failed")
        return False
    
    # Test 7: Change password
    print("\n7. Testing password change...")
    if db.change_password("testuser", "testpass123", "newpass456"):
        print("✓ Password changed successfully")
    else:
        print("✗ Password change failed")
        return False
    
    # Test 8: Authenticate with new password
    print("\n8. Testing authentication with new password...")
    if db.authenticate_user("testuser", "newpass456"):
        print("✓ Authentication with new password successful")
    else:
        print("✗ Authentication with new password failed")
        return False
    
    # Test 9: Close and reconnect
    print("\n9. Testing database persistence...")
    db.close()
    
    # Create new instance and reconnect
    db2 = DatabaseManager("test_secure_app.db")
    if db2.connect("test_password_123"):
        print("✓ Database reconnection successful")
        
        # Test if data persists
        persons = db2.get_all_persons()
        if persons and len(persons) > 0:
            print("✓ Data persistence verified")
        else:
            print("✗ Data persistence failed")
            return False
        
        db2.close()
    else:
        print("✗ Database reconnection failed")
        return False
    
    print("\n✓ All tests passed! The database system is working correctly.")
    
    # Cleanup
    try:
        if os.path.exists("test_secure_app.db"):
            os.remove("test_secure_app.db")
        if os.path.exists("test_secure_app.db.enc"):
            os.remove("test_secure_app.db.enc")
        print("✓ Test files cleaned up")
    except Exception as e:
        print(f"Warning: Could not clean up test files: {e}")
    
    return True

if __name__ == "__main__":
    try:
        success = test_database_functionality()
        if success:
            print("\n🎉 All tests completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
