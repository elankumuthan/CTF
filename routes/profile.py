from flask import Blueprint, request, render_template, g, url_for, redirect
import sqlite3, os, imghdr
from werkzeug.utils import secure_filename
from .utils.login_required import login_required

bp = Blueprint('profile', __name__, url_prefix='/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
PROFILE_PHOTO_DIR = 'profile_photo'

def get_all_users():
    try:
        conn = sqlite3.connect('utils/users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users ORDER BY rowid ASC")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users
    except:
        return []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_image_file(file):
    header = file.read(512)
    file.seek(0)
    file_type = imghdr.what(None, header)
    return file_type in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
@login_required
def view_profile():
    users = get_all_users()
    user_id = request.args.get('id')

    # Determine which user's profile to show
    if user_id:
        try:
            user_id = int(user_id)
        except ValueError:
            return "Invalid user ID", 400
        if user_id < 0 or user_id >= len(users):
            return "Invalid user ID", 404
        requested_user = users[user_id]
        if g.user != "3y_adm!n!strat0r" and g.user != requested_user:
            return render_template("error.html", error="Forbidden: You can only view your own profile.")
        username = requested_user
    else:
        username = g.user
        if not username:
            return render_template("main.html", error="Please log in first")
        user_id = users.index(username)

    # Handle POST actions
    success = None
    if request.method == 'POST':
        # Avatar upload
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and allowed_file(file.filename) and is_image_file(file):
                filename = secure_filename(file.filename)
                user_dir = os.path.join(PROFILE_PHOTO_DIR, username)
                os.makedirs(user_dir, exist_ok=True)
                file.save(os.path.join(user_dir, filename))
                return redirect(url_for('profile.view_profile'))
            else:
                return render_template("error.html", error="Invalid image file.")

        # Password reset
        if 'new_password' in request.form:
            if g.user != username:
                return "Forbidden: You can only reset your own password.", 403
            new_password = request.form.get('new_password', '').strip()
            if not new_password:
                return render_template("error.html", error="Password cannot be empty.")
            try:
                conn = sqlite3.connect('utils/users.db')
                cursor = conn.cursor()
                if g.user == "3y_adm!n!strat0r":
                    import bcrypt
                    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                else:
                    import hashlib
                    hashed = hashlib.md5(new_password.encode()).hexdigest()
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
                conn.commit()
                conn.close()
                success = "Password updated."
            except Exception as e:
                print(e)
                return render_template("error.html", error="Error resetting password.")

    # Get latest avatar
    avatar = "uploads/default.png"
    user_folder = os.path.join(PROFILE_PHOTO_DIR, username)
    try:
        files = os.listdir(user_folder)
        if files:
            files.sort(key=lambda f: os.path.getmtime(os.path.join(user_folder, f)), reverse=True)
            avatar = os.path.join(user_folder, files[0])
    except:
        pass

    return render_template("profile.html", user={"name": username, "avatar": avatar}, user_id=user_id, success=success)
