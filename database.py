import sqlite3
import bcrypt
import os
from typing import Optional, List, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class DatabaseManager:
    def __init__(self, db_path: str = "secure_app.db"):
        self.db_path = db_path
        self.encrypted_db_path = db_path + ".enc"
        self.connection = None
        self.db_password = None
        self.fernet = None
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _get_fernet(self, password: str) -> Fernet:
        """Get Fernet encryption object from password"""
        # Use a fixed salt for consistency (in production, store this securely)
        salt = b'secure_app_salt_'  # 16 bytes
        key = self._derive_key(password, salt)
        return Fernet(key)
    
    def connect(self, password: str) -> bool:
        """Connect to the encrypted database with the given password."""
        try:
            self.fernet = self._get_fernet(password)
            
            # If encrypted file exists, decrypt it first
            if os.path.exists(self.encrypted_db_path):
                with open(self.encrypted_db_path, 'rb') as f:
                    encrypted_data = f.read()
                
                try:
                    decrypted_data = self.fernet.decrypt(encrypted_data)
                    with open(self.db_path, 'wb') as f:
                        f.write(decrypted_data)
                except Exception:
                    return False  # Wrong password
            
            # Connect to SQLite database
            self.connection = sqlite3.connect(self.db_path)
            self.db_password = password
            
            # Test the connection
            self.connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
            
            # Create tables if they don't exist
            self._create_tables()
            
            # Encrypt and save the database
            self._encrypt_and_save()
            
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            if self.connection:
                self.connection.close()
                self.connection = None
            return False
    
    def _encrypt_and_save(self):
        """Encrypt the database file"""
        if self.fernet and os.path.exists(self.db_path):
            with open(self.db_path, 'rb') as f:
                data = f.read()
            
            encrypted_data = self.fernet.encrypt(data)
            with open(self.encrypted_db_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Remove unencrypted file
            try:
                os.remove(self.db_path)
            except OSError:
                pass
    
    def _create_tables(self):
        """Create necessary tables if they don't exist."""
        cursor = self.connection.cursor()
        
        # Create users table for authentication
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create persons table for storing name and CNP
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                cnp TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
    
    def create_user(self, username: str, password: str) -> bool:
        """Create a new user with hashed password."""
        if not self.connection:
            return False
        
        try:
            # Hash the password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user with username and password."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT password_hash FROM users WHERE username = ?",
                (username,)
            )
            result = cursor.fetchone()
            
            if result:
                stored_hash = result[0]
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
            return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password after verifying the old one."""
        if not self.connection:
            return False
        
        # First authenticate with old password
        if not self.authenticate_user(username, old_password):
            return False
        
        try:
            # Hash the new password
            new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = ? WHERE username = ?",
                (new_password_hash, username)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
    
    def add_person(self, name: str, cnp: str) -> bool:
        """Add a new person to the database."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO persons (name, cnp) VALUES (?, ?)",
                (name, cnp)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # CNP already exists
        except Exception as e:
            print(f"Error adding person: {e}")
            return False
    
    def get_all_persons(self) -> List[Tuple[int, str, str, str]]:
        """Get all persons from the database."""
        if not self.connection:
            return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, name, cnp, created_at FROM persons ORDER BY name")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving persons: {e}")
            return []
    
    def update_person(self, person_id: int, name: str, cnp: str) -> bool:
        """Update person information."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE persons SET name = ?, cnp = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (name, cnp, person_id)
            )
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False  # CNP already exists
        except Exception as e:
            print(f"Error updating person: {e}")
            return False
    
    def delete_person(self, person_id: int) -> bool:
        """Delete a person from the database."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM persons WHERE id = ?", (person_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting person: {e}")
            return False
    
    def user_exists(self, username: str) -> bool:
        """Check if a user exists in the database."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            return cursor.fetchone() is not None
        except Exception:
            return False
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            # Encrypt and save before closing
            self._encrypt_and_save()
            self.connection.close()
            self.connection = None
    
    def initialize_database(self, password: str) -> bool:
        """Initialize a new encrypted database."""
        try:
            # Create new database file
            if os.path.exists(self.encrypted_db_path):
                return False  # Database already exists
            
            # Create temporary SQLite database
            conn = sqlite3.connect(self.db_path)
            
            # Create a test table to ensure the database is properly created
            conn.execute("CREATE TABLE test_table (id INTEGER)")
            conn.execute("DROP TABLE test_table")
            conn.close()
            
            # Now encrypt it
            self.fernet = self._get_fernet(password)
            self._encrypt_and_save()
            
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False
