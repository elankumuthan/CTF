from flask import Flask, send_from_directory, g, Blueprint
from routes import auth, upload, profile, comment, uploads, honeypot
import os

app = Flask(__name__)
app.secret_key = 'this_is_secret'

app.config['UPLOAD_FOLDER'] = 'uploads'

# Register blueprints 
app.register_blueprint(auth.bp)
app.register_blueprint(upload.bp)
app.register_blueprint(profile.bp)
app.register_blueprint(comment.bp)
app.register_blueprint(uploads.bp)
app.register_blueprint(honeypot.bp)

# Add HTTP-ish headers so nmap -sV recognizes this as http on a nonstandard port
@app.after_request
def force_http_identification(response):
    # Help nmap’s service detection (don’t override if something already set it)
    response.headers.setdefault("Server", "Apache/2.4.41 (Ubuntu)")
    # Only set Content-Type if missing so file downloads etc. aren’t broken
    if not response.headers.get("Content-Type"):
        response.headers["Content-Type"] = "text/html; charset=UTF-8"
    return response

@app.route('/profile_photo/<user>/<filename>')
def serve_profile_photo(user, filename):
    if g.user != user and g.user != "3y_adm!n!strat0r":
        return "Forbidden", 403
    return send_from_directory(f"profile_photo/{user}", filename)

if __name__ == '__main__':
    # Ensure uploads folder exists
    os.makedirs('uploads', exist_ok=True)
    # Bind to 49200 so nmap scans that port
    app.run(debug=True, host='0.0.0.0', port=49200)
