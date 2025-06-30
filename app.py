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


@app.route('/profile_photo/<user>/<filename>')
def serve_profile_photo(user, filename):
    if g.user != user and g.user != "3y_adm!n!strat0r":
        return "Forbidden", 403
    return send_from_directory(f"profile_photo/{user}", filename)


if __name__ == '__main__':
    # Ensure uploads folder exists
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=80)
