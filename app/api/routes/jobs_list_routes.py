from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from app.services.file_services.orchestration_service import extract_and_query
from app.utils.helpers import format_description
import os
from app import db


UPLOAD_FOLDER = 'app/static/uploads/'
FILES_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'files/')
os.makedirs(FILES_UPLOAD_FOLDER, exist_ok=True)

jobs_list_bp = Blueprint('jobs_list_bp', __name__, url_prefix='/jobs_list')


@jobs_list_bp.route('/', methods=['GET'])
def jobs_list():
    """
    Renders the jobs list page with job data.

    This route fetches all job postings from the database, formats their descriptions,
    and renders the 'jobs_list.html' template with this data.

    Returns:
        Response: The rendered jobs list HTML page with job data.
    """
    jobs = db['job'].jobs.find()

    all_jobs = list(jobs)
    for job in all_jobs:
        job['job_description'] = format_description(job['job_description'])
    return render_template('jobs_list.html', jobs=all_jobs)


@jobs_list_bp.route('/upload_resume', methods=['POST'])
def upload_resume():
    """
    Handles the upload of a resume file.

    This route processes a resume file uploaded through a form, saves it to the
    server, and extracts and queries the information from the resume using the
    `extract_and_query` function.

    Returns:
        Response: JSON response indicating success or error.
    """
    job_id = request.form['job_id']
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    resume_file = request.files['resume']
    if resume_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if resume_file:
        filename = secure_filename(resume_file.filename)
        file_path = os.path.join(FILES_UPLOAD_FOLDER, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        resume_file.save(file_path)
        return extract_and_query(file_path, job_id)