from flask import Blueprint, request, send_file, make_response, g, render_template_string
import os
from urllib.parse import quote

bp = Blueprint('uploads', __name__, url_prefix='/uploads')
UPLOADS_ROOT = os.path.abspath('uploads')

# Whitelist of folders that can be accessed via path traversal
# Any files within these folders will also be accessible
ACCESSIBLE_FOLDERS = {
    'etc',
    'home',
    'tmp',
    'var',
    'bin',
    'lib',
    'usr',

    # Add more folders that should be accessible for your CTF
}

def is_path_whitelisted(filepath):
    """Check if the resolved path is within a whitelisted folder"""
    # Get all parent directories of the file/folder
    path_parts = []
    current_path = os.path.abspath(filepath)
    
    while True:
        parent, folder = os.path.split(current_path)
        if folder:
            path_parts.append(folder)
            current_path = parent
        else:
            break
    
    # Check if any parent directory is in the whitelist
    for folder in path_parts:
        if folder in ACCESSIBLE_FOLDERS:
            return True
    
    return False

# Whitelist of folders that can be accessed via path traversal
# Any files within these folders will also be accessible
ACCESSIBLE_FOLDERS = {
    'etc',
    'home'
    # Add more folders that should be accessible for your CTF
}

def is_path_whitelisted(filepath):
    """Check if the resolved path is within a whitelisted folder"""
    # Get all parent directories of the file/folder
    path_parts = []
    current_path = os.path.abspath(filepath)
    
    while True:
        parent, folder = os.path.split(current_path)
        if folder:
            path_parts.append(folder)
            current_path = parent
        else:
            break
    
    # Check if any parent directory is in the whitelist
    for folder in path_parts:
        if folder in ACCESSIBLE_FOLDERS:
            return True
    
    return False

@bp.route('/<user>/<filename>', methods=['GET'])
def serve_user_file(user, filename):
    try:
        if g.user != user and g.user != "3y_adm!n!strat0r":
            return "Forbidden", 403
        
        user_path = os.path.abspath(os.path.join(UPLOADS_ROOT, user))
        full_path = os.path.abspath(os.path.join(user_path, filename))
        
        # Keep the path traversal vulnerability but check whitelist
        if not full_path.startswith(user_path):
            # This is a path traversal attempt - check if target file is whitelisted
            if not is_path_whitelisted(full_path):
                return "Access denied", 403
        
        if not os.path.exists(full_path):
            return "File not found", 404
            
        # Double-check whitelist for all files outside user directory
        if not full_path.startswith(user_path) and not is_path_whitelisted(full_path):
            return "Access denied", 403
        
        if request.headers.get('X-Render', '').lower() == 'true':
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                contents = f.read()
            return render_template_string(contents)
        
        return send_file(full_path, as_attachment=False)
        
    except Exception as e:
        print("[ERROR]", e)
        return "500 Internal Server Error", 500

@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def uploads_index(path):
    target_path = os.path.abspath(os.path.join(UPLOADS_ROOT, path))
    
    if not os.path.exists(target_path):
        return "404 Not Found", 404
    
    # Check whitelist for any path outside UPLOADS_ROOT (both files and directories)
    if not target_path.startswith(UPLOADS_ROOT) and not is_path_whitelisted(target_path):
        return "Access denied", 403
    
    if os.path.isfile(target_path):
        return send_file(target_path)
    
    try:
        entries = os.listdir(target_path)
        html = f"<h1>Index of /uploads/{path}/</h1><ul>"
        for entry in sorted(entries):
            entry_path = os.path.join(target_path, entry)
            slash = '/' if os.path.isdir(entry_path) else ''
            href = f"{request.path.rstrip('/')}/{quote(entry)}{slash}"
            html += f"<li><a href='{href}'>{entry}{slash}</a></li>"
        html += "</ul>"
        
        resp = make_response(html)
        resp.status_code = 200
        resp.headers['Content-Type'] = 'text/html'
        return resp
        
    except Exception as e:
        return f"<h1>Error</h1><pre>{e}</pre>", 500