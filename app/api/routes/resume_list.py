from flask import Blueprint, render_template
from app.db.resume_model import ResumeModel  # Import your Resume model

resume_list_bp = Blueprint('resume_list_bp', __name__)

@resume_list_bp.route('/resumes')
def resume_list():
    # Fetch all resumes from the database
    resumes = ResumeModel.get_all()
    return render_template('resume_list.html', resumes=resumes)
