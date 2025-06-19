from flask import Blueprint, request, render_template
from .utils.login_required import login_required


bp = Blueprint('comment', __name__)

@bp.route('/comment')
@login_required
def comment():
    return("Comment route is working")
