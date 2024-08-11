from flask import Blueprint, render_template, request, jsonify
from app.services.file_services.match_service import match_resumes
from bson.objectid import ObjectId
from app import db

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/', methods=['GET'])
def dashboard():
    """
    Render the dashboard page with job data.

    This route fetches all job postings from the database,
    calculates the number of applicants for each job, and
    renders the 'dashboard.html' template with this data.

    Returns:
        Response: The rendered dashboard HTML page with job data.
    """
    # jobs = db.jobs.find()
    jobs = db['job'].jobs.find()
    print("---jobs---", jobs)
    job_data = []
    for job in jobs:
        job_id = job['_id']
        job_title = job.get('job_title', 'No Title')
        job_description = job.get('job_description', 'No Description')
        job_number = job.get('job_number', 'No Job Number')

        num_applicants = db['resume'].resumes.count_documents({'job_id': job_id})

        job_data.append({
            '_id': job_id,
            'job_title': job_title,
            'job_description': job_description,
            'job_number': job_number,
            'num_applicants': num_applicants
        })

    return render_template('dashboard.html', job_data=job_data)


@dashboard_bp.route('/edit/<job_id>', methods=['POST'])
def edit_job(job_id):
    """
    Edit an existing job's details.

    Args:
        job_id (str): The ID of the job to edit.

    Returns:
        Response: JSON response indicating success or error.
    """
    print("edit job func")
    job_title = request.form['job_title']
    job_number = request.form['job_number']
    job_description = request.form['job_description']
    # existing_job = db.get_job(job_id)
    if not db['job'].update_job(job_id, job_title, job_number, job_description):
        return jsonify({'status': 'error'})
    # if existing_job['job_description'] != job_description:
    #     db.delete_matches_by_job_id(job_id)
    #     resumes = db.get_resumes_by_job_id(job_id)
    #     for resume in resumes:
    #         match_resumes(resume)
    return jsonify({'status': 'success'})


@dashboard_bp.route('/edit/savenmatch/<job_id>', methods=['POST'])
def save_and_match_job(job_id):
    print("save and change job func")
    # TODO: why do we need to do this if?
    if edit_job(job_id):
        db['match'].delete_matches_by_job_id(job_id)
        resumes = db['resume'].get_resumes_by_job_id(job_id)
        for resume in resumes:
            match_resumes(resume)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})


@dashboard_bp.route('/delete_job/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    """
    Delete a job and its associated resumes.

    Args:
        job_id (str): The ID of the job to delete.

    Returns:
        Response: JSON response indicating success or error.
    """
    try:
        print(f"Received request to delete job with ID: {job_id}")  # Debug message
        job_id_obj = ObjectId(job_id)
        # Delete the job
        result = db['job'].jobs.delete_one({'_id': job_id_obj})
        print(f"Job delete result: {result.deleted_count}")  # Debug message

        # Delete associated resumes
        resume_result = db['resume'].resumes.delete_many({'job_id': job_id_obj})
        print(f"Resume delete result: {resume_result.deleted_count}")  # Debug message

        if result.deleted_count == 1:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Job not found'})
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug message in case of an error
        return jsonify({'success': False, 'error': str(e)})