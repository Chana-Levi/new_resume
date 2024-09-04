from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from app.services.file_services.orchestration_service import extract_and_query
from app.utils.helpers import format_description
import os
from app import db
from bson.objectid import ObjectId

UPLOAD_FOLDER = 'app/static/uploads/'
FILES_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'files/')
os.makedirs(FILES_UPLOAD_FOLDER, exist_ok=True)

jobs_list_bp = Blueprint('jobs_list_bp', __name__, url_prefix='/jobs_list')


def combine_requirements(job):
    """Combines general, mandatory, and advantageous requirements into a single string."""
    requirements = []
    if job.get('mandatory_requirements'):
        requirements.append(f"Mandatory: {', '.join(job['mandatory_requirements'])}")
    if job.get('general_requirements'):
        requirements.append(f"General: {', '.join(job['general_requirements'])}")
    if job.get('advantageous_requirements'):
        requirements.append(f"Advantageous: {', '.join(job['advantageous_requirements'])}")
    return "\n".join(requirements)


@jobs_list_bp.route('/', methods=['GET'])
def jobs_list():
    jobs = db['job'].jobs.find()

    all_jobs = list(jobs)
    for job in all_jobs:
        job['job_description'] = format_description(job['job_description'])
        job['valid_date'] = job.get('opening_valid_date', 'No date provided')
        job['requirements'] = combine_requirements(job)  # Combine requirements

    return render_template('jobs_list.html', jobs=all_jobs)


@jobs_list_bp.route('/upload_resume', methods=['POST'])
def upload_resume():
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


@jobs_list_bp.route('/edit_job', methods=['POST'])
def edit_job():
    data = request.get_json()

    job_id = data.get('job_id')
    job_title = data.get('job_title')
    job_description = data.get('job_description')
    valid_date = data.get('valid_date')
    requirements = data.get('requirements')

    try:
        # Update the job in the database
        db['job'].jobs.update_one(
            {'_id': job_id},
            {'$set': {
                'job_title': job_title,
                'job_description': job_description,
                'valid_date': valid_date,
                'requirements': requirements
            }}
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})


@jobs_list_bp.route('/delete_job', methods=['POST'])
def delete_job():
    data = request.get_json()
    job_id = data.get('job_id')

    try:
        job_object_id = ObjectId(job_id)

        result = db['job'].jobs.delete_one({'_id': job_object_id})

        if result.deleted_count == 1:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Job not found or could not be deleted.'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
