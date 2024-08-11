from flask import Blueprint, render_template


nav_bp = Blueprint('nav_bp', __name__, template_folder='../templates', url_prefix='/')


@nav_bp.route('/', methods=['GET'])
def nav():
    return render_template("nav.html")

