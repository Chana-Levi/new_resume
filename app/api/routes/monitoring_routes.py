import os
from flask import Blueprint, render_template, request
from app.services.file_services.monitoring_service import start_monitoring

monitoring_bp = Blueprint('monitoring_bp', __name__, url_prefix='/monitoring')


@monitoring_bp.route('/', methods=['GET'])
def monitoring():
    """
    Renders the monitoring page.

    This route renders the 'monitoring.html' template which is the user interface for the monitoring functionality.

    Returns:
        Response: The rendered monitoring HTML page.
    """
    return render_template('monitoring.html')


@monitoring_bp.route('/listening', methods=['POST'])
def listening():
    """
    Starts monitoring a specified directory for new files.

    This route accepts a folder path via a POST request, verifies if the path exists,
    and starts a separate thread to monitor the directory for new files.

    Returns:
        str: A message indicating the monitoring status or an error if the folder path is invalid.
    """
    folder_path = request.form.get('folder_path')
    if not os.path.isdir(folder_path):
        return f"The specified folder path does not exist: {folder_path}", 400
    return start_monitoring(folder_path)