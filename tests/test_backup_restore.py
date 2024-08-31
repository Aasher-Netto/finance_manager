import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import shutil
import unittest
import glob
from datetime import datetime

from database import get_db_connection
from main import backup_database, restore_database

class TestBackupRestore(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_finance_manager.db'  
        self.backup_dir = 'test_backups'
        self.backup_file = os.path.join(self.backup_dir, 'test_backup.db')

        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.backup_file):
            os.remove(self.backup_file)

        conn = get_db_connection(self.db_path) 
        conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('test_user', 'test_pass'))
        conn.commit()
        conn.close()

    def test_backup_database(self):
       # Find the most recent backup file in the directory
       latest_backup = max(glob.glob('test_backups/*.db'), key=os.path.getctime)
       self.assertTrue(os.path.exists(latest_backup))

    def test_restore_database(self):
        backup_database(self.backup_dir)
        restore_database(self.backup_file, self.db_path)
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', ('test_user',))
        user = cursor.fetchone()
        self.assertIsNotNone(user)
        conn.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.backup_file):
            os.remove(self.backup_file)

if __name__ == '__main__':
    unittest.main()