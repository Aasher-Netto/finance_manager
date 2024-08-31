import sqlite3
from database import get_db_connection

def add_category(name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO categories (name)
    VALUES (?)
    ''', (name,))

    conn.commit()
    conn.close()
    print(f"Category '{name}' added successfully.")

def update_category(category_id, new_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE categories
    SET name = ?
    WHERE id = ?
    ''', (new_name, category_id))

    conn.commit()
    conn.close()
    print(f"Category ID {category_id} updated successfully.")

def delete_category(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM categories WHERE id = ?
    ''', (category_id,))

    conn.commit()
    conn.close()
    print(f"Category ID {category_id} deleted successfully.")

def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()

    conn.close()
    return categories