from flask import Blueprint, jsonify, render_template, request
from app import db
from app.services.file_services.query_service import query, parse_response_to_dict
import os
import json

add_job_bp = Blueprint('add_job_bp', __name__, url_prefix='/add_job')


@add_job_bp.route('/', methods=['GET'])
def add_job():
    """
    Render the add job page.

    Returns:
        Response: Rendered HTML page for adding a job.
    """
    return render_template('add_job.html')


@add_job_bp.route('/job_content', methods=['POST'])
def job_content():
    """
    Handle the form submission for adding a job.

    Extract job details from the form, use a template to structure the query,
    extract relevant details from the response, and add the job to the database.

    Returns:
        Response: JSON response containing the job title, job number, and job description.
    """
    job_title = request.form['job_title']
    job_description = request.form['job_description']
    job_number = request.form['job_number']

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'static', 'json_templates', 'job_template.json')
    with open(json_path, 'r') as json_file:
        cv_data_template = json.load(json_file)

    query_request = (f"extract the following details from the text: {cv_data_template} \nMake sure your response is a "
                     f"valid json format")
    response = query(f"{job_title} \n {job_description} \n {job_number}", query_request)
    extracted_details = parse_response_to_dict(response)

    company_name = extracted_details.get('organization_name')
    general_requirements = extracted_details.get('general_requirements', [])
    mandatory_requirements = extracted_details.get('mandatory_requirements', [])
    advantageous_requirements = extracted_details.get('advantageous_requirements', [])
    link_to_file = extracted_details.get('link_to_file', '')
    job_model = db['job']
    job_id = job_model.add_job(company_name, job_title, job_number, job_description, link_to_file,
                               mandatory_requirements,
                               general_requirements, advantageous_requirements)
    if not job_id:
        return "The job not added to mongo db"
    return jsonify({
        "job_title": job_title,
        "job_number": job_number,
        "job_description": job_description
    })