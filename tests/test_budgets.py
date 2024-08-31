import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from database import get_db_connection
from budgets import set_budget, get_remaining_budgets, check_budget_exceeded
from transactions import add_transaction
from datetime import datetime

class TestBudgetModule(unittest.TestCase):
    def setUp(self):
        self.user_id = 1
        self.category_id = 1
        self.year = "2024"
        self.month = "08"
        self.date = f"{self.year}-{self.month}-23"
        self.budget = 500.00

        # Reset the state by clearing the transactions and budgets
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE user_id = ? AND category_id = ?', (self.user_id, self.category_id))
        cursor.execute('DELETE FROM budgets WHERE user_id = ? AND category_id = ? AND year = ? AND month = ?', (self.user_id, self.category_id, self.year, self.month))
        conn.commit()
        conn.close()

        set_budget(self.user_id, self.category_id, self.year, self.month, self.budget)

    def test_set_budget(self):
        result = get_remaining_budgets(self.user_id, self.category_id, self.year, self.month)
        self.assertEqual(result, self.budget)

    def test_budget_tracking(self):
        add_transaction(self.user_id, 100.00, self.category_id, 'expense', self.date)
        result = get_remaining_budgets(self.user_id, self.category_id, self.year, self.month)
        self.assertEqual(result, 400.00)

    def test_budget_exceed_notification(self):
        add_transaction(self.user_id, 600.00, self.category_id, 'expense', self.date)
        exceeded = check_budget_exceeded(self.user_id, self.category_id, self.year, self.month)
        self.assertTrue(exceeded)

if __name__ == '__main__':
    unittest.main()