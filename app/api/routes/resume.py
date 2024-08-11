from flask import Blueprint, render_template, request
from app import db
from bson.objectid import ObjectId

resume_bp = Blueprint('resume_bp', __name__, url_prefix='/resume')


@resume_bp.route('/', methods=['GET'])
def show_resume():
    # resume = db['resume'].resumes.find_one({}, sort=[('date_uploaded', -1)])
    resume_id = request.args.get('resume_id')

    if not resume_id:
        return "No resume ID provided", 400

    resume = db['resume'].resumes.find_one({"_id": ObjectId(resume_id)})

    # resume_id = db['resume'].resumes.find().sort('date_uploaded', -1).limit(1)
    # resume_id = resume.get('_id')
    # resume = db['resume'].resumes.find_one({"_id": ObjectId(resume_id)})

    # Extracting the data from the 'extract_resume' field
    extract_resume = resume.get('extract_resume', {})

    # Breaking down the dictionary for easy access in the template
    personal_info = extract_resume.get('personal_information', {})
    summary = extract_resume.get('summary', '')
    experience = extract_resume.get('professional_experience', [])
    education = extract_resume.get('education', [])
    skills = extract_resume.get('skills', [])
    tools = extract_resume.get('tools', [])
    languages = extract_resume.get('languages', [])

    # Pass the data to the template
    return render_template("resume.html",
                           personal_info=personal_info,
                           summary=summary,
                           experience=experience,
                           education=education,
                           skills=skills,
                           tools=tools,
                           languages=languages)
