from flask import render_template
from source.shop import bp

@bp.route('/')
def index():
    return render_template('shop/index.html')