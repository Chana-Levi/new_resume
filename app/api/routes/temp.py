from flask import Blueprint, render_template


temp_bp = Blueprint('temp_bp', __name__, url_prefix='/temp')


@temp_bp.route('/', methods=['GET'])
def temp():
    return render_template("temp.html")