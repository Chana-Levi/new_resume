from flask import Blueprint, render_template
from app import db

matching_bp = Blueprint('matching_bp', __name__, url_prefix='/matching')


@matching_bp.route('/', methods=['GET'])
def list_matches():
    """
    Renders the matching list page with match data.

    This route fetches all matches from the database, retrieves associated job and candidate details,
    and renders the 'matching.html' template with this data.

    Returns:
        Response: The rendered matching list HTML page with match data.
    """
    matches = db['match'].matches.find()
    matches_list = list(matches)
    updated_matches_list = []
    for match in matches_list:
        job = db['job'].get_job(match['job_id'])
        candidate = db['candidate'].get_candidate(match['candidate_id'])
        match = {
            "candidate_id": match['candidate_id'],
            "candidate_name": candidate['name'],
            "job_id": match['job_id'],
            "job_number": job['job_number'],
            "general_requirements": match['general_requirements'],
            "mandatory_requirements": match['mandatory_requirements'],
            "advantageous_requirements": match['advantageous_requirements'],
            "final_score": match['final_score'],
            "general_system_comments": match['general_system_comments'],
        }
        updated_matches_list.append(match)

    return render_template('matching.html', resumes=updated_matches_list)