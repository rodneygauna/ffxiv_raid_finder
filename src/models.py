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


# Model - User Accounts (Discord, YouTube, Twitch)
class UserAccounts(db.Model):
    """User's Steam and Microsoft Accounts"""

    __tablename__ = "user_game_accounts"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Account Information
    discord_account = db.Column(db.Text)
    youtube_account = db.Column(db.Text)
    twitch_account = db.Column(db.Text)
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)


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
    realm = db.Column(db.String(255), nullable=False)


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


# Model - Events
class Events(db.Model):
    """Raid Events"""

    __tablename__ = "events"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    leader_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Event Information
    start_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    start_timezone = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    event_status = db.Column(db.String(30), nullable=False, default="open")
    requirements = db.Column(db.Text)
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)


# Model - Event Members
class EventRoster(db.Model):
    """Event Member Roster"""

    __tablename__ = "event_roster"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    character_job_id = db.Column(
        db.Integer, db.ForeignKey("character_jobs.id"))
    # Event Information
    role = db.Column(db.String(255), nullable=False)
    secondary_role = db.Column(db.String(255))
    comments = db.Column(db.Text)
    # Event Status
    player_status = db.Column(db.String(30), nullable=False, default="pending")
    # Timestamps
    created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
