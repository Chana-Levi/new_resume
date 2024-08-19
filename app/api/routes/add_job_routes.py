from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from app import db
from app.services.file_services.query_service import query, parse_response_to_dict
import os
import json

add_job_bp = Blueprint('add_job_bp', __name__, url_prefix='/add_job')


@add_job_bp.route('/', methods=['GET'])
def add_job():
    """
    Render the add job page with optional pre-filled data.

    Returns:
        Response: Rendered HTML page for adding a job.
    """
    job_title = request.args.get('job_title', '')
    job_number = request.args.get('job_number', '')
    job_description = request.args.get('job_description', '')
    requirements = request.args.get('requirements', '')
    opening_valid_date = request.args.get('opening_valid_date', '')

    return render_template(
        'add_job.html',
        job_title=job_title,
        job_number=job_number,
        job_description=job_description,
        requirements=requirements,
        opening_valid_date=opening_valid_date
    )


@add_job_bp.route('/job_content', methods=['POST'])
def job_content():
    """
    Handle the form submission for adding a job.

    Validate form inputs, check if the job exists, and either redirect to the confirmation page or show an error.

    Returns:
        Response: Redirects to the job confirmation page if successful,
                  or renders the add job page with an error message if unsuccessful.
    """
    job_title = request.form['job_title']
    job_description = request.form['job_description']
    job_number = request.form['job_number']
    requirements = request.form['requirements']
    date = request.form['opening_valid_date']
    print("date", date)

    # Validate that all fields are filled
    if not job_title or not job_description or not job_number:
        flash("All fields are required.", "error")
        return render_template('add_job.html')

    # Example check for existing job - Adjust this according to your database logic
    existing_job = db['job'].jobs.find_one({"job_number": job_number})
    if existing_job:
        flash("Job with this number already exists.", "error")
        return render_template('add_job.html')

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'static', 'json_templates', 'job_template.json')
    with open(json_path, 'r') as json_file:
        cv_data_template = json.load(json_file)

    query_request = (f"extract the following details from the text: {cv_data_template} \nMake sure your response is a "
                     f"valid json format")
    response = query(f"{job_title} \n {job_description} \n {job_number} \n {requirements}", query_request)
    extracted_details = parse_response_to_dict(response)

    company_name = extracted_details.get('organization_name')
    general_requirements = extracted_details.get('general_requirements', [])
    mandatory_requirements = extracted_details.get('mandatory_requirements', [])
    advantageous_requirements = extracted_details.get('advantageous_requirements', [])
    link_to_file = extracted_details.get('link_to_file', '')
    job_model = db['job']
    job_id = job_model.add_job(company_name, job_title, job_number, job_description, link_to_file, date,
                               mandatory_requirements,
                               general_requirements, advantageous_requirements)
    if not job_id:
        flash("The job could not be added to the database.", "error")
        return render_template('add_job.html')

    return redirect(url_for('add_job_bp.job_confirmation', job_title=job_title, job_number=job_number))


@add_job_bp.route('/job_confirmation')
def job_confirmation():
    """
    Render the job confirmation page after a job has been successfully created.

    Returns:
        Response: Rendered HTML page for job confirmation.
    """
    job_title = request.args.get('job_title')
    job_number = request.args.get('job_number')
    return render_template('job_confirmation.html', job_title=job_title, job_number=job_number)
