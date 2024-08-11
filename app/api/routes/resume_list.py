from flask import Blueprint, render_template


resume_list_bp = Blueprint('resume_list_bp', __name__, url_prefix='/resume_list')


@resume_list_bp.route('/', methods=['GET'])
def resume_list():
    return render_template("resume_list.html")