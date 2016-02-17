# import statment for running on cloud 9
import os 

from datetime import date, datetime
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

# date objects for display and for database
# date stamp for db session
today = datetime.now()

# date formatted for user display
today_date = "%s/%s/%s" % (today.month, today.day, today.year) 


# Serves the mentor sign-up form
@app.route('/new_mentor')
def serve_new_mentor_form():
    """Displays user new user form."""
    
    # values for dropdown menu
    sites = db.session.query(Site).all()
    
    msg = "I'm serving the new mentor form"
    today_date = "2/17/16"
    return render_template("new_mentor.html", 
                           sites=sites,
                           msg=msg,
                           today_date=today_date)


# Collects the new mentor form information 
@app.route('/register_new_mentor', methods=["POST"])
def register_new_mentor():
        # values for dropdown menu
    sites = db.session.query(Site).all()
    # values fro the form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    birthday = request.form.get("birthday")
    password = request.form.get("password")
    
    
    # future feature add school site to model.py for sidekicks
    # queries db for site_id based on school name
    school = request.form.get('school')
    site = Site.query.filter(Site.name==school).first()
    site_id = site.site_id
    
    today_date = "2/17/16"
    
    
    # checks if mentor is already in db
    if db.session.query(Sidekick).filter((Sidekick.first_name==first_name) &
                                         (Sidekick.last_name==last_name) &
                                         (Sidekick.password==password)).first():
    
        sidekick = db.session.query(Sidekick).filter((Sidekick.first_name==first_name) &
                                         (Sidekick.last_name==last_name) &
                                         (Sidekick.password==password)).first()
    
        print "Database queried!"
        print sidekick

        # confirmation message for user
        flash("You're already a BUILD Mentor %s!" % first_name)
        msg ="database was queried successfully!"
            
        # registers new user to db
    else:
        # sets id for new user entry
        new_sidekick_id = set_val_sidekick_id()
     
        # creates instance of User for db     
        new_sidekick = Sidekick(sidekick_id=new_sidekick_id,
                        first_name=first_name, 
                        last_name=last_name,
                        password=password)

        new_sidekick.commit_to_db()
        
        # flashes db confirmation message to user
        flash("Hi %s! We added you to BUILD reads!" % first_name)
        
        # confirmation message in terminal
        print "I commited ", new_sidekick, "to the database"
        
        msg= new_sidekick, "was added to the database"
    
        
    return render_template("new_mentor.html", 
                           sites=sites, 
                           msg=msg,
                           today_date=today_date)

if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    connect_to_db(app)
    # app.run(debug=True)

    # app config for Cloud9
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
