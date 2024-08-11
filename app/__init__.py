# app/__init__.py
from flask import Flask
from config import Config
from authlib.integrations.flask_client import OAuth
from app.db.mongo_connection import db_connection
from app.db.job_model import JobModel
from app.db.match_model import MatchModel
from app.db.resume_model import ResumeModel
from app.db.candidate_model import CandidateModel
from app.db.organization_model import OrganizationModel
from app.db.mongo_connection import MongoDB

oauth = OAuth()
db = {}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    oauth.init_app(app)

    oauth.register(
        name='google',
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url="https://www.googleapis.com/oauth2/v1/",
        client_kwargs={'scope': 'profile email'},
        server_metadata_url=Config.GOOGLE_DISCOVERY_URL,
    )

    # Initialize database models
    global db
    db_connect = MongoDB(uri='mongodb://localhost:27017/', db_name='my_resume').get_database()
    db = {
        'organization': OrganizationModel(db_connect),
        'candidate': CandidateModel(db_connect),
        'resume': ResumeModel(db_connect),
        'job': JobModel(db_connect),
        'match': MatchModel(db_connect),
    }

    print("DB Initialized: ", db)

    # Register blueprints
    from app.api.routes.auth_routes import auth_bp
    from app.api.routes.dashboard_routes import dashboard_bp
    from app.api.routes.add_job_routes import add_job_bp
    from app.api.routes.jobs_list_routes import jobs_list_bp
    from app.api.routes.matching_routes import matching_bp
    from app.api.routes.monitoring_routes import monitoring_bp
    from app.api.routes.resume_routes import resume_list_bp
    # from app.api.routes.nav_bar import navbar_bp
    from app.api.routes.temp import temp_bp
    from app.api.routes.job_confirmation import job_confirmation_bp
    from app.api.routes.nav import nav_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(add_job_bp)
    app.register_blueprint(jobs_list_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(monitoring_bp)
    app.register_blueprint(resume_list_bp)
    # app.register_blueprint(navbar_bp)
    app.register_blueprint(temp_bp)
    app.register_blueprint(job_confirmation_bp)
    app.register_blueprint(nav_bp)

    # Assign db and oauth to app
    app.db = db
    app.oauth = oauth

    return app