"""
Main application module for user management system.
This module provides functionality for user registration and authentication.
"""

import hashlib
import sqlite3
from typing import Optional, Tuple


class DatabaseConfig:
    """Database configuration constants."""
    DB_NAME = 'users.db'
    USERS_TABLE = 'users'


class UserManager:
    """Manages user operations including registration and authentication."""

    def __init__(self, db_name: str = DatabaseConfig.DB_NAME):
        """
        Initialize UserManager with database connection.
        
        Args:
            db_name: Name of the SQLite database file
        """
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self) -> None:
        """Create users table if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        email TEXT NOT NULL
                    )
                ''')
                conn.commit()
        except sqlite3.Error as db_error:
            raise DatabaseError(f"Failed to initialize database: {db_error}") from db_error

    def register_user(self, username: str, password: str, email: str) -> bool:
        """
        Register a new user in the system.
        
        Args:
            username: Unique username for the user
            password: Plain text password (will be hashed)
            email: User's email address
            
        Returns:
            True if registration successful, False otherwise
            
        Raises:
            DatabaseError: If database operation fails
            ValueError: If input validation fails
        """
        if not username or not password or not email:
            raise ValueError("Username, password, and email are required")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        password_hash = self._hash_password(password)
        
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f'INSERT INTO {DatabaseConfig.USERS_TABLE} (username, password_hash, email) VALUES (?, ?, ?)',
                    (username, password_hash, email)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as db_error:
            raise DatabaseError(f"Failed to register user: {db_error}") from db_error

    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticate a user by username and password.
        
        Args:
            username: Username to authenticate
            password: Password to verify
            
        Returns:
            True if authentication successful, False otherwise
            
        Raises:
            DatabaseError: If database operation fails
        """
        if not username or not password:
            return False
        
        password_hash = self._hash_password(password)
        
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f'SELECT password_hash FROM {DatabaseConfig.USERS_TABLE} WHERE username = ?',
                    (username,)
                )
                result = cursor.fetchone()
                
                if result is None:
                    return False
                
                stored_hash = result[0]
                return stored_hash == password_hash
        except sqlite3.Error as db_error:
            raise DatabaseError(f"Failed to authenticate user: {db_error}") from db_error

    def get_user_info(self, username: str) -> Optional[Tuple[int, str, str]]:
        """
        Retrieve user information by username.
        
        Args:
            username: Username to look up
            
        Returns:
            Tuple of (id, username, email) if found, None otherwise
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f'SELECT id, username, email FROM {DatabaseConfig.USERS_TABLE} WHERE username = ?',
                    (username,)
                )
                result = cursor.fetchone()
                return result
        except sqlite3.Error as db_error:
            raise DatabaseError(f"Failed to retrieve user info: {db_error}") from db_error

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.
        
        Args:
            password: Plain text password
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(password.encode()).hexdigest()


class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass


def main() -> None:
    """Main function to demonstrate UserManager functionality."""
    user_manager = UserManager()
    
    # Example usage
    try:
        # Register a new user
        if user_manager.register_user("john_doe", "securepass123", "john@example.com"):
            print("User registered successfully!")
        else:
            print("Username already exists!")
        
        # Authenticate user
        if user_manager.authenticate_user("john_doe", "securepass123"):
            print("Authentication successful!")
            
            # Get user info
            user_info = user_manager.get_user_info("john_doe")
            if user_info:
                user_id, username, email = user_info
                print(f"User ID: {user_id}, Username: {username}, Email: {email}")
        else:
            print("Authentication failed!")
            
    except (ValueError, DatabaseError) as error:
        print(f"Error occurred: {error}")


if __name__ == "__main__":
    main()
