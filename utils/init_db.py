import sqlite3
import hashlib
import bcrypt
import os

def hash_md5(plain_pw):
    return hashlib.md5(plain_pw.encode()).hexdigest()

def hash_bcrypt(plain_pw):
    return bcrypt.hashpw(plain_pw.encode(), bcrypt.gensalt()).decode()

def initialize_db():
    conn = None
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute('DROP TABLE IF EXISTS users')
        c.execute('CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)')

        users = [
            ('admin', 'sup3rs3cur3p@ssw0rd'),
            ('EY_user123', 'EYpass!!!@@@'),
            ('guest', 'Gu3stp@ss!')
        ]

        for username, raw_password in users:
            if username == 'admin':
                hashed = hash_bcrypt(raw_password)  # bcrypt for admin
            else:
                hashed = hash_md5(raw_password)      # md5 for normal user
            c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))

        conn.commit()
        print("Database initialized with mixed hashing (bcrypt + md5).")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

initialize_db()
