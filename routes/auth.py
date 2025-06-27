import datetime
import hashlib
import bcrypt
import sqlite3
from flask import Blueprint, request, render_template, redirect, make_response, g
from collections import defaultdict
from datetime import datetime as dt, timedelta
from utils.jwt_handler import encode_jwt, decode_jwt

bp = Blueprint('auth', __name__)
login_attempts = defaultdict(list)
suspicious_attempts = defaultdict(list)

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

    # Clean up old entries
    login_attempts[client_ip] = [ts for ts in login_attempts[client_ip] if now - ts < timedelta(minutes=1)]
    suspicious_attempts[client_ip] = [ts for ts in suspicious_attempts[client_ip] if now - ts < timedelta(minutes=1)]

    # Rate limiting
    if len(login_attempts[client_ip]) >= 5:
        return "Too many login attempts. Try again in 1 minute.", 429
    if len(suspicious_attempts[client_ip]) >= 5:
        return "Blocked due to repeated suspicious input. Try again in 1 minute", 403

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if is_banned_payload(username) or is_banned_payload(password):
            suspicious_attempts[client_ip].append(now)
            return render_template("main.html", error="Suspicious input blocked.")

        try:
            conn = sqlite3.connect('utils/users.db')
            cursor = conn.cursor()

            if username == "3y_adm!n!strat0r":
                # Secure login for admin
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    stored_password = result[1]
                    if bcrypt.checkpw(password.encode(), stored_password.encode()):
                        token = encode_jwt({"username": "3y_adm!n!strat0r"})
                        resp = make_response(redirect('/'))
                        resp.set_cookie('session', token, httponly=True, samesite='Lax', secure=False)
                        return resp

            else:
                # Insecure MD5 + SQLi-vulnerable query
                hashed_input = hashlib.md5(password.encode()).hexdigest()
                query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_input}'"
                print(f"[DEBUG] Executing query: {query}")
                cursor.execute(query)
                result = cursor.fetchone()
                conn.close()

                if result:
                    token = encode_jwt({"username": result[0]})
                    resp = make_response(redirect('/profile'))
                    resp.set_cookie('session', token, httponly=True, samesite='Lax', secure=False)
                    return resp

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
