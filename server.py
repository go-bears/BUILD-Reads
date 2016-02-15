# import statment for running on cloud 9
import os 

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined

from model import *

app = Flask(__name__)
#db = SQLAlchemy(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined




@app.route('/')
def index():
    """Homepage."""

    user_list = User.query.all()
    print user_list 
    book_list = Book.query.all()
    print book_list

    session_list = Reading_session.query.all()
    print session_list

    sidekicks_list = Sidekick.query.all()
    print sidekicks_list

    ratings_list = Rating.query.all()
    print ratings_list

    badges = Badge.query.all()
    print badges


    msg = "we are the users", user_list, "we are the books", book_list,\
            "We are the sessions", session_list,\
            "We are the sidekicks", sidekicks_list,\
            "We are ratings_list", ratings_list,\
            "we are badges list", badges

    return render_template("index.html", msg=msg)


@app.route("/new_user")
def new_user_form():
    """Displays user login form."""

    
    return render_template("new_reader.html")


@app.route('/new_user_completion', methods=['POST'])
def new_user_completion():
    """ User registration new user's first_name, last_name, birthday, school"""

    pass



@app.route('/login_completion', methods=["POST"])
def login_completion():
    """Login resolution page, takes in login info, checks db for login or adds user"""

    email = request.form.get('username')
    password =request.form.get('password')

    print email, password

    # successful login    
    if db.session.query(User).filter((User.email==email) & (User.password==password)).first():
        print "Database queried!"
        flash("You are now logged in!")
        session['email'] = email
        return render_template("homepage.html", logged_in=session.get('email', False))

    # email already exists -- incorrect password
    elif db.session.query(User).filter(User.email==email).first():
        flash("The password does not match the user email. Try Again!")
        return render_template('login_form.html', logged_in=session.get('email', False)) 

    # not email in db -- new user add
    elif not db.session.query(User).filter((User.email==email) & (User.password==password)).first():
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['email'] = email
        flash("Hi! We added you the database")

        print "I commited ", new_user, "to the database"
        return render_template("homepage.html", logged_in=session.get('email', False))





if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    connect_to_db(app)
    # app.run(debug=True)

    

    # app config for Cloud9
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
