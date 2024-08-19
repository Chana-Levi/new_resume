from flask import Blueprint, render_template

aaa_bp = Blueprint('aaa_bp', __name__, url_prefix='/aaa')


@aaa_bp.route('/', methods=['GET'])
def add_job():
    """
    Render the add job page.

    Returns:
        Response: Rendered HTML page for adding a job.
    """
    return render_template('aaa.html')