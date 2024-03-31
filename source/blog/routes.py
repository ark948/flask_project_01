from source.blog import bp
from flask import render_template

@bp.route('/')
def index():
    return render_template('blog/index.html')