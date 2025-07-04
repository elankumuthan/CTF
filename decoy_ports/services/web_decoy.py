
#!/usr/bin/env python3
# services/web_decoy.py - Convincing web app with fake vulnerabilities
from flask import Flask, request, render_template_string
import time

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>SecureCorp Internal Portal</title></head>
    <body>
        <h1>SecureCorp Employee Portal</h1>
        <p>Last successful login: admin@securecorp.local</p>
        <ul>
            <li><a href="/admin">Admin Panel</a></li>
            <li><a href="/backup">Backup Files</a></li>
            <li><a href="/api/config">API Config</a></li>
        </ul>
        <!-- Debug: Remove before production -->
        <p style="color:red">Debug mode enabled. Check /var/log/debug.log</p>
    </body>
    </html>
    '''

@app.route('/admin')
def admin():
    # Waste time
    time.sleep(3)
    return '''
    <h1>Admin Panel</h1>
    <p>Access denied. IP logged.</p>
    <p>Try default credentials: admin/admin123</p>
    '''

@app.route('/backup')
def backup():
    return '''
    <h1>Backup Directory</h1>
    <ul>
        <li><a href="/backup/database.sql">database.sql</a> - Contains user table</li>
        <li><a href="/backup/config.conf">config.conf</a> - Server configuration</li>
    </ul>
    '''

@app.route('/backup/<filename>')
def download_backup(filename):
    time.sleep(2)
    return f'# Backup file: {filename}\n# Access denied - insufficient privileges\n# Contact sysadmin for access'

@app.route('/api/config')
def api_config():
    return '''
    {
        "database": "mysql://admin:password123@localhost/ctf_db",
        "debug": true,
        "flag_location": "/var/flags/not_here.txt"
    }
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)