from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app import db

resume_list_bp = Blueprint('resume_list_bp', __name__, url_prefix='/resume_list')


@resume_list_bp.route('/', methods=['GET'])
def resume_list():
    resumes = db['resume'].resumes.find()
    all_resumes = list(resumes)
    processed_resumes = []
    print("all_resumes", all_resumes)
    for resume in all_resumes:
        print("in for statement", str(resume.get('candidate_id')))
        candidate = db['candidate'].get_candidate(str(resume.get('candidate_id')))
        job = db['job'].get_job(str(resume.get('job_id')))

        processed_resumes.append({
            'id': str(resume.get('_id')),  # Add the resume ID here
            'name': candidate['name'],
            'job_number': job['job_number'],
            'hasNotification': False,
            'resume_link': url_for('resume_bp.show_resume', resume_id=str(resume.get('_id')))  # Updated link
        })
        print("all_resumes", all_resumes[0])

    return render_template('resume_list.html', resumes=processed_resumes)


@resume_list_bp.route('/delete_resume/<resume_id>', methods=['POST'])
def delete_resume(resume_id):
    job_id = request.form['job_id']
    db['resume'].delete_resume(resume_id)
    return redirect(url_for('resume_list_bp.resume_list', job_id=job_id))


