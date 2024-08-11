from flask import Blueprint, render_template


job_confirmation_bp = Blueprint('job_confirmation_bp', __name__, url_prefix='/job_confirmation')


@job_confirmation_bp.route('/', methods=['GET'])
def job_confirmation():
    return render_template("job_confirmation.html")

