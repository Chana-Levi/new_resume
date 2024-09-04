from flask import Blueprint, render_template

mishra_number_bp = Blueprint('mishra_number_bp', __name__, url_prefix='/mishra_number')


@mishra_number_bp.route('/', methods=['GET'])
def mishra_number():
    """
    Render the add job page.

    Returns:
        Response: Rendered HTML page for adding a job.
    """
    return render_template('mishra_number.html')