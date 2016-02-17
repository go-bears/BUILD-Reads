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

today = datetime.now()

# date stamp for db session
date_stamp = today.date()

# date formatted for user display
today_date = "%s/%s/%s" % (today.month, today.day, today.year)


#TESTED and WORKS!!

#server the landing page. Currently page is used as summary page 
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


    p_msg = "we are the users", user_list, \
          "we are the books", book_list,\
          "We are the sessions", session_list,\
          "We are the sidekicks", sidekicks_list,\
          "We are ratings_list", ratings_list,\
          "we are badges list", badges, "\n"

    return render_template("index.html", msg=p_msg, today_date=today_date)


#TESTED and WORKS!!
@app.route("/new_user")
def serve_new_user_form():
    """Displays user new user form."""
    
    # values for dropdown menu
    sites = db.session.query(Site).all()
    grades = ['k', 1,2,3,4,5,6,7,8]
    msg = "I'm serving the form"

    return render_template("new_user.html", 
                           sites=sites,
                           grades=grades,
                           msg=msg,
                           today_date=today_date)
    

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
    str_birthday = request.form.get('birthday')
    print "this string", str_birthday
    
    year, month, day = str_birthday.split('-')
    print 'this is the split string,', year, month, day
    # converting string into datetime object for db
    birthday = date(int(year), int(month), int(day))
    print "this is the birthday date obj", birthday
    
    
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
            
            
    return render_template("new_user.html", 
                           sites=sites,
                           grades=grades,
                           msg=msg,
                           today_date=today_date)


# Serves the reading log form 
@app.route('/reading_session')
def serve_reading_session_form():
    """Serves the reading session log. """

    # Flask session data for reader's name
    user = session['first_name']

    # queries db for list of sidekicks for dropdown menu
    # TODO limit dropdown mentors to mentors currently assigned to the site.
    sidekicks = db.session.query(Sidekick).all()
    
    # information messages    
    msg = "i'm serving the reading session page"
    flash("Tell us about your reading adventure %s !" % user)

    return render_template("reading_session.html", 
                           msg=msg, 
                           sidekicks=sidekicks, 
                           today_date=today_date)



# Collects the form information 
@app.route('/log_reading_session', methods=["POST"])
def log_reading_session():
    """Collects reading session data and logs reading session to db."""

    # reader's name from Flask session
    user = session['first_name']
    
    # queries db for list of sidekicks for dropdown menu
    # TODO limit dropdown mentors to mentors currently assigned to the site.
    sidekicks = db.session.query(Sidekick).all()

    # TODO get for the data from the form fields
    title = request.form.get('title')
    print title
    sidekick_lastname = request.form.get('sidekick')
    print sidekick_lastname
    rating_score = request.form.get('rating_score')
    print rating_score
    comments = request.form.get('comment')
    print comments
    time_length = request.form.get('time_length')
    print time_length

    # queries db for user information by first name. this is ok for now.
    #TODO make query smarter by searching by first and last name or get query from data in Flask Session
    user_data = db.session.query(User).filter((User.first_name==user)).first()
    book_data = db.session.query(Book).filter(Book.title==title).first()
    
    # queries db by sidekick's last name
    sidekick_data = db.session.query(Sidekick).filter(Sidekick.last_name==sidekick_lastname).first()
    
    # sets function generates new reading session id number
    new_session_id = set_val_reading_session_id()
    
    # creates new reading session instance
    new_reading_session = Reading_session(session_id=new_session_id,
                                          date=date_stamp,
                                          time_length=time_length,
                                          # TODO write this function that calculates badges on basis of time length 1 badge for 20min 2 for 40 min3 for 60min
                                          badges_awarded=1,
                                          rating_score=rating_score,
                                          user_id=user_data.user_id,
                                          book_id=book_data.book_id,    
                                          sidekick_id=sidekick_data.sidekick_id)
    
    # commits new reaading session instance to db
    new_reading_session.commit_to_db()
    
    # user confirmation
    flash("Great Work! I logged your reading session %s !" % user)
    msg = "I recorded the reading log information"
    return render_template("reading_session.html", msg=msg, sidekicks=sidekicks, today_date=today_date)


# Serves the mentor sign-up form
@app.route('/new_mentor')
def serve_new_mentor_form():
    """Displays user new user form."""
    
    # values for dropdown menu
    sites = db.session.query(Site).all()
    
    msg = "I'm serving the new mentor form"
   
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
     
        # creates instance of Sidekick for db     
        new_sidekick = Sidekick(sidekick_id=new_sidekick_id,
                        first_name=first_name, 
                        last_name=last_name,
                        password=password)
                        
        # commits new sidekick/mentor to db 
        new_sidekick.commit_to_db()
        
        # flashes db confirmation message to user
        flash("Hi %s! We added you to BUILD reads!" % first_name)
        
        # confirmation message in terminal
        print "I commited ", new_sidekick, "to the database"
        
        msg = new_sidekick, "was added to the database"
    
        
    return render_template("new_mentor.html", 
                           sites=sites, 
                           msg=msg,
                           today_date=today_date)


if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    connect_to_db(app)
    
    # app config for local machine
    # app.run(debug=True)

    

    # app config for Cloud9
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
