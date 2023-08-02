"""
Database models for the application.
"""

# Imports
from datetime import datetime
from flask import redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from src import db, login_manager


# Login Manager - User Loader
@login_manager.user_loader
def load_user(user_id):
    """Loads the user from the database"""
    return User.query.get(int(user_id))


# Login Manager - Unauthorized Handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirects unauthorized users to the login page"""
    return redirect(url_for("users.login"))


# Model - User
class User(db.Model, UserMixin):
    """User model"""

    __tablename__ = "users"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    # Login Information
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Status
    status = db.Column(db.String(10), default="ACTIVE")
    # Profile Picture
    profile_image = db.Column(
        db.String(255), nullable=False, default="default_profile.png"
    )
    # Username
    username = db.Column(db.String(255), nullable=False, unique=True)

    def check_password(self, password):
        """Checks if the password is correct"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User email: {self.email}"


# Model - Characters
class Character(db.Model):
    """User character model"""

    __tablename__ = "characters"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Status
    status = db.Column(db.String(10), default="ACTIVE")
    # Character Information
    name = db.Column(db.String(255), nullable=False)
    race = db.Column(db.String(255), nullable=False)
    profile_url = db.Column(db.Text)

    def __repr__(self):
        return f"Character name: {self.name}"


# Model - User Characters
class UserCharacter(db.Model):
    """User and Character relationship model"""

    __tablename__ = "user_characters"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))

    def __repr__(self):
        return f"User ID: {self.user_id} - Character ID: {self.character_id}"


# Model - Jobs
class Job(db.Model):
    """User character job model"""

    __tablename__ = "jobs"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Status
    status = db.Column(db.String(10), default="ACTIVE")
    # Job Information
    job = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"Job name: {self.job}"


# Model - User Character Jobs
class CharacterJob(db.Model):
    """Character and Job relationship model"""

    __tablename__ = "character_jobs"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))

    def __repr__(self):
        return f"Character ID: {self.character_id} - Job ID: {self.job_id}"
