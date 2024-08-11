from flask import current_app
from app import db
from app.services.file_services.query_service import query, parse_response_to_dict
import os
import json


def match_resumes(resume):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'static', 'json_templates', 'matching_template.json')
    with open(json_path, 'r') as json_file:
        matching_template = json.load(json_file)
    job_model = db['job']
    match_model = db['match']
    job = job_model.get_job(resume['job_id'])
    full_text_resume = resume['full_text_resume']

    text = f"full text resume {full_text_resume}"
    q = (f"instruction: Give a score 0-5 for each requirement according to the job requirements, calculate the "
         f"final score and write an opinion on the level of compatibility between the job and the resume. Return "
         f"the results as a dictionary matching the matching template. Make sure your response is a valid json "
         f"format. job_requirements: {job}, matching_template: {matching_template}")
    query_result = query(text, q)
    extracted_result = parse_response_to_dict(query_result)
    if extracted_result:
        general_requirements = extracted_result.get('general_requirements', {})
        mandatory_requirements = extracted_result.get('mandatory_requirements', {})
        advantageous_requirements = extracted_result.get('advantageous_requirements', {})
        final_score = extracted_result.get('final_score', "")
        general_comments = extracted_result.get('general_system_comments', "")

        if general_requirements or mandatory_requirements or advantageous_requirements:
            id_matching = match_model.add_match(resume['candidate_id'], resume['job_id'], general_requirements,
                                                mandatory_requirements, advantageous_requirements, final_score,
                                                general_comments)
            print(f"Match added with ID: {id_matching}")
        else:
            print("No matching requirements found")