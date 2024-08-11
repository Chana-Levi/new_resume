import os
import json
from flask import jsonify
from app import db
from app.services.file_services.match_service import match_resumes
from app.services.file_services.extraction_service import extract_info
from app.services.file_services.query_service import query, parse_response_to_dict


def extract_and_query(file_path, job_id):
    content = extract_info(file_path)
    if not content:
        return jsonify({'error': 'Failed to extract information from the resume.'}), 400
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'static', 'json_templates', 'cv_template.json')
    with open(json_path, 'r') as json_file:
        cv_data_template = json.load(json_file)
    query_request = (f"extract the following details from the text: {cv_data_template} \nMake sure your response is a"
                     f" valid json format")
    response = query(content, query_request)
    if not response:
        return jsonify({'error': 'Failed to query to llamaindex.'}), 400
    extraction_result = parse_response_to_dict(response)
    if not extraction_result:
        return jsonify({'error': 'Failed to parse_response_to_dictionary.'}), 400
    name = extraction_result['personal_information']['name']
    email = extraction_result['personal_information']['contact_info']['email']
    if name and email:
        candidate_model = db['candidate']
        resume_model = db['resume']
        match_model = db['match']
        candidate = candidate_model.find_candidate(name, email)
        if candidate:
            id_candidate = candidate['_id']
        else:
            id_candidate = candidate_model.add_candidate(email, name)
        existing_resume = resume_model.find_resume(id_candidate, job_id)
        if existing_resume:
            old_file_path = existing_resume['resume_link']
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            resume_model.update_resume_by_id_and_job(id_candidate, job_id, content, extraction_result, file_path)
            id_resume = existing_resume['_id']
            match_model.delete_match_by_candidate_and_job(id_candidate, job_id)
        else:
            id_resume = resume_model.add_resume(id_candidate, job_id, content, extraction_result, file_path)
        match_resumes(resume_model.get_resume(id_resume))
        return jsonify({'success': True, 'message': 'Resume has been successfully uploaded.'})
    else:
        return jsonify({'error': 'Name or email is missing in the extracted details.'}), 400
