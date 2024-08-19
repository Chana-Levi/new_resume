from flask import Blueprint, render_template
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
            'name': candidate['name'],
            'job_number': job['job_number'],
            'hasNotification': False
        })
        print("all_resumes", all_resumes[0])

    return render_template('resume_list.html', resumes=processed_resumes)
