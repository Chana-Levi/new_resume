# app/api/routes/main_routes.py
import os
from flask import Blueprint, request, render_template, redirect, url_for, send_from_directory, current_app, flash
from werkzeug.utils import secure_filename
import pypandoc

full_resume_bp = Blueprint('full_resume_bp', __name__, url_prefix='/full_resume')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx', 'txt'}


@full_resume_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            file_extension = filename.rsplit('.', 1)[1].lower()

            if file_extension == 'txt':
                with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'r') as f:
                    file_content = f.read()
            elif file_extension in {'doc', 'docx'}:
                file_content = pypandoc.convert_file(os.path.join(current_app.config['UPLOAD_FOLDER'], filename),
                                                     'html')
            else:
                file_content = None

            return render_template('full_resume.html', filename=filename, file_extension=file_extension,
                                   file_content=file_content)

    return render_template('full_resume.html')


@full_resume_bp.route('/display/<filename>')
def display_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
