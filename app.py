import os

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import json

from scraper.scrape_reviews import start_scraping
from model.predict import prediction
from database.user_db import connect_to_db, User


app = Flask(__name__)

app.secret_key = "ProductAnalysis"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def display_homepage():

    return render_template("homepage.html")


@app.route('/register', methods=["GET"])
def display_registration():
    """Display register form"""

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def process_registration():
    """Process a new user's' registration form"""

    # Grab inputs from registration form
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter_by(email=email).count() != 0:
        message = "That email already exists. Please login or register for a new account"
    else:
        User.register_user(name, email, password)
        message = "Welcome to Product Analyzer"

    flash(message)

    return redirect("/login")


@app.route('/login', methods=["GET"])
def display_login():
    """Display login form"""

    return render_template('login_form.html')


@app.route('/login', methods=["POST"])
def log_in():
    """Log user in"""

    email = request.form.get('email')
    password = request.form.get('password')

    # Fetch user from db
    user_query = User.query.filter_by(email=email)

    # Check if user exists
    if user_query.count() == 0:
        flash("No account exists for that email")
        return redirect("/")

    user = user_query.one()

    # Check if password is correct
    if user.password == password:

        # Add user to session cookie
        session['user'] = {"id": user.user_id,
                           "name": user.name}

        flash("Logged in as {}".format(user.name))
        return redirect("/")

    else:
        flash("Incorrect password")
        return redirect("/login")


@app.route('/logout')
def log_out():
    """Log user out"""

    # Remove user from session
    del session['user']

    return redirect("/")



@app.route('/search')
def search_products():

    search_query = request.args.get('query')

    print("---------- Started Scraping Reviews ----------")
    product = search_query.split('/')[3]
    reviews, ratings = start_scraping(search_query, 300)

    print("---------- Analysing Reviews ----------")

    sentiments_list, score_list, words = prediction(reviews)

    score = sum(score_list)/len(score_list)

    json_data = {
        "reviews": reviews,
        "sentiments_list": sentiments_list,
        "score_list": score_list,
        "words": words,
        "numpos": sentiments_list.count('Positive'),
        "numneg": sentiments_list.count('Negative'),
        "toppos": reviews[score_list.index(max(score_list))],
        "topneg": reviews[score_list.index(min(score_list))]
    }

    with open('output.json', 'w+') as f:
        json.dump(json_data, f)

    print(json_data)

    return render_template("product_details.html",
                           product=product,
                           Score =score,
                           words=words,
                           toppos=json_data["toppos"],
                           topneg=json_data["topneg"])


@app.route('/product-bar-data')
def product_reviews_data():
    """Return data about product reviews for histogram."""

    f = open('output.json')
    data = json.load(f)

    numpos = data['numpos']
    numneg = data['numneg']

    print(numpos,numneg)

    return jsonify(data)


if __name__ == "__main__":
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.run(port=5000, host='0.0.0.0', debug=True)
