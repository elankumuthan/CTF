import sqlite3
import hashlib
import bcrypt
import os
from datetime import datetime

def hash_md5(plain_pw):
    return hashlib.md5(plain_pw.encode()).hexdigest()

def hash_bcrypt(plain_pw):
    return bcrypt.hashpw(plain_pw.encode(), bcrypt.gensalt()).decode()

def initialize_users_db():
    try:
        conn = sqlite3.connect('/app/utils/users.db')
        c = conn.cursor()

        c.execute('DROP TABLE IF EXISTS users')
        c.execute('CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)')

        users = [
            ('3y_adm!n!strat0r', 'sup3rs3cur3p@ssw0rd'),
            ('3y_us3r!23', 'EYpass!!!@@@'),
            ('guest', 'Gu3stp@ss!'),
            ('user5', 'Trym3!23')
        ]

        for username, raw_password in users:
            if username == '3y_adm!n!strat0r':
                hashed = hash_bcrypt(raw_password)
            else:
                hashed = hash_md5(raw_password)
            c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))

        conn.commit()
        print("[✔] users.db initialized with mixed hash passwords")
    except Exception as e:
        print(f"[!] Error initializing users.db: {e}")
    finally:
        conn.close()

def initialize_comments_db():
    try:
        conn = sqlite3.connect('/app/utils/comments.db')
        c = conn.cursor()

        c.execute('DROP TABLE IF EXISTS comments')
        c.execute('''
            CREATE TABLE comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                author TEXT,
                timestamp TEXT,
                message TEXT
            )
        ''')

        conn.commit()
        print("[✔] comments.db initialized with table and test comment")
    except Exception as e:
        print(f"[!] Error initializing comments.db: {e}")
    finally:
        conn.close()

def initialize_database_to_leak_db():
    try:
        conn = sqlite3.connect('/app/utils/database_to_leak.db')
        c = conn.cursor()

        c.execute('DROP TABLE IF EXISTS users')
        c.execute('CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)')

        users = [
            ('3y_us3r!23', 'EYpass!!!@@@'),
            ('guest', 'Gu3stp@ss!')
        ]

        for username, raw_password in users:
            if username == '3y_adm!n!strat0r':
                hashed = hash_bcrypt(raw_password)
            else:
                hashed = hash_md5(raw_password)
            c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))

        conn.commit()
        print("[✔] database_to_leak.db initialized with mixed hash passwords")
    except Exception as e:
        print(f"[!] Error initializing database_to_leak.db: {e}")
    finally:
        conn.close()
# Run both initializations
initialize_users_db()
initialize_comments_db()
initialize_database_to_leak_db()
