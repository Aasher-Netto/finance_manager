import sys
import os

# Ensure the parent directory is in the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from transactions import add_transaction, update_transaction, delete_transaction, get_transactions_by_category
from budgets import set_budget
from database import get_db_connection
from datetime import datetime



class TestTransactionsModule(unittest.TestCase):
    def setUp(self):
        # Setting up the database connection in clean state
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

        # Setting up the sample data for testing
        self.user_id = 1
        self.category_id = 1
        self.category_name = 'Groceries'
        self.budget_amount = 500.00
        self.date = datetime.now().strftime('%Y-%m-%d')

        # Setting a budget for the category
        set_budget(self.user_id, self.category_id, 2024, '08', self.budget_amount)
    

    def test_add_transaction(self):
        # Testing by adding an expense transaction
        add_transaction(self.user_id, 100.00, self.category_id, 'expense', self.date)

        # Checking if the transaction is in the database
        self.cursor.execute('''
        SELECT * FROM transactions WHERE user_id = ? AND category_id = ? AND amount = ? AND type = ?
        ''', (self.user_id, self.category_id, 100.00, 'expense'))

        transaction = self.cursor.fetchone()
        self.assertIsNotNone(transaction)
    
        # Assuming transaction[3] should hold 'expense' as a string
        if isinstance(transaction[3], int):  # If type is stored as an int
           type_map = {1: 'expense', 2: 'income'}
           self.assertEqual(type_map[transaction[3]], 'expense')
        else:  # If type is stored as a string
           self.assertEqual(transaction[3], 'expense')


    def test_update_transaction(self):
        # Adding a transaction to update
        add_transaction(self.user_id, 100.00, self.category_id, 'expense', self.date)

        # Get the transaction ID
        self.cursor.execute('''
        SELECT id FROM transactions WHERE user_id = ? AND category_id = ? AND amount = ? AND type = ?
        ''', (self.user_id, self.category_id, 100.00, 'expense'))
        transaction_id = self.cursor.fetchone()[0]

        # Updating the transaction
        update_transaction(transaction_id, 150.00, self.category_id, 'expense', self.date)

        # Checking if the transaction is updated
        self.cursor.execute('''
        SELECT amount FROM transactions WHERE id = ?
        ''', (transaction_id,))
        updated_transaction = self.cursor.fetchone()
        self.assertEqual(updated_transaction[0], 150.00)

    def test_delete_transaction(self):
        # Adding a transaction to delete
        add_transaction(self.user_id, 100.00, self.category_id, 'expense', self.date)

        # Get the transaction ID
        self.cursor.execute('''
        SELECT id FROM transactions WHERE user_id = ? AND category_id = ? AND amount = ? AND type = ?
        ''', (self.user_id, self.category_id, 100.00, 'expense'))
        transaction_id = self.cursor.fetchone()[0]

        # Deleting the transaction
        delete_transaction(transaction_id)

        # Checking if the transaction is deleted
        self.cursor.execute('''
        SELECT * FROM transactions WHERE id = ?
        ''', (transaction_id,))
        deleted_transaction = self.cursor.fetchone()
        self.assertIsNone(deleted_transaction)

    def test_get_transactions_by_category(self):
        # Add multiple transactions for the category
        add_transaction(self.user_id, 100.00, self.category_id, 'expense', self.date)
        add_transaction(self.user_id, 200.00, self.category_id, 'income', self.date)

        # Retrieve transactions by category
        transactions = get_transactions_by_category(self.user_id, self.category_id)

        # Check the transactions are retrieved correctly
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0][2], 100.00)
        self.assertEqual(transactions[1][2], 200.00)

    def tearDown(self):
        # Clean up the database
        self.cursor.execute('DELETE FROM transactions')
        self.cursor.execute('DELETE FROM budgets')
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
