import os

from flask import Flask, render_template, flash, request, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Recipe
from forms import LoginForm, SignUpForm
import requests

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

#######################################################################################
@app.route('/sign-up', methods=["GET", "POST"])
def signup():
    """ sign up form to create new user and add user to DB"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already exists!!")
            return render_template('/signup.html', form=form)
        
        do_login(user)
        return redirect("/")
    
    else:
        return render_template('login.html', form=form)

@app.route('/login', methods=["GET",  "POST"])
def login():
    """ user log in page"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        flash("You have logged in successfully!")

        if user:
            do_login(user)
            return redirect('/')
    
    return render_template("login.html", form=form)

###########################################################################################################
# serializing 

def recipe_serialize(Recipe):
    """ serializing a recipe SQLALchemy obt to dict """

    return {
        "title": Recipe.title,
        "image": Recipe.image,
    }


##############################################################################################################
# Homepage and Search Route

@app.route('/')
def homepage():
    """ Shows homepage """

    return render_template('home.html')

@app.route('/search', methods=["GET", "POST"])
def search():
    """search route"""
    """ API request"""

    if request.method == 'POST':
        search = request.form["search"]
        print(search)
        res = requests.get('https://api.spoonacular.com/recipes/complexSearch',
                       params={"apiKey": API_SECRET_KEY, "query": search})
    
        recipe_data = res.json()
        print(recipe_data)

        return render_template('recipe.html', recipe=recipe_data, searches=search)
    else: 
        return render_template('recipe.html', recipe=[])

