from flask import Blueprint, render_template_string, send_file
import os

bp = Blueprint('download', __name__, url_prefix='/download')

@bp.route('/<path:filepath>', methods=['GET'])
def download(filepath):
    try:
        full_path = os.path.abspath(os.path.join('uploads', filepath))
        print("[DEBUG] Full resolved path:", full_path)

        if not os.path.isfile(full_path):
            return "404 File not found", 404

        if full_path.endswith('.txt'):
            with open(full_path) as f:
                contents = f.read()
            return render_template_string(contents)

        return send_file(full_path, as_attachment=False)

    except Exception as e:
        print("[ERROR]", e)
        return "500 Internal Server Error", 500
