from flask import Blueprint, request, render_template, session, g
import os
from werkzeug.utils import secure_filename
from .utils.login_required import login_required

bp = Blueprint('upload', __name__, url_prefix='/upload')

UPLOAD_BASE = 'uploads'
os.makedirs(UPLOAD_BASE, exist_ok=True)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # ❌ Block guest users AFTER they try to upload
        if g.user == 'guest':
            return render_template("guest_upload.html"), 403

        uploaded_file = request.files.get('file')
        if not uploaded_file:
            return "No file uploaded", 400

        # ✅ Check file extension
        allowed_exts = {'.jpg', '.png', '.pdf', '.php5'}
        filename = secure_filename(uploaded_file.filename)
        _, ext = os.path.splitext(filename.lower())
        if ext not in allowed_exts:
            return "File type not allowed", 400

        # ✅ Save to user-specific folder
        user_folder = g.user
        user_path = os.path.join(UPLOAD_BASE, user_folder)
        os.makedirs(user_path, exist_ok=True)

        save_path = os.path.join(user_path, filename)
        uploaded_file.save(save_path)

        return "Uploaded successfully. You can check your profile for more info."

    return render_template("upload.html")
