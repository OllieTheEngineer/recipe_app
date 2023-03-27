import os

from flask import Flask, render_template, flash, request, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Recipe, Ingredients, Category
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

API_SECRET_KEY = "d4bdce467cf94b428dbcfbbc2b656fc1"


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

    session[CURR_USER_KEY] = user.username


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
            db.session.add(user)
            db.session.commit()

        except IntegrityError as e:
            flash("Username already exists!!")
            return render_template('/signup.html', form=form)
        
        # do_login(user)
        return redirect("/login")
    
    else:
        return render_template('signup.html', form=form)

@app.route('/login', methods=["GET",  "POST"])
def login():
    """ user log in page"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        flash("You have logged in successfully!")

        if user:
            do_login(user)
            return redirect('/search')
        else:
            print("Couldnt't find user")
    else:
        print("Could not validate form")
        print(form.username.data, form.password.data)
    
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    """Logout user."""

    do_logout()
    flash("You have been logged out successfully!")
    return redirect('/')

###########################################################################################################

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
                       params={"apiKey": API_SECRET_KEY, 
                               "query": search, 
                               "instructionsRequired": True, 
                               "addRecipeInformation": True
                               }
                            )
    
        recipe_data = res.json()
        results = recipe_data["results"]
        for recipes in results:
            print(recipes["title"])
            print(recipes["analyzedInstructions"])
            print(recipes["summary"])
            print()

        return render_template('recipe.html', recipe=recipe_data, searches=search, results=results )
    else: 
        return render_template('recipe.html', recipe=[])

@app.route('/recipes/<int:recipe_id>', methods=["GET"])
def recipeInfo(recipe_id):
    """recipe route"""
    """ API request"""
    res = requests.get(f'https://api.spoonacular.com/recipes/{recipe_id}/information',
                       params={"apiKey": API_SECRET_KEY,  
                               "includeNutrition": True
                               }
                            )
    
    recipe_data = res.json()
    print(recipe_data)
    return render_template('recipe_data.html', recipe=recipe_data)


    

@app.route('/sandbox', methods=["GET"])
def sandbox():

    response = {}

    users = User.query.all()
    user_list = [{'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name} for user in users]
    print ("User")
    print (user_list)
    print()
    response["user"] = user_list

    categories = Category.query.all()
    category_list = [{'category': category.name} for category in categories]
    print ("Category")
    print (category_list)
    print()
    response["category"] = category_list

    recipes = Recipe.query.all()
    recipe_list = [{'recipe_name': recipe.recipe_name, 'ingredient': recipe.ingredient, 'instruction': recipe.ingredient, 'category': recipe.category, 'image_url': recipe.image_url, 'username': recipe.user_username, 'category_id': recipe.category_id} for recipe in recipes]
    print ("Recipe")
    print (recipe_list)
    print()
    response["recipe"] = recipe_list

    ingredients = Ingredients.query.all()
    ingredient_list = [{'name': ingredient.name, 'description': ingredient.description, 'recipe_id': ingredient.recipe_id} for ingredient in ingredients]
    print("Ingredients")
    print (ingredient_list)
    print()

    response["ingredient"] = ingredient_list

    return "Look in the terminal"

