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
        
        # Create assessments table for patient assessments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                assessment_date DATE NOT NULL,
                chief_complaint TEXT,
                medical_history TEXT,
                physical_examination TEXT,
                diagnosis TEXT,
                treatment_plan TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
            )
        """)
        
        # Create consultations table for follow-up consultations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                consultation_date DATE NOT NULL,
                consultation_type TEXT NOT NULL DEFAULT 'Follow-up',
                symptoms TEXT,
                examination_findings TEXT,
                recommendations TEXT,
                medications TEXT,
                next_appointment DATE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
            )
        """)
        
        self.connection.commit()
    
    def create_user(self, username: str, password: str) -> bool:
        """Create a new user with hashed password."""
        if not self.connection:
            return False
        
        try:
            # Hash the password
            password_hash_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # Store as UTF-8 text to be consistent with the TEXT column type
            password_hash = password_hash_bytes.decode('utf-8')
            
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
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode('utf-8')
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
            new_password_hash_bytes = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            new_password_hash = new_password_hash_bytes.decode('utf-8')
            
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
            # Ensure all changes are flushed
            try:
                self.connection.commit()
            except Exception:
                pass
            # Close the connection to release file handles (important on Windows)
            self.connection.close()
            self.connection = None
            # Encrypt and remove plaintext after the database file is released
            self._encrypt_and_save()
    
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
        
    # Assessment Management Methods
    def add_assessment(self, person_id: int, assessment_date: str, chief_complaint: str = "",
                      medical_history: str = "", physical_examination: str = "", 
                      diagnosis: str = "", treatment_plan: str = "", notes: str = "") -> bool:
        """Add a new assessment for a person."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO assessments (person_id, assessment_date, chief_complaint, 
                                       medical_history, physical_examination, diagnosis, 
                                       treatment_plan, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (person_id, assessment_date, chief_complaint, medical_history, 
                  physical_examination, diagnosis, treatment_plan, notes))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding assessment: {e}")
            return False
    
    def get_assessments_for_person(self, person_id: int) -> List[Tuple]:
        """Get all assessments for a specific person."""
        if not self.connection:
            return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT id, assessment_date, chief_complaint, medical_history, 
                       physical_examination, diagnosis, treatment_plan, notes, 
                       created_at, updated_at
                FROM assessments 
                WHERE person_id = ? 
                ORDER BY assessment_date DESC
            """, (person_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting assessments: {e}")
            return []
    
    def update_assessment(self, assessment_id: int, assessment_date: str = None,
                         chief_complaint: str = None, medical_history: str = None,
                         physical_examination: str = None, diagnosis: str = None,
                         treatment_plan: str = None, notes: str = None) -> bool:
        """Update an existing assessment."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            
            # Build dynamic update query
            updates = []
            values = []
            
            if assessment_date is not None:
                updates.append("assessment_date = ?")
                values.append(assessment_date)
            if chief_complaint is not None:
                updates.append("chief_complaint = ?")
                values.append(chief_complaint)
            if medical_history is not None:
                updates.append("medical_history = ?")
                values.append(medical_history)
            if physical_examination is not None:
                updates.append("physical_examination = ?")
                values.append(physical_examination)
            if diagnosis is not None:
                updates.append("diagnosis = ?")
                values.append(diagnosis)
            if treatment_plan is not None:
                updates.append("treatment_plan = ?")
                values.append(treatment_plan)
            if notes is not None:
                updates.append("notes = ?")
                values.append(notes)
            
            if not updates:
                return True  # No updates to make
            
            updates.append("updated_at = CURRENT_TIMESTAMP")
            values.append(assessment_id)
            
            query = f"UPDATE assessments SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating assessment: {e}")
            return False
    
    def delete_assessment(self, assessment_id: int) -> bool:
        """Delete an assessment."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM assessments WHERE id = ?", (assessment_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting assessment: {e}")
            return False
    
    # Consultation Management Methods
    def add_consultation(self, person_id: int, consultation_date: str, 
                        consultation_type: str = "Follow-up", symptoms: str = "",
                        examination_findings: str = "", recommendations: str = "",
                        medications: str = "", next_appointment: str = None, 
                        notes: str = "") -> bool:
        """Add a new consultation for a person."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO consultations (person_id, consultation_date, consultation_type,
                                         symptoms, examination_findings, recommendations,
                                         medications, next_appointment, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (person_id, consultation_date, consultation_type, symptoms,
                  examination_findings, recommendations, medications, next_appointment, notes))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding consultation: {e}")
            return False
    
    def get_consultations_for_person(self, person_id: int) -> List[Tuple]:
        """Get all consultations for a specific person."""
        if not self.connection:
            return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT id, consultation_date, consultation_type, symptoms,
                       examination_findings, recommendations, medications,
                       next_appointment, notes, created_at, updated_at
                FROM consultations 
                WHERE person_id = ? 
                ORDER BY consultation_date DESC
            """, (person_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting consultations: {e}")
            return []
    
    def update_consultation(self, consultation_id: int, consultation_date: str = None,
                           consultation_type: str = None, symptoms: str = None,
                           examination_findings: str = None, recommendations: str = None,
                           medications: str = None, next_appointment: str = None,
                           notes: str = None) -> bool:
        """Update an existing consultation."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            
            # Build dynamic update query
            updates = []
            values = []
            
            if consultation_date is not None:
                updates.append("consultation_date = ?")
                values.append(consultation_date)
            if consultation_type is not None:
                updates.append("consultation_type = ?")
                values.append(consultation_type)
            if symptoms is not None:
                updates.append("symptoms = ?")
                values.append(symptoms)
            if examination_findings is not None:
                updates.append("examination_findings = ?")
                values.append(examination_findings)
            if recommendations is not None:
                updates.append("recommendations = ?")
                values.append(recommendations)
            if medications is not None:
                updates.append("medications = ?")
                values.append(medications)
            if next_appointment is not None:
                updates.append("next_appointment = ?")
                values.append(next_appointment)
            if notes is not None:
                updates.append("notes = ?")
                values.append(notes)
            
            if not updates:
                return True  # No updates to make
            
            updates.append("updated_at = CURRENT_TIMESTAMP")
            values.append(consultation_id)
            
            query = f"UPDATE consultations SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating consultation: {e}")
            return False
    
    def delete_consultation(self, consultation_id: int) -> bool:
        """Delete a consultation."""
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM consultations WHERE id = ?", (consultation_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting consultation: {e}")
            return False
    
    def get_person_complete_record(self, person_id: int) -> dict:
        """Get complete medical record for a person including assessments and consultations."""
        if not self.connection:
            return {}
        
        try:
            cursor = self.connection.cursor()
            
            # Get person details
            cursor.execute("SELECT * FROM persons WHERE id = ?", (person_id,))
            person = cursor.fetchone()
            
            if not person:
                return {}
            
            # Get assessments
            assessments = self.get_assessments_for_person(person_id)
            
            # Get consultations
            consultations = self.get_consultations_for_person(person_id)
            
            return {
                'person': person,
                'assessments': assessments,
                'consultations': consultations
            }
        except Exception as e:
            print(f"Error getting complete record: {e}")
            return {}
