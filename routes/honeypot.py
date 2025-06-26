from flask import Blueprint, request, make_response, abort
import os
import datetime
import random
import time

bp = Blueprint('honeypot', __name__, url_prefix='')

# Directory for logging
LOG_DIR = "/tmp/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_honeypot_hit(path):
    with open(os.path.join(LOG_DIR, "honeypot_access.log"), "a") as f:
        f.write(f"[{datetime.datetime.now()}] {request.remote_addr} requested {path}\n")

# Only respond to common brute-force path targets
HONEY_ALLOW = ['admin', 'backup', 'login', 'uploads', 'config', 'test', 'old', 'dev', 'private']

@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path):
    # --- Check if path is worth faking ---
    if not any(path.startswith(p) for p in HONEY_ALLOW):
        return abort(404)  # Realistic behavior: unknown path = not found

    log_honeypot_hit(path)

    # --- Random delay to mess with scanners ---
    time.sleep(random.uniform(0.1, 1.2))  # 100ms to 1.2s

    # --- Generate fake file/directory listing ---
    fake_dirs = [f"dir_{random.randint(1000,9999)}" for _ in range(random.randint(2, 5))]
    fake_files = [f"file_{random.randint(1000,9999)}.php" for _ in range(random.randint(1, 4))]

    html = f"<h1>Index of /{path}</h1><ul>"
    for d in fake_dirs:
        html += f"<li><a href='/{path}/{d}/'>{d}/</a></li>"
    for f in fake_files:
        html += f"<li><a href='/{path}/{f}'>{f}</a></li>"
    html += "</ul>"

    # --- Random HTTP status ---
    status = random.choices(
        [200, 403, 401, 500],
        weights=[70, 15, 10, 5]
    )[0]

    # --- Build response ---
    resp = make_response(html)
    resp.status_code = status
    resp.headers['Content-Type'] = 'text/html'
    resp.headers['Server'] = random.choice([
        'Apache/2.4.41 (Ubuntu)',
        'nginx/1.18.0',
        'Microsoft-IIS/10.0'
    ])
    resp.headers['X-Powered-By'] = random.choice([
        'PHP/7.4.3', 'Express', 'ASP.NET', 'Flask'
    ])
    return resp
