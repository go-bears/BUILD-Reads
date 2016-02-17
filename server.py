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


#TESTED and WORKS!!

#server the landing page. Currently page is used as summaryy page 
#displaying all data in build_reads db
@app.route('/')
def index():
    """Homepage."""

    user_list = User.query.all()
    book_list = Book.query.all()
    session_list = Reading_session.query.all()
    sidekicks_list = Sidekick.query.all()
    ratings_list = Rating.query.all()
    badges = Badge.query.all()


    msg = "we are the users", user_list, \
          "we are the books", book_list,\
          "We are the sessions", session_list,\
          "We are the sidekicks", sidekicks_list,\
          "We are ratings_list", ratings_list,\
          "we are badges list", badges

    return render_template("index.html", msg=msg)


#TESTED and WORKS!!
@app.route("/new_user")
def serve_new_user_form():
    """Displays user new user form."""
    
    # values for dropdown menu
    sites = db.session.query(Site).all()
    grades = ['k', 1,2,3,4,5,6,7,8]
    msg = "I'm serving the form"

    return render_template("new_reader.html", sites=sites, grades=grades, msg=msg)


#TESTED and WORKS!!
@app.route('/register_new_user', methods=["POST"])
def register_new_user():
    """ User registration: saves new user's first_name, last_name, birthday, school"""
    
    # temporary message for me about page info
    msg = "i am registering new users"
    
    # values for dropdown menu
    sites = db.session.query(Site).all()
    grades =  ['k', 1,2,3,4,5,6,7,8]
    

   # collecting new user data from new_reader.html
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    school = request.form.get('school')
    grade = request.form.get('grade')
    password = request.form.get('password')

    # splitting string returned in birthday
    year, month, day = request.form.get('birthday').split('-')
    # converting string into datetime object for db
    birthday =date(int(year), int(month), int(day))
    
    
    # values for Flask session dictionary
    session['first_name'] = first_name
    session['school'] = school


    #### Database queries to build_reads db ######################################
    
    # checks if user is already in db
    if db.session.query(User).filter((User.first_name==first_name) &
                                     (User.last_name==last_name) &
                                     (User.birthday==birthday)).first():

        reader = db.session.query(User).filter((User.first_name==first_name) &
                                     (User.last_name==last_name) &
                                     (User.birthday==birthday)).first()

        print "Database queried!"
        print reader

        # stores reader's user.id from db
        session['reader_id'] = reader.user_id
        print session['reader_id']
        
        print "the reader id is for {} is {}".format(reader, session['reader_id'])

        # confirmation message for user
        flash("You're already a BUILD reader! We logged you in %s!" % first_name)
        
    # registers new user to db
    else:
        # queries db for site_id based on school name
        site = Site.query.filter(Site.name==school).first()
        site_id = site.site_id

        # sets id for new user entry
        new_user_id = set_val_user_id()
     
        # creates instance of User for db     
        new_user = User(user_id=new_user_id,
                        first_name=first_name, 
                        last_name=last_name,
                        birthday=birthday,
                        grade=grade,
                        password=password,
                        site_id=site_id)

        new_user.commit_to_db()
        
        # flashes db confirmation message to user
        flash("Hi %s! We added you to BUILD reads!" % first_name)
        
        # confirmation message in terminal
        print "I commited ", new_user, "to the database"
        
        
    return render_template("new_reader.html", sites=sites, msg=msg, grades=grades)


# Serves the reading log form 
@app.route('/reading_session')
def serve_reading_session_form():
    """Serves the reading session log. """

    # date to for date stamp for db session
    today = datetime.now()

    #date for user display
    date = "%s/%s/%s" % (today.month, today.day, today.year) 
    
    # Flask session data for reader's name
    user = session['first_name']

    # queries db for list of sidekicks for dropdown menu
    # TODO limit dropdown mentors to mentors currently assigned to the site.
    sidekicks = db.session.query(Sidekick).all()
    
    # information messages    
    msg = "i'm serving the reading session page"
    flash("Tell us about your reading adventure %s !" % user)

    return render_template("reading_session.html", msg=msg, sidekicks=sidekicks, date=date)


if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    connect_to_db(app)
    
    # app config for local machine
    # app.run(debug=True)

    

    # app config for Cloud9
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
