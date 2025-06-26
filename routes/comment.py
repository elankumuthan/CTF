from flask import Blueprint, request, render_template, redirect, g
from .utils.login_required import login_required
import sqlite3
from datetime import datetime
import os

bp = Blueprint('comment', __name__)
COMMENTS_DB = 'utils/comments.db'

@bp.route('/comment', methods=['GET', 'POST'])
@login_required
def comment():
    if request.method == 'POST':
        username = g.user
        author = request.form.get('author', 'anonymous').strip()
        message = request.form.get('message', '').strip()

        if not message:
            return redirect('/comment?error=empty')

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            conn = sqlite3.connect(COMMENTS_DB)
            c = conn.cursor()
            c.execute('''
                INSERT INTO comments (user, author, timestamp, message)
                VALUES (?, ?, ?, ?)
            ''', (username, author, timestamp, message))
            conn.commit()
            conn.close()
        except Exception as e:
            print("[!] Error saving comment:", e)

        return redirect('/comment')

    # Load all comments
    comments = []
    try:
        conn = sqlite3.connect(COMMENTS_DB)
        c = conn.cursor()
        c.execute("SELECT author, timestamp, message FROM comments ORDER BY id DESC LIMIT 25")
        rows = c.fetchall()
        conn.close()

        for row in rows:
            comments.append({
                "author": row[0],
                "timestamp": row[1],
                "message": row[2]
            })
    except Exception as e:
        print("[!] Error loading comments:", e)

    error = request.args.get('error')
    return render_template('comment.html', comments=comments, error=error)
