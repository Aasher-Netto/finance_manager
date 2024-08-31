import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from categories import add_category, update_category, delete_category, get_all_categories

class TestCategoriesModule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup a fresh database or clean the categories table
        pass

    def setUp(self):
        # Use a fresh category name for each test
        self.category_name = "Groceries"
        self.new_category_name = "Supermarket"
        
        # Clean up the category if it exists to avoid UNIQUE constraint failures
        existing_categories = get_all_categories()
        existing_category = next((cat for cat in existing_categories if cat[1] == self.category_name), None)
        if existing_category:
            delete_category(existing_category[0])
        
        # Add the category to work with
        add_category(self.category_name)

        # Retrieve the newly added category to get its ID
        self.categories = get_all_categories()
        self.category_id = next((cat[0] for cat in self.categories if cat[1] == self.category_name), None)

    def test_add_category(self):
        # Retrieve all categories and check if the new category was added
        categories = get_all_categories()
        added_category = next((cat for cat in categories if cat[0] == self.category_id), None)
        self.assertIsNotNone(added_category)
        self.assertEqual(added_category[1], self.category_name)  # Assuming name is the second column

    def test_update_category(self):
        # Update the category and verify the change
        update_category(self.category_id, self.new_category_name)
        categories = get_all_categories()
        updated_category = next((cat for cat in categories if cat[0] == self.category_id), None)
        self.assertIsNotNone(updated_category)
        self.assertEqual(updated_category[1], self.new_category_name)  # Assuming name is the second column

    def test_delete_category(self):
        # Delete the category and verify it's removed
        delete_category(self.category_id)
        categories = get_all_categories()
        deleted_category = next((cat for cat in categories if cat[0] == self.category_id), None)
        self.assertIsNone(deleted_category)

    @classmethod
    def tearDownClass(cls):
        # Clean up the database after tests
        pass

if __name__ == '__main__':
    unittest.main()
