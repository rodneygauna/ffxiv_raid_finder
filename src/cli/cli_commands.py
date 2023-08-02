"""
CLI Commands for the app
"""


# Imports
import random
from faker import Faker
from flask import Blueprint
from werkzeug.security import generate_password_hash
from src import db
from src.models import (
    User,
    Character,
    UserCharacter,
    Job,
    CharacterJob,
)


# Faker instance
faker = Faker()


# Blueprint initialization
commands_bp = Blueprint("commands", __name__)


# Flask CLI Commands
@commands_bp.cli.command("db_create")
def db_create():
    """Creates the database using SQLAlchemy"""
    db.create_all()
    print("Database created!")


@commands_bp.cli.command("db_drop")
def db_drop():
    """Drops the database using SQLAlchemy"""
    db.drop_all()
    print("Database dropped!")


@commands_bp.cli.command("db_seed")
def db_seed():
    """Seeds the database"""

    # Variable for the maximum range
    max_range = 10+1
    # Data to seed the database with
    data = []

    # Create 10 users
    for i in range(1, max_range):
        data.append(
            User(
                email=faker.email(),
                password_hash=generate_password_hash("password"),
                username=faker.user_name(),
            )
        )

    # Create 10 characters
    for i in range(1, max_range):
        data.append(
            Character(
                name=faker.name(),
                race=random.choice(
                    ["Hyur", "Elezen", "Lalafell", "Miqo'te", "Roegadyn",
                     "Au Ra", "Viera", "Hrothgar"]
                    ),
            )
        )

    # Create 10 jobs
    for i in range(1, max_range):
        data.append(
            Job(
                job=random.choice(
                    ["Paladin", "Warrior", "Dark Knight", "Warrior",
                     "Monk", "Dragoon", "Ninja", "Samurai", "Reaper",
                     "Bard", "Machinist", "Dancer",
                     "Black Mage", "Summoner", "Red Mage", "Blue Mage"]
                ),
                level=random.randint(1, 90),
                description=faker.paragraph(nb_sentences=3),
            )
        )

    # Link the users to the characters
    for i in range(1, max_range):
        data.append(
            UserCharacter(
                user_id=random.randint(1, max_range-1),
                character_id=random.randint(1, max_range-1),
            )
        )

    # Link the characters to the jobs
    for i in range(1, max_range):
        data.append(
            CharacterJob(
                character_id=random.randint(1, max_range-1),
                job_id=random.randint(1, max_range-1),
            )
        )

    # Add the data to the database
    for entry in data:
        db.session.add(entry)
    db.session.commit()
    print("Database seeded!")
