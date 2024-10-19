import sqlite3

def connect():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        email TEXT)''')
    
    conn.commit()
    conn.close()

def insert_contact(name, phone, email):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    conn.commit()
    conn.close()

def fetch_contacts():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_contact(contact_id):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()

def update_contact(contact_id, name, phone, email):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE contacts SET name = ?, phone = ?, email = ? 
                      WHERE id = ?''', (name, phone, email, contact_id))
    conn.commit()
    conn.close()
