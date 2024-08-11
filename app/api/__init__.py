from flask import Flask
from config import Config
from authlib.integrations.flask_client import OAuth
from app.db.mongo_connection import MongoDB

oauth = OAuth()


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

    db = MongoDB(uri='mongodb://localhost:27017/', db_name='my_resume')

    from app.api.routes.auth_routes import auth_bp
    from app.api.routes.dashboard_routes import dashboard_bp
    from app.api.routes.add_job_routes import add_job_bp
    from app.api.routes.matching_routes import matching_bp
    from app.api.routes.resume_routes import resume_list_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(add_job_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(resume_list_bp)

    app.db = db
    app.oauth = oauth

    return app
