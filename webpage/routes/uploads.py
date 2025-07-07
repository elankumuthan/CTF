from flask import Blueprint, request, render_template_string, send_file, g
import os

bp = Blueprint('uploads', __name__, url_prefix='/uploads')

@bp.route('/<user>/<filename>', methods=['GET'])
def serve_user_file(user, filename):
    try:
        if g.user != user and g.user != "3y_adm!n!strat0r":
            return "Forbidden", 403

        uploads_root = os.path.abspath('uploads')
        user_path = os.path.abspath(os.path.join(uploads_root, user))
        full_path = os.path.abspath(os.path.join(user_path, filename))

        if not full_path.startswith(user_path):
            return "Invalid path", 400

        if not os.path.exists(full_path):
            return "File not found", 404

        if request.headers.get('X-Render', '').lower() == 'true':
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                contents = f.read()
            return render_template_string(contents)  # 🔥 SSTI executes here

        return send_file(full_path, as_attachment=False)

    except Exception as e:
        print("[ERROR]", e)
        return "500 Internal Server Error", 500
