import jwt
import datetime
import hashlib
import bcrypt
import sqlite3
import time
from flask import Blueprint, request, render_template, redirect, make_response, g
from collections import defaultdict
from datetime import datetime as dt, timedelta

bp = Blueprint('auth', __name__)
login_attempts = defaultdict(list)
suspicious_attempts = defaultdict(list)

# Replace with a strong, secret key for JWT signing
SECRET_KEY = 'supersecret'  # Use a more secure key in production!

def encode_jwt(data):
    """Create a JWT token."""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'username': data['user'],
        'exp': expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt(token):
    """Decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@bp.before_app_request
def load_fake_session():
    cookie = request.cookies.get('session')
    g.user = None
    if cookie:
        session_data = decode_jwt(cookie)
        if session_data:
            g.user = session_data.get('username')

@bp.route('/', methods=['GET', 'POST'])
def login():
    client_ip = request.remote_addr
    now = dt.now()

    login_attempts[client_ip] = [ts for ts in login_attempts[client_ip] if now - ts < timedelta(minutes=1)]
    suspicious_attempts[client_ip] = [ts for ts in suspicious_attempts[client_ip] if now - ts < timedelta(minutes=1)]

    if len(login_attempts[client_ip]) >= 5:
        return "Too many login attempts. Try again in 1 minute.", 429
    if len(suspicious_attempts[client_ip]) >= 5:
        return "Blocked due to repeated suspicious input. Try again in 1 minute", 403

    if request.method == 'POST':
        action = request.form.get('action')  # "login" or "register"
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if is_banned_payload(username) or is_banned_payload(password):
            suspicious_attempts[client_ip].append(now)
            return render_template("main.html", error="Suspicious input blocked.")

        try:
            conn = sqlite3.connect('utils/users.db')
            cursor = conn.cursor()

            if action == 'register':
                if username == "" or password == "":
                    return render_template("main.html", error="Username and password required.")
                if username == "admin" or username == "root":
                    return render_template("main.html", error="You thought you were sneaky?")
                try:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                    conn.commit()
                    return render_template("main.html", error="Account created. Please log in.")
                except sqlite3.IntegrityError:
                    return render_template("main.html", error="Username already exists.")

            else:
                if username == "admin":
                    # Safe bcrypt logic for admin
                    query = f"SELECT * FROM users WHERE username = '{username}'"
                    print(f"[DEBUG] Executing query: {query}")
                    cursor.execute(query)
                    result = cursor.fetchone()
                    conn.close()

                    if result:
                        stored_password = result[1]
                        if bcrypt.checkpw(password.encode(), stored_password.encode()):
                            token = encode_jwt({"user": 'admin'})
                            resp = make_response(redirect('/'))
                            resp.set_cookie('session', token)
                            return resp
                        else:
                            login_attempts[client_ip].append(now)
                            return render_template("main.html", error="Login failed")
                    else:
                        login_attempts[client_ip].append(now)
                        return render_template("main.html", error="Login failed")

                else:
                    # Hash password with MD5 for non-admin users
                    hashed_input = hashlib.md5(password.encode()).hexdigest()

                    # ⚠️ SQLi-vulnerable query
                    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_input}'"
                    print(f"[DEBUG] Executing query: {query}")
                    cursor.execute(query)
                    result = cursor.fetchone()
                    conn.close()

                    if result:
                        actual_username = result[0]
                        token = encode_jwt({"user": actual_username})
                        resp = make_response(redirect('/'))
                        resp.set_cookie('session', token)
                        return resp
                    else:
                        login_attempts[client_ip].append(now)
                        return render_template("main.html", error="Login failed")

        except Exception as e:
            print("[ERROR]", e)
            return render_template("main.html", error="Database error.")

    return render_template("main.html")

@bp.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('session', '', expires=0)
    return resp

def is_banned_payload(value: str) -> bool:
    value = value.lower()
    banned = [" or ", "union", ";", "select", "update", "insert", "drop", "sleep(", "benchmark("]
    return any(b in value for b in banned)
