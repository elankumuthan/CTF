from flask import Blueprint, request, render_template, abort, g, url_for, redirect
import sqlite3, os
from .utils.login_required import login_required

bp = Blueprint('profile', __name__, url_prefix='/profile')

def get_all_users():
    try:
        conn = sqlite3.connect('utils/users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users ORDER BY rowid ASC")  # Ensures fixed order
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users
    except:
        return []

@bp.route('/')
@login_required
def view_profile():
    users = get_all_users()
    user_id = request.args.get('id')

    # Determine which user to view
    if user_id:
        try:
            user_id = int(user_id)
        except ValueError:
            return "Invalid user ID", 400

        if user_id < 0 or user_id >= len(users):
            return "Invalid user ID", 404

        requested_user = users[user_id]

        # Only admin can view others' profiles
        if g.user == "guest" and g.user != requested_user:
            return "Forbidden: You can only view your own profile.", 403

        username = requested_user
    else:
        # Default to current user's profile
        username = g.user
        if not username:
            return render_template("main.html", error="Please log in first")
        user_id = users.index(username)

    # Avatar logic
    avatar = "uploads/default.png"
    user_folder = f"uploads/{username}"
    try:
        files = os.listdir(user_folder)
        if files:
            files.sort(key=lambda f: os.path.getmtime(os.path.join(user_folder, f)), reverse=True)
            avatar = os.path.join(user_folder, files[0])
    except:
        pass


    # File hint logic
    file_hint = None
    if g.user == "admin":
        try:
            files = os.listdir("uploads/admin")
            if files:
                files.sort(key=lambda f: os.path.getmtime(os.path.join("uploads/admin", f)), reverse=True)
                avatar = f"uploads/admin/{files[0]}"  # ✅ relative path
                file_hint = f"admin/{files[0]}"
        except:
            file_hint = None

    elif g.user == "EY_user123":
        try:
            files = os.listdir("uploads/EY_user123")
            if files:
                files.sort(key=lambda f: os.path.getmtime(os.path.join("uploads/EY_user123", f)), reverse=True)
                file_hint = f"EY_user123/{files[0]}"
        except:
            file_hint = None

    elif g.user == "guest":
        try:
            files = os.listdir("uploads/guest")
            if files:
                files.sort(key=lambda f: os.path.getmtime(os.path.join("uploads/guest", f)), reverse=True)
                file_hint = f"guest/{files[0]}"
        except:
            file_hint = None

    return render_template("profile.html", user={"name": username, "avatar": avatar}, file_hint=file_hint, user_id=user_id)
