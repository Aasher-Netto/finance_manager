import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from auth import register_user, login_user

class TestAuthModule(unittest.TestCase):

    def test_register_user(self):
        # Test case for registering a new user
        result = register_user("test_user", "password123")
        if result == "Error: Username already exists.":
           self.assertEqual(result, "Error: Username already exists.")
        else:
           self.assertIsNone(result)  # If successful, no return value

    def test_login_user(self):
        # Assuming the user was registered in the above test
        result = login_user("test_user", "password123")
        self.assertTrue(result)

        # Test with incorrect password
        result = login_user("test_user", "wrongpassword")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()

if __name__ == '__main__':
    unittest.main()