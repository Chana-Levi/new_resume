from flask import Blueprint, redirect, render_template, request, jsonify, url_for
import json
from app import db

resume_list_bp = Blueprint('resume_list_bp', __name__, url_prefix='/resume_list')


@resume_list_bp.route('/', methods=['GET'])
def resume_list():
    jobs = db['job'].jobs.find()
    job_list = list(jobs)
    selected_job = None
    resumes = []

    job_id = request.args.get('job_id')
    if job_id:
        selected_job = db['job'].get_job(job_id)
        resumes = db['resume'].get_resumes_by_job_id(job_id)

    return render_template('resume_list.html', jobs=job_list, resumes=list(resumes), selected_job=selected_job)


@resume_list_bp.route('/delete_resume/<resume_id>', methods=['POST'])
def delete_resume(resume_id):
    job_id = request.form['job_id']
    db['resume'].delete_resume(resume_id)
    return redirect(url_for('resume_list_bp.resume_list', job_id=job_id))


@resume_list_bp.route('/view_resume/<resume_id>', methods=['GET'])
def view_resume(resume_id):
    resume = db['resume'].get_resume(resume_id)
    if resume:
        return jsonify({'resume_text': resume['extract_resume']})
    return jsonify({'error': 'Resume not found'}), 404


@resume_list_bp.route('/view_resume_link/<resume_id>', methods=['GET'])
def view_resume_link(resume_id):
    resume = db['resume'].get_resume(resume_id)
    if resume:
        return jsonify({'resume_link': resume['resume_link']})
    return jsonify({'error': 'Resume not found'}), 404


@resume_list_bp.route('/edit_resume/<resume_id>', methods=['POST'])
def edit_resume(resume_id):
    updated_data = request.get_json()
    extract_resume_data = json.loads(updated_data['extract_resume'])
    result = db['resume'].update_resume(resume_id, extract_resume_data)
    if result.modified_count == 1:
        return jsonify({'success': True, 'message': 'Resume updated successfully.'})
    else:
        return jsonify({'success': False, 'message': 'Resume update failed.'})
