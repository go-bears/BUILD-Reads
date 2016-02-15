# import statment for running on cloud 9
import os 

from datetime import date
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


@app.route("/new_user")
def new_user_form():
    """Displays user login form."""
    
    sites = db.session.query(Site).all()
    grades = ['k', 1,2,3,4,5,6,7,8]
    msg = "i'm displaying the form"
  
  
    return render_template("new_reader.html", sites=sites, grades=grades, msg=msg)


@app.route('/register_new_user', methods=["POST"])
def register_new_user():
    """ User registration: saves new user's first_name, last_name, birthday, school"""
    msg = "i am registering new users"
    sites = db.session.query(Site).all()
    grades =  ['k', 1,2,3,4,5,6,7,8]
    
   # collecting new user data from new_reader.html
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    # splitting string returned in birthday
    year, month, day = request.form.get('birthday').split('-')
    # converting string into datetime object for db
    birthday =date(int(year), int(month), int(day))
    
    school = request.form.get('school')
    grade = request.form.get('grade')
    password = request.form.get('password')
    
    if db.session.query(User).filter((User.first_name==first_name) &
                                     (User.last_name==last_name) &
                                     (User.birthday==birthday)).first():
        print "Database queried!"
        session['first_name'] = first_name
        flash("You're a BUILD reader! We logged you in!", first_name)
        print "did you want to update your settings? or start a reading session?"
        
    
    else:
        site = Site.query.filter(Site.name==school).first()
        site_id = site.site_id
        
            
        new_user = User(first_name=first_name, 
                        last_name=last_name,
                        birthday=birthday,
                        grade=grade,
                        password=password,
                        site_id=site_id)

        new_user.commit_to_db()
        
        session['first_name'] = first_name
        flash("Hi! We added you the database", first_name)

        print "I commited ", new_user, "to the database"
        
        
    return render_template("new_reader.html", sites=sites, msg=msg, grades=grades)


if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    connect_to_db(app)
    # app.run(debug=True)

    # app config for Cloud9
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
