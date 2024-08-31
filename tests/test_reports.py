import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from reports import get_monthly_report, get_yearly_report
from transactions import add_transaction
from budgets import set_budget
from datetime import datetime
from database import get_db_connection

class TestReportsModule(unittest.TestCase):

    def setUp(self):
        #setting up database connection in clean state
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

        # Setting up sample data for testing
        self.user_id = 1
        self.category_id = 1
        self.category_name = 'Groceries'
        self.budget_amount = 500.00
        self.date = datetime.now().strftime('%Y-%m-%d')

        # Setting up budget and transactions
        set_budget(self.user_id, self.category_id, 2024, '08', self.budget_amount)
        add_transaction(self.user_id, 100.00, self.category_id, 'expense', self.date)
        add_transaction(self.user_id, 200.00, self.category_id, 'income', self.date)

    def test_get_monthly_report(self):
        report = get_monthly_report(self.user_id, 2024, '08')
        self.assertIn('income', report)
        self.assertIn('expenses', report)
        self.assertEqual(report['income'], 200.00)
        self.assertEqual(report['expenses'], 100.00)

    def test_get_yearly_report(self):
        report = get_yearly_report(self.user_id, 2024)
        self.assertIn('income', report)
        self.assertIn('expenses', report)
        self.assertEqual(report['income'], 200.00)
        self.assertEqual(report['expenses'], 100.00)

    def test_report_formatting(self):
        report = get_monthly_report(self.user_id, 2024, '08')
        # Checking formatting or structure as needed
        self.assertIsInstance(report, dict) # this is an example for JSON Format

    def tearDown(self):
        # Clean up the database
        self.cursor.execute('DELETE FROM transactions')
        self.cursor.execute('DELETE FROM budgets')
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
