from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db, oauth


auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates', url_prefix='/auth')


@auth_bp.route('/', methods=['GET'])
def auth_home():
    return redirect(url_for('auth_bp.register'))


@auth_bp.route('/google_login')
def google_login():
    redirect_uri = url_for('auth_bp.google_callback', _external=True)
    print(f"Redirect URI: {redirect_uri}")  # Debugging line to ensure correct URI
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route('/google_callback')
def google_callback():
    print("---google callback function---")
    token = oauth.google.authorize_access_token()
    session['oauth_token'] = token  # Save the token to the session
    resp = oauth.google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    user_model = db['organization']
    user = user_model.get_organization_by_email(user_info['email'])
    print("---user---", user)
    if not user:
        user_id = user_model.add_organization(email=user_info['email'], name=user_info['name'])
        user = {
            "_id": user_id,
            "email": user_info['email'],
            "name": user_info['name']
        }
    else:
        user_id = user['_id']
    if user:
        session['user_id'] = str(user_id)
        session['user_name'] = user_info['name']
        session['user_email'] = user_info['email']
        session['user_picture'] = user_info.get('picture')
    return redirect(url_for('dashboard_bp.dashboard'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user_model = db['organization']
        if not user_model.is_valid_email(email):
            return """
                <script>
                    alert('Invalid email address');
                    window.location.href = '/auth/register';
                </script>
            """
        existing_user = user_model.get_organization_by_email(email)
        if existing_user:
            return """
                <script>
                    alert('User already exists');
                    window.location.href = '/auth/register';
                </script>
            """
        user_model.add_organization(username=username, email=email, password=password)
        return redirect(url_for('auth_bp.login'))
    return render_template('auth.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user_model = db['organization']
        user = user_model.get_organization_by_email(email)
        if user and user.verify_password(password):
            session['user_email'] = user.email
            session['username'] = user.username
            return redirect(url_for('main_bp.index'))
        return """
                <script>
                    alert('Invalid credentials');
                    window.location.href = '/auth/login';
                </script>
            """
    return render_template('auth.html')


@auth_bp.route('/logout')
def logout():
    token = session.get('oauth_token')
    if token:
        oauth.google.post(
            'https://accounts.google.com/o/oauth2/revoke',
            params={'token': token['access_token']},
            headers={'content-type': 'application/x-www-form-urlencoded'}
        )
    session.clear()
    # Redirect to Google logout URL to ensure account selection screen is shown
    return redirect(
        'https://accounts.google.com/Logout?continue=https://appengine.google.com/_ah/logout?continue=https'
        '://accounts.google.com/ServiceLogin?continue=https://localhost:5000/auth/login')