import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///recipes_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

API_SECRET_KEY = "ec5b8151d1ca4723963202741272cba1"


connect_db(app)

##########################################################################################################
# user sign up/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


##############################################################################################################
# API Request

# resp = request.get('https://api.spoonacular.com/recipes/complexSearch?apiKey=ec5b8151d1ca4723963202741272cba1')

@app.route('/')
def homepage():
    """ Shows homepage """

    return render_template('home.html')

@app.route('/search', methods=["GET"])
def search():
    """search route"""
    recipes = request.args["recipes"]
    res = request.get('https://api.spoonacular.com/recipes/complexSearch',
                       params={"recipes": recipes, "key": API_SECRET_KEY})
    
    recipe_data = res.json

    return render_template('recipe.html', recipe=recipe_data)

# recipe page route