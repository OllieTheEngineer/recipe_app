""" Models for Recipe App"""


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """user info in system"""

    __tablename__ = 'users'

    username = db.Column(
        db.String(15),
        primary_key=True
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

class Categories(db.Model):
    """ Dietary preferences"""

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    category = db.Column(
        db.String,
        nullable=False,
    )


class Recipe(db.Model):
    """recipes added by user"""

    __tablename__ = 'recipes'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    recipe_name = db.Column(
        db.Text,
        nullable=False,
    )

    ingredient = db.Column(
        db.String(500),
        nullable=False,
    )

    instruction = db.Column(
        db.String(500),
        nullable=False,
    )

    category = db.Column(
        db.String,
        nullable=True,
    )
    
    image_url = db.Column(
        db.Text,
        nullable=True,
    )
    user_username = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship("User", backref=db.backref('recipes', cascade='all.delete'))

    category_id = db.Column(
        db.Integer,
        db.Foreign_key('categories.id'),
        nullable=False,
    )

    category = db.relationship("Category", backref=db.backref('categories'))

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

    description = db.Column(
        db.String(100),
        nullable=False
    )
    
    recipe_id = db.Column(
        db.Integer, 
        db.ForeignKey(
        'recipes.id', ondelete='CASCADE'), 
        nullable=False
    )
    
    recipe = db.relationship('Recipe', backref=db.backref(
        'ingredients', cascade='all,delete'))


def connect_db(app):
    db.app = app
    db.init_app(app)