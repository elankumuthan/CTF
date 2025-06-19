from flask import Blueprint, request, render_template, session, g
import os, uuid
from .utils.login_required import login_required

bp = Blueprint('upload', __name__, url_prefix='/upload')

UPLOAD_BASE = 'uploads'
os.makedirs(UPLOAD_BASE, exist_ok=True)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def upload_wallpaper():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')

        if not uploaded_file:
            return "No file uploaded", 400

        attacker_filename = uploaded_file.filename
        user_folder = g.user
        user_path = os.path.join(UPLOAD_BASE, user_folder)
        os.makedirs(user_path, exist_ok=True)

        save_path = os.path.join(user_path, attacker_filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        uploaded_file.save(save_path)

        # ✅ Also save it as avatar.png to show in profile
        avatar_path = os.path.join(user_path, "avatar.png")
        uploaded_file.seek(0)  # rewind file pointer before saving again
        uploaded_file.save(avatar_path)

        return "Uploaded successfully. You can check your profile for more info."

    return render_template("upload.html")
