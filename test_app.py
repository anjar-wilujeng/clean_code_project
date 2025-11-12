"""
Unit tests for the user management system.
"""

import unittest
import os
import tempfile
import sqlite3
from unittest.mock import patch, MagicMock
from app import UserManager, DatabaseError, DatabaseConfig


class TestUserManager(unittest.TestCase):
    """Test cases for UserManager class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary database for testing
        self.test_db_fd, self.test_db_path = tempfile.mkstemp()
        os.close(self.test_db_fd)  # Close immediately to avoid Windows lock issues
        self.user_manager = UserManager(self.test_db_path)

    def tearDown(self):
        """Clean up after each test method."""
        # Ensure all connections are closed before deletion
        try:
            if os.path.exists(self.test_db_path):
                os.unlink(self.test_db_path)
        except PermissionError:
            pass  # File may still be in use on Windows

    def test_register_user_success(self):
        """Test successful user registration."""
        result = self.user_manager.register_user("testuser", "password123", "test@example.com")
        self.assertTrue(result)

    def test_register_duplicate_user(self):
        """Test that duplicate username registration fails."""
        self.user_manager.register_user("testuser", "password123", "test@example.com")
        result = self.user_manager.register_user("testuser", "different_pass", "other@example.com")
        self.assertFalse(result)

    def test_register_user_empty_username(self):
        """Test that empty username raises ValueError."""
        with self.assertRaises(ValueError):
            self.user_manager.register_user("", "password123", "test@example.com")

    def test_register_user_empty_password(self):
        """Test that empty password raises ValueError."""
        with self.assertRaises(ValueError):
            self.user_manager.register_user("testuser", "", "test@example.com")

    def test_register_user_short_password(self):
        """Test that password shorter than 8 characters raises ValueError."""
        with self.assertRaises(ValueError):
            self.user_manager.register_user("testuser", "short", "test@example.com")

    def test_authenticate_user_success(self):
        """Test successful user authentication."""
        self.user_manager.register_user("testuser", "password123", "test@example.com")
        result = self.user_manager.authenticate_user("testuser", "password123")
        self.assertTrue(result)

    def test_authenticate_user_wrong_password(self):
        """Test that wrong password fails authentication."""
        self.user_manager.register_user("testuser", "password123", "test@example.com")
        result = self.user_manager.authenticate_user("testuser", "wrongpassword")
        self.assertFalse(result)

    def test_authenticate_nonexistent_user(self):
        """Test that nonexistent user fails authentication."""
        result = self.user_manager.authenticate_user("nonexistent", "password123")
        self.assertFalse(result)

    def test_authenticate_empty_username(self):
        """Test that empty username fails authentication."""
        result = self.user_manager.authenticate_user("", "password123")
        self.assertFalse(result)

    def test_get_user_info_success(self):
        """Test successful retrieval of user information."""
        self.user_manager.register_user("testuser", "password123", "test@example.com")
        user_info = self.user_manager.get_user_info("testuser")
        
        self.assertIsNotNone(user_info)
        self.assertEqual(user_info[1], "testuser")
        self.assertEqual(user_info[2], "test@example.com")

    def test_get_user_info_nonexistent(self):
        """Test that nonexistent user returns None."""
        user_info = self.user_manager.get_user_info("nonexistent")
        self.assertIsNone(user_info)

    def test_hash_password_consistency(self):
        """Test that password hashing is consistent."""
        hash1 = UserManager._hash_password("testpassword")
        hash2 = UserManager._hash_password("testpassword")
        self.assertEqual(hash1, hash2)

    def test_hash_password_different_inputs(self):
        """Test that different passwords produce different hashes."""
        hash1 = UserManager._hash_password("password1")
        hash2 = UserManager._hash_password("password2")
        self.assertNotEqual(hash1, hash2)

    def test_register_user_empty_email(self):
        """Test that empty email raises ValueError."""
        with self.assertRaises(ValueError):
            self.user_manager.register_user("testuser", "password123", "")

    def test_authenticate_empty_password(self):
        """Test that empty password fails authentication."""
        result = self.user_manager.authenticate_user("testuser", "")
        self.assertFalse(result)

    @patch('sqlite3.connect')
    def test_initialize_database_error(self, mock_connect):
        """Test database initialization error handling."""
        mock_connect.side_effect = sqlite3.Error("Database connection failed")
        with self.assertRaises(DatabaseError):
            UserManager(self.test_db_path)

    @patch('sqlite3.connect')
    def test_register_user_database_error(self, mock_connect):
        """Test database error during user registration."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = sqlite3.Error("Database error")
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_connect.return_value = mock_conn

        user_manager = UserManager.__new__(UserManager)
        user_manager.db_name = self.test_db_path

        with self.assertRaises(DatabaseError):
            user_manager.register_user("testuser", "password123", "test@example.com")

    @patch('sqlite3.connect')
    def test_authenticate_user_database_error(self, mock_connect):
        """Test database error during user authentication."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = sqlite3.Error("Database error")
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_connect.return_value = mock_conn

        user_manager = UserManager.__new__(UserManager)
        user_manager.db_name = self.test_db_path

        with self.assertRaises(DatabaseError):
            user_manager.authenticate_user("testuser", "password123")

    @patch('sqlite3.connect')
    def test_get_user_info_database_error(self, mock_connect):
        """Test database error during get_user_info."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = sqlite3.Error("Database error")
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_connect.return_value = mock_conn

        user_manager = UserManager.__new__(UserManager)
        user_manager.db_name = self.test_db_path

        with self.assertRaises(DatabaseError):
            user_manager.get_user_info("testuser")


class TestDatabaseConfig(unittest.TestCase):
    """Test cases for DatabaseConfig class."""

    def test_database_config_constants(self):
        """Test that DatabaseConfig has the correct constants."""
        self.assertEqual(DatabaseConfig.DB_NAME, 'users.db')
        self.assertEqual(DatabaseConfig.USERS_TABLE, 'users')


class TestDatabaseError(unittest.TestCase):
    """Test cases for DatabaseError exception."""

    def test_database_error_creation(self):
        """Test that DatabaseError can be created and raised."""
        error = DatabaseError("Test error message")
        self.assertEqual(str(error), "Test error message")


if __name__ == '__main__':
    unittest.main()
