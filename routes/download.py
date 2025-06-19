from flask import Blueprint, send_file, g, abort
import os

bp = Blueprint('download', __name__, url_prefix='/download')

@bp.route('/<path:filepath>', methods=['GET'])
def download(filepath):
    try:
        full_path = os.path.abspath(os.path.join('uploads', filepath))
        print("[DEBUG] Download request for:", filepath)
        print("[DEBUG] Full resolved path:", full_path)

        requesting_user = g.get('user', None)
        target_folder = filepath.split('/')[0]  # e.g., 'guest', 'EY', 'admin', '..'

    

        return send_file(full_path, as_attachment=False)

    except Exception as e:
        print("[ERROR]", e)
        return "500 Internal Server Error", 500
