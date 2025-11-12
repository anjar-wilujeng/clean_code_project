"""
Unit tests for the user management system.
"""

import unittest
import os
import tempfile
from app import UserManager, DatabaseError, DatabaseConfig


class TestUserManager(unittest.TestCase):
    """Test cases for UserManager class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary database for testing
        self.test_db_fd, self.test_db_path = tempfile.mkstemp()
        self.user_manager = UserManager(self.test_db_path)

    def tearDown(self):
        """Clean up after each test method."""
        os.close(self.test_db_fd)
        os.unlink(self.test_db_path)

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


if __name__ == '__main__':
    unittest.main()
