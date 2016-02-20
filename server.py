# import statment for running on cloud 9
import os 

from datetime import date, datetime
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined

from model import *

#######################################################################
# Flask variables and tools

app = Flask(__name__)
#db = SQLAlchemy(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined



######################################################################
# Global variables for this app

# Create datetime objects for display and for database
today = datetime.now()

# date stamp for db session
date_stamp = today.date()

# date formatted for user display
today_date = "%s/%s/%s" % (today.month, today.day, today.year)


####### Serving Pages ################################################

#TESTED and WORKS!!

# serving the landing page. Currently page is used as summary page 
# displaying all data in build_reads db
@app.route('/')
def index():
    """Homepage."""

    user_list = User.query.all()
    book_list = Book.query.all()
    session_list = Reading_session.query.all()
    sidekicks_list = Sidekick.query.all()
    ratings_list = Rating.query.all()
    badges = Badge.query.all()


    p_msg = "Everything I know is here:",\
            "we are the users", user_list,\
            "we are the books", book_list,\
            "We are the sessions", session_list,\
            "We are the sidekicks", sidekicks_list,\
            "We are ratings_list", ratings_list,\
            "we are badges list", badges

    return render_template("index.html", msg=p_msg, today_date=today_date)


# TESTED and WORKS!
@app.route('/login')
def serve_login_form():
    """Displays login form"""

    
    return render_template("login.html", today_date=today_date)


# TESTED AND WORKS
# Serves the reading log form 
@app.route('/reading_session')
def serve_reading_session_form():
    """Serves the reading session log. """

    # queries db for list of sidekicks for dropdown menu
    # TODO limit dropdown mentors to mentors currently assigned to the site.
    sidekicks = db.session.query(Sidekick).all()
    
    # information messages    
    msg = "i'm serving the reading session page"
    flash("Tell us about your reading adventure %s !" % session['first_name'])

    return render_template("reading_session.html", 
                           msg=msg, 
                           sidekicks=sidekicks, 
                           today_date=today_date)


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


# TESTED AND WORKS
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


@app.route("/user/")
def serve_user_details_page():
    """Displays template for user's reading history """
    
    msg = "you must be logged in to see your reading history"
    
    return render_template("index.html", 
                           msg=msg,
                           today_date=today_date)


########### Server Logic ###################################                           

# TODO in progress Method not allow error. mentor login should go to mentor dashboard
@app.route('/resolve_login', methods=["POST", "GET"])    
def resolve_login():
    """Manages login logic to direct to /reading_session or /new_user."""
    
    # collects login information from form
    user_type = request.form.get('user_type')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    

    if user_type == "scholar":

        #checks login information against database
        if db.session.query(User).filter((User.first_name==first_name) &
                                         (User.last_name==last_name) &
                                         (User.password==password)).first():
            
            
            scholar = db.session.query(User).filter((User.first_name==first_name) &
                                                    (User.last_name==last_name) &
                                                    (User.password==password)).first()
            
            # save values for Flask session dictionary
            session["logged_in"] = True
            
            session['first_name'] = first_name
            print "this person is logged in,", session['first_name']
            
            session['scholar_id'] = scholar.user_id
            print "this is the user id", session['scholar_id'] 
            
            
            # confirmation message
            flash("Success! You're logged in %s! Let's start reading!" % first_name)
            
            # redirect to new reading session log
            return redirect('/reading_session')
        
        else:
            flash("Looks like you're new to BUILD! Let's sign you up!")
            return redirect('/new_user')
            
    
    if user_type == 'mentor':
        
        # checks loging information against mentor/sidekick table
        if db.session.query(User).filter((User.first_name==first_name) &
                                         (User.last_name==last_name) &
                                         (User.password==password)).first():
                                         
            sidekick = db.session.query(User).filter((Sidekick.first_name==first_name) &
                                                     (Sidekick.last_name==last_name) &
                                                     (Sidekick.password==password)).first()
        # success redirects to mentor dashboard eventually
            
            flash("Let's start reading with your scholar! \
                  Please help them with logging in")
            return redirect('/login')
        
        else:
            flash("Looks like you're new to BUILD! Let's sign you up!")
            return redirect('/new_mentor')
            


#TESTED and WORKS!!
@app.route('/register_new_user', methods=["POST"])
def register_new_user():
    """ User registration: saves new user's 
    first_name, last_name, birthday, school"""
    
    # temporary message for me about page info
    msg = "i am registering new users"
    
    # values for dropdown menu
    sites = db.session.query(Site).all()
    grades =  ['k', 1,2,3,4,5,6,7,8]
    

   # collecting new user data from new_user.html
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    school = request.form.get('school')
    
    grade = request.form.get('grade')
    # convert grade k to integer for db record
    if grade =='k':
        grade = 0
    
    password = request.form.get('password')

    # splitting string returned in birthday
    str_birthday = request.form.get('birthday')
    print "this string", str_birthday
    
    year, month, day = str_birthday.split('-')
    print 'this is the split string,', year, month, day
    # converting string into datetime object for db
    birthday = date(int(year), int(month), int(day))
    print "this is the birthday date obj", birthday
    
    

    
    # values for Flask session dictionary for new user
    session['first_name'] = first_name
    session['school'] = school


    ## Database queries to build_reads db ##
    
    # checks if user is already in db
    if db.session.query(User).filter((User.first_name==first_name) &
                                     (User.last_name==last_name) &
                                     (User.birthday==birthday)).first():

        scholar = db.session.query(User).filter((User.first_name==first_name) &
                                     (User.last_name==last_name) &
                                     (User.birthday==birthday)).first()

        print "Database queried!"
        print scholar
        
        # stores scholar's user.id from db if scholar is already in db
        session['scholar_id'] = scholar.user_id
        print session['scholar_id']
        
        print "the scholar id is for {} is {}".format(scholar, session['scholar_id'])

        # confirmation message for user
        flash("You're already a BUILD scholar! We logged you in %s!" % first_name)
        
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
        
        # stores scholar_id in flask session after db commit
        session['scholar_id'] = new_user.user_id

        
        # flashes db confirmation message to user
        flash("Hi %s! We added you to BUILD reads!" % first_name)
        
        # confirmation message in terminal
        print "I commited ", new_user, "to the database"
            
            
    return render_template("new_user.html", 
                           sites=sites,
                           grades=grades,
                           msg=msg,
                           today_date=today_date)





# TESTED AND WORKS
# Collects the form information 
@app.route('/log_reading_session', methods=["POST"])
def log_reading_session():
    """Collects reading session data and logs reading session to db."""


    # queries db for list of sidekicks for dropdown menu
    # TODO limit dropdown mentors to mentors currently assigned to the site.
    sidekicks = db.session.query(Sidekick).all()

    # collects data from the form fields
    title = request.form.get('title').strip()
    sidekick_lastname = request.form.get('sidekick')
    rating_score = request.form.get('rating_score')
    comment = request.form.get('comment')
    time_length = request.form.get('time_length')
    print time_length, " is how long the reading session was"
        # calculates badges earned per reading session
    if time_length < 20:
        badges = 0
    elif time_length >= 20 or time_length <= 40:
        badges = 1
    elif time_length >= 40 or time_length <= 60:
        badges = 2
    else:
        badges = 3
    

    # queries db for user information by first name. this is ok for now.
    #TODO make query smarter by searching by first and last name or get query from data in Flask Session
    user_data = db.session.query(User).filter(User.first_name==\
                                              session['first_name']).first()
    book_data = db.session.query(Book).filter(Book.title==title).first()
    
    # queries db by sidekick's last name
    sidekick_data = db.session.query(Sidekick).filter(Sidekick.last_name==\
                                                      sidekick_lastname).first()
    
    # sets function generates new reading session id number, use only when seeding db
    # new_session_id = set_val_reading_session_id()
    # badges = None
    
    
    # creates new reading session instance
    new_reading_session = Reading_session(#session_id=new_session_id,
                                          date=date_stamp,
                                          time_length=time_length,
                                          badges_awarded=badges,
                                          rating_score=rating_score,
                                          user_id=user_data.user_id,
                                          book_id=book_data.book_id,    
                                          sidekick_id=sidekick_data.sidekick_id)
    # terminal confirmation
    print new_reading_session

    # commits new reading session instance to db
    new_reading_session.commit_to_db()
    
    msg = "I recorded the reading log information"


    # sets new rating id
    #new_rating_id = set_val_rating_session_id()
    
    # creates new instance of a rating
    new_rating = Rating(#rating_id=new_rating_id,
                        comment=comment,
                        user_id=user_data.user_id,
                        book_id=book_data.book_id,
                        session_id=new_reading_session.session_id)
    
    new_rating.commit_to_db()
    print "i logged new this new_rating",  book_data.book_id, comment#, new_rating_id,                    
        
    # user confirmation
    flash("Great Work! I logged your reading session %s !" % session['first_name'])
    
    
    return render_template("reading_session.html", 
                           msg=msg,
                           sidekicks=sidekicks,
                           today_date=today_date)



# TESTED AND WORKS
# Collects the new mentor form information 
@app.route('/register_new_mentor', methods=["POST"])
def register_new_mentor():
    """Logs new mentors data from form to database """
    
    # draws values from db for dropdown menu
    sites = db.session.query(Site).all()
    
    # collectts values from the form
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
        
        # terminal confirmation messages
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
        
        # confirmation message for user
        msg = new_sidekick, "was added to the database"
    
        
    return render_template("new_mentor.html", 
                           sites=sites, 
                           msg=msg,
                           today_date=today_date)



# TODO in progress: need to limit data to books and ratings_scores
@app.route("/user/<int:scholar_id>")
def show_user_details(scholar_id):
    """Return page showing the details of a scholar's history."""
    
    # queries database for scholar information by id
    scholar_data = User.query.filter(User.user_id == session['scholar_id']).first()
    print "i'm the user", scholar_data
    
    # queries database for all ratings by the scholar by scholar id
    user_ratings_list = Rating.query.filter(Rating.user_id == session['scholar_id']).all()
    
    
    print 'you read these books'
    book_rating_dict = {}
    badges = 0
    total_time = 0
    
    for user_rating in user_ratings_list:
        
        # calculate total badges earned
        if user_rating.session.badges_awarded:
            badges +=1
        
        # calculates tot
        if user_rating.session.time_length:
            total_time += user_rating.session.time_length
        
        # collects individual book ratings
        if user_rating.book.title not in book_rating_dict:
            book_rating_dict[user_rating.book.title] = \
            [user_rating.session.rating_score]
        
        else:
            book_rating_dict[user_rating.book.title].append(user_rating.session.rating_score)
        
    import numpy
    
    
    
    for title, ratings in book_rating_dict.items():
        avg_rating = numpy.mean(ratings)
        book_rating_dict[title] = avg_rating
    
    
    print book_rating_dict
            
        # Nice to have
        #TODO get books titles to show on user page
        #calculate average ratings for a book
        #count earned for badges per day/day/month
        
    
    
    print "badges earned", badges
    msg = 'your earned %s badges!!!' % badges
    
    flash("You worked hard %s !" % session['first_name'])
    
    return render_template("user_details.html",
                           msg=msg,
                           today_date=today_date,
                           user_details=scholar_data,
                           user_ratings_list=user_ratings_list,
                           book_dict=book_rating_dict,
                           time=total_time)


if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    connect_to_db(app)
    # app config for local machine
    # app.run(debug=True)
    
    # flask debugging toolbar
    DebugToolbarExtension(app)
    

    # app config for Cloud9
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
