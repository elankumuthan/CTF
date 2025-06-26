from flask import Blueprint, render_template_string, send_file
import os

bp = Blueprint('uploads', __name__, url_prefix='/uploads')

@bp.route('/', defaults={'filepath': ''})
@bp.route('/<path:filepath>', methods=['GET'])
def uploads(filepath):
    try:
        uploads_root = os.path.abspath('uploads')
        full_path = os.path.abspath(os.path.join(uploads_root, filepath))
        print("[DEBUG] Full resolved path:", full_path)

        # If directory, list contents
        if os.path.isdir(full_path):
            entries = os.listdir(full_path)
            links = [
                f'<li><a href="{filepath}/{entry}">{entry}</a></li>' if filepath else f'<li><a href="{entry}">{entry}</a></li>'
                for entry in entries
            ]
            return render_template_string(f"""
                <h1>Index of /uploads/{{{{ filepath }}}}</h1>
                <ul>
                    {''.join(links)}
                </ul>
            """, filepath=filepath)

        # If it's a .txt file, render it with template injection (for XSS/SSTI)
        if full_path.endswith('.txt'):
            with open(full_path) as f:
                contents = f.read()
            return render_template_string(contents)

        # Else: serve file normally
        return send_file(full_path, as_attachment=False)

    except Exception as e:
        print("[ERROR]", e)
        return "500 Internal Server Error", 500
