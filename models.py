""" Models for Recipe App"""


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """user info in system"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
        unique=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
        unique=False,
    )

    password = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )


class Recipe(db.Model):
    """recipes added by user"""

    __tablename__ = 'recipes'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    recipe_title = db.Column(
        db.Text,
        nullable=False,
    )

    recipe_ingredients = db.Column(
        db.String(500),
        nullable=False,
    )

    recipe_instructions = db.Column(
        db.String(500),
        nullable=False,
    )

    recipe_image = db.Column(
        db.Text
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(''),
        nullable=False
    )

    user = db.relationship('User')

class Ingredients(db.Model):
    """ list of ingredients """

    __tablename__ = "ingredients"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(20),
        nullable=False
    )
    ingredient = db.relationship('Ingredients')

    def connect_db(app):

        db.app = app
        db.init_app(app)