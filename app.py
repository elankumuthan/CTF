from flask import Flask, send_from_directory, g
from routes import auth, upload, profile, comment, download
import os

app = Flask(__name__)
app.secret_key = 'this_is_secret'

app.config['UPLOAD_FOLDER'] = 'uploads'
# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(upload.bp)
app.register_blueprint(profile.bp)
app.register_blueprint(comment.bp)
app.register_blueprint(download.bp)

@app.route('/uploads/<user>/<filename>')
def serve_user_file(user, filename):
    if g.user != user and g.user != "admin":
        return "Forbidden", 403
    return send_from_directory(f"uploads/{user}", filename)

if __name__ == '__main__':
    # Ensure uploads folder exists
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
