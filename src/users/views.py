"""
Users > Views
"""

# Imports
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from werkzeug.security import generate_password_hash
from flask_login import (
    login_user,
    login_required,
    logout_user,
)
from src.users.forms import (
    RegisterUserForm,
    LoginForm,
)
from src import db
from src.models import (
    User,
)


# Blueprint Configuration
users_bp = Blueprint('users', __name__)


# Register User
@users_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    """Registers a new user"""

    form = RegisterUserForm()

    if form.validate_on_submit():
        # Check if email is already registered
        if User.query.filter_by(email=form.email.data).first():
            flash('This email is already registered.', 'danger')
            return redirect(url_for('users.register_user'))

        # Check if username is already registered
        if User.query.filter_by(username=form.username.data).first():
            flash('This username is already in use.', 'danger')
            return redirect(url_for('users.register_user'))

        # Commit the new user to the database
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html',
                           title='FFXIV Raid Finder - Register',
                           form=form)


# Login user
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Logs in a user"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)

            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('core.index')

            flash('Login successful.', 'success')
            return redirect(next)
        flash('Invalid email or password.', 'error')

    return render_template('users/login.html',
                           title='FFXIV Raid FInder - Login',
                           form=form)


# Logout user
@users_bp.route('/logout')
@login_required
def logout():
    '''Logs out a user'''

    logout_user()
    return redirect(url_for('core.index'))
