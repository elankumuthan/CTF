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

@bp.route('/', methods=['GET', 'POST'])
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
        if g.user != "admin" and g.user != requested_user:
            return render_template("error.html", error="Forbidden: You can only view your own profile.")

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

    elif g.user == "ey_user123":
        try:
            files = os.listdir("uploads/ey_user123")
            if files:
                files.sort(key=lambda f: os.path.getmtime(os.path.join("uploads/ey_user123", f)), reverse=True)
                file_hint = f"ey_user123/{files[0]}"
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

    
    #Reset password logic
    if request.method == 'POST':
        if g.user != username:
            return "Forbidden: You can only reset your own password.", 403

        new_password = request.form.get('new_password', '').strip()
        print(new_password)
        if not new_password:
            return render_template("error.html", error="Password cannot be empty.")

        try:
            print("a")
            conn = sqlite3.connect('utils/users.db')
            cursor = conn.cursor()

            # Admin passwords are stored hashed with bcrypt
            if g.user == "admin":
                import bcrypt
                hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            else:
                print("b")
                import hashlib
                hashed = hashlib.md5(new_password.encode()).hexdigest()


            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
            conn.commit()
            conn.close()
            print("c")
            return render_template("profile.html", user={"name": username, "avatar": avatar}, file_hint=file_hint, user_id=user_id, success="Password updated.")
        except Exception as e:
            print(e)
            return render_template("error.html", error="Error resetting password.")

    return render_template("profile.html", user={"name": username, "avatar": avatar}, file_hint=file_hint, user_id=user_id)
