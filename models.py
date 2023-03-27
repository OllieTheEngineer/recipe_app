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

    @classmethod
    def signup(cls, username, first_name, last_name, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False;

class Category(db.Model):
    """ Dietary preferences"""

    __tablename__ = 'categories'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
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

    # category = db.Column(
    #     db.String,
    #     nullable=True,
    # )
    
    image_url = db.Column(
        db.Text,
        nullable=True,
    )
    user_username = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship("User", backref=db.backref('recipes', cascade='all,delete'))

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable=False,
    )

    category = db.relationship("Category", backref=db.backref('categories'))

class Ingredients(db.Model):
    """ list of ingredients """

    __tablename__ = 'ingredients'

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