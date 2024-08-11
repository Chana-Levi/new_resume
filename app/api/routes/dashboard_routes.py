from flask import Blueprint, render_template, request, jsonify, session
from bson.objectid import ObjectId
from app import db

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/', methods=['GET'])
def dashboard():
    """
    Render the dashboard page with job and resume data.

    This route fetches all job postings and recent resumes from the database,
    and renders the 'dashboard.html' template with this data.

    Returns:
        Response: The rendered dashboard HTML page with job and resume data.
    """
    user_name = session.get('user_name')

    # Fetch job postings from the database
    jobs = db['job'].jobs.find().sort('date_uploaded', -1).limit(6)
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

    # Fetch recent resumes from the database
    resumes = db['resume'].resumes.find().sort('date_uploaded', -1).limit(6)  # Limiting to 6 recent resumes
    resume_data = []
    for resume in resumes:
        # Fetch the candidate information
        candidate = db['candidate'].candidates.find_one({'_id': resume['candidate_id']})
        job = db['job'].jobs.find_one({'_id': resume['job_id']})

        resume_data.append({
            'candidate_name': candidate.get('name', 'No Name'),
            'job_number': job.get('job_number', 'No Job Number'),
            'job_title': job.get('job_title', 'No Title'),
            'resume_id': str(resume['_id'])
        })

    return render_template('dashboard.html', job_data=job_data, resume_data=resume_data, user_name=user_name)


@dashboard_bp.route('/edit/<job_id>', methods=['POST'])
def edit_job(job_id):
    """
    Edit an existing job's details.

    Args:
        job_id (str): The ID of the job to edit.

    Returns:
        Response: JSON response indicating success or error.
    """
    job_title = request.form['job_title']
    job_number = request.form['job_number']
    job_description = request.form['job_description']

    if not db['jobs'].update_one({'_id': ObjectId(job_id)}, {'$set': {
        'job_title': job_title,
        'job_number': job_number,
        'job_description': job_description
    }}):
        return jsonify({'status': 'error'})

    return jsonify({'status': 'success'})


@dashboard_bp.route('/edit/savenmatch/<job_id>', methods=['POST'])
def save_and_match_job(job_id):
    if edit_job(job_id):
        db['match'].delete_many({'job_id': ObjectId(job_id)})
        resumes = db['resumes'].find({'job_id': ObjectId(job_id)})
        for resume in resumes:
            match_resumes(resume)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})


@dashboard_bp.route('/delete_job/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        job_id_obj = ObjectId(job_id)
        result = db['jobs'].delete_one({'_id': job_id_obj})

        resume_result = db['resumes'].delete_many({'job_id': job_id_obj})

        if result.deleted_count == 1:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Job not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
