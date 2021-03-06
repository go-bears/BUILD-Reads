# import statment for running on cloud 9
import os
import numpy
import pprint

from datetime import date, datetime
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined


from model import *


from  server_helper_funct import pick_avatar, calculate_badges,\
                                 birthday_format,\
                                 calculates_total_badges,\
                                 calculates_total_reading_time,\
                                 tally_book_ratings, format_chart_colors,\
                                 display_book_data, display_badges,format_site_chart,\
                                 reading_confidence

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


####### DB Queries ################################################

#TESTED and WORKS!!

# serving the landing page. Currently page is used as summary page 
# displaying all data in build_reads db
def query_all_users():
    """db query to pull all users """
    
    user_list = User.query.all()

    return user_list

def query_all_books():
    """db query to pull all books"""
    
    book_list = Book.query.all()

    return book_list

def query_all_sites():
    """db query to pull all badges data """
    
    sites_list = Site.query.all()

    return sites_list


def query_all_reading_sessions():
    """db query to pull all reading sesssion data"""
    
    session_list = Reading_session.query.all()

    return session_list

def query_all_sidekick():
    """db query to pull all sidekicks data"""
    
    sidekicks_list = Sidekick.query.all()

    return sidekicks_list

def query_all_ratings():
    """db query to pull all ratings data"""
    
    ratings_list = Rating.query.all()

    return ratings_list

def query_all_badges():
    """db query to pull all badges data """
    
    badges_list = Badge.query.all()

    return badges_list



####### Serving Pages ################################################


@app.route('/')
def index():
    """Homepage."""

    p_msg = "Everything I know is here:",\
            "we are the users", user_list,\
            "we are the books", book_list,\
            "We are the sessions", session_list,\
            "We are the sidekicks", sidekicks_list,\
            "We are ratings_list", ratings_list,\
            "we are badges list", badges_list

    return render_template("index.html", msg=p_msg, today_date=today_date)


# TESTED and WORKS!
@app.route('/login')
def serve_login_form():
    """Displays login form"""
    

    return render_template("login.html", today_date=today_date)


@app.route('/logout')
def serve_logout_button():
    """Clears sessioin and returns user to login form"""
    
    session.clear()
    flash("You successfuly logged out!")
    
    return redirect('/login')

# TESTED AND WORKS
@app.route('/reading_session', methods=["POST", "GET"])
def serve_reading_session_form():
    """Serves the reading session log. """

    # queries db for list of sidekicks for dropdown menu
    # TODO limit dropdown mentors to mentors currently assigned to the site.
    sidekicks = sidekicks_list
    # queries databse for scholar ID for go to 
    scholar = User.query.filter(User.first_name == session['first_name']).first()
    
    sites = scholar.site.name
    
    # information messages    
    msg = "Tell us about your reading adventure %s !" % session['first_name']
    
    return render_template("reading_session.html", 
                           msg=msg, 
                           sidekicks=sidekicks, 
                           user_id=scholar.user_id,
                           today_date=today_date,
                           avatar=scholar.avatar,
                           sites=sites)


#TESTED and WORKS!!
@app.route("/new_user")
def serve_new_user_form():
    """Displays user new user form."""
    
    # values for dropdown menu
    sites = [site.name for site in sites_list]
    
    # db.session.query(Site).all()
    grades = ['k', 1,2,3,4,5,6,7,8]
    
    return render_template("new_user.html", 
                           sites=sites,
                           grades=grades,
                           today_date=today_date)


# TESTED AND WORKS
# Serves the mentor sign-up form
@app.route('/new_mentor')
def serve_new_mentor_form():
    """Displays user new user form."""
    
    # values for dropdown menu
    sites = [site.name for site in sites_list]
    
    
    return render_template("new_mentor.html", 
                           sites=sites,
                           today_date=today_date)


@app.route("/user")
def serve_user_details_page():
    """Displays template for user's reading history """
    
    msg = "you must be logged in to see your reading history"
    
    return render_template("index.html", 
                           msg=msg,
                           today_date=today_date)


########### Server Logic ###################################                           

# TODO in progress Method not allow error. mentor login should go to mentor dashboard
@app.route('/resolve_login', methods=["POST"])    
def resolve_login():
    """Manages login logic to direct to /reading_session or /new_user."""
    
    # collects login information from form
    user_type = request.form.get('user_type')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    

    
    if user_type == "scholar":

        #checks scholar's login information against user database
        if db.session.query(User).filter((User.first_name==first_name) &
                                         (User.last_name==last_name) &
                                         (User.password==password)).first():
            
            # queries db for scholar object
            scholar = db.session.query(User).filter((User.first_name==first_name) &
                                                    (User.last_name==last_name) &
                                                    (User.password==password)).first()
            
            # save values for Flask session dictionary
            session["logged_in"] = True
            
            session['first_name'] = first_name
            print "this person is logged in,", session['first_name']
            
            session['scholar_id'] = scholar.user_id
            print "this is the user id", session['scholar_id'] 
            
            session['avatar'] = scholar.avatar
            
            
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
            
            session['mentor'] = sidekick.sidekick_id
        

        return redirect('/mentor_detail')
          


#TESTED and WORKS!!
@app.route('/register_new_user', methods=["POST", "GET"])
def register_new_user():
    """ User registration: saves new user's 
    first_name, last_name, birthday, school"""
    
    # temporary message for me about page info
    msg = "i am registering new users"
    
    # values for dropdown menu
    sites = [site.name for site in sites_list]
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
    
    avatar = pick_avatar()
    session['scholar_id'] = avatar
    
    # splitting string returned in birthday
    str_birthday = request.form.get('birthday')
    birthday = birthday_format(str_birthday)

    
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
        
        # stores scholar's user.id from db if scholar is already in db
        session['scholar_id'] = scholar.user_id
        
        
        print "the scholar id is for {} is {}".format(scholar, session['scholar_id'])

        # confirmation message for user
        flash("You're already a BUILD scholar! We logged you in %s!" % first_name)
        
    # registers new user to db
    else:
        # queries db for site_id based on school name
        site = Site.query.filter(Site.name==school).first()
        site_id = site.site_id

        # sets id for new user entry
        # new_user_id = set_val_user_id()
    
 
        # creates instance of User for db     
        new_user = User(#user_id=new_user_id,
                        first_name=first_name, 
                        last_name=last_name,
                        birthday=birthday,
                        grade=grade,
                        password=password,
                        avatar=avatar,
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
        
        # queries for sidekick information
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


# TESTED AND WORKS
# Collects the form information 
@app.route('/log_reading_session', methods=["POST"])
def log_reading_session():
    """Collects reading session data and logs reading session to db."""


    # queries db for list of sidekicks for dropdown menu
    # TODO limit dropdown mentors to mentors currently assigned to the site.
    sidekicks = sidekicks_list

    # collects data from the form fields
    title = request.form.get('title').strip()
    sidekick_lastname = request.form.get('sidekick')
    rating_score = request.form.get('rating_score')
    comment = request.form.get('comment')
    time_length = int(request.form.get('time_length'))
    
    print time_length, " is how long the reading session was"
    
    # calculates badges earned per reading session
    badge_id = calculate_badges(time_length)
    print badge_id
    
    session['session_badge'] = badge_id
    session['time'] = time_length


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
   
    # creates new reading session instance
    new_reading_session = Reading_session(#session_id=new_session_id,
                                          date=date_stamp,
                                          time_length=time_length,
                                          badges_awarded=badge_id,
                                          rating_score=rating_score,
                                          user_id=user_data.user_id,
                                          isbn=book_data.isbn,    
                                          sidekick_id=sidekick_data.sidekick_id)
    # terminal confirmation
    print new_reading_session

    # commits new reading session instance to db
    new_reading_session.commit_to_db()
    
    msg = "I recorded the reading log information"


    # sets new rating id
    # new_rating_id = set_val_rating_session_id()
    
    # creates new instance of a rating
    new_rating = Rating(#rating_id=new_rating_id,
                        comment=comment,
                        user_id=user_data.user_id,
                        isbn=book_data.isbn,
                        session_id=new_reading_session.session_id)
    
    new_rating.commit_to_db()
    
    print "i logged new this new_rating",  book_data.isbn, comment#, new_rating_id,                    
        
    # user confirmation
    flash("Great Work! I logged your reading session %s !" % session['first_name'])
    
    
    return render_template("reading_session.html", 
                           msg=msg,
                           avatar=user_data.avatar,
                           sidekicks=sidekicks,
                           user_id=user_data.user_id,
                           today_date=today_date)


# TODO in progress: need to limit data to books and ratings_scores
@app.route("/user/<int:scholar_id>", methods=["POST", "GET"])
def show_user_details(scholar_id):
    """Return page showing the details of a scholar's history."""
    
    # queries database for scholar information by id
    scholar_data = User.query.filter(User.user_id == scholar_id).first()
    
    # queries database for all ratings by the scholar by scholar id
    user_ratings_list = Rating.query.filter(Rating.user_id == scholar_id).all()
    
    # query for badge data for the current reading session.
    badge_data = Badge.query.filter(Badge.badge_id == session['session_badge']).first()

    # calculates how many of different badges were earned
    badges_dict = calculates_total_badges(badges_list, user_ratings_list)


    # calculates total time reading
    total_time = calculates_total_reading_time(user_ratings_list)

    # collects individual book ratings
    book_rating_dict = tally_book_ratings(book_list, user_ratings_list)


    flash("You worked hard %s !" % session['first_name'])
    
    return render_template("user_details.html",
                           today_date=today_date,
                           avatar=scholar_data.avatar,
                           user_details=scholar_data,
                           badge_id=session['session_badge'],
                           time_length = session['time'],
                           user_ratings_list=user_ratings_list,
                           time=total_time,
                           badges_dict=badges_dict,
                           badge_data=badge_data,
                           book_rating_dict=book_rating_dict)


@app.route('/reading-chart.json')
def books_data():
    """Return chart data about scholar's reading history."""
    
    user_ratings_list = Rating.query.filter(Rating.user_id == session['scholar_id']).all()

    book_rating_dict = tally_book_ratings(book_list, user_ratings_list)

    books_data = format_chart_colors(book_rating_dict)
    
    return jsonify(books_data)


# this doesn't work yet
@app.route("/mentor_detail", methods=["POST", "GET"])
def show_mentor_details():
    """Show possible books for scholars  """
    
    # recommendation derived from data.py machine learning library
    sci_fan = [
            "0439420105",
            "0439136369",
            "0440498058",
            "0439139597",
             ]

    main_rec = [
                "0440414806",
                "0441005489",
                "0440407524",
                "0064400557",
                ]
    
    sci_fan_display = display_book_data(book_list, sci_fan)
    
    main_books = display_book_data(book_list, main_rec)
    
    badges_display_list = display_badges(badges_list)
    
    
    return render_template('mentor_detail.html', 
                           today_date=today_date,
                           book_display=main_books,
                           sci_fan_display=sci_fan_display,
                           badges_list=badges_display_list)

                           
@app.route('/mentor-chart.json')
def mentor_data():
    """Return chart data about scholar's reading history.""" 
    
    data = reading_confidence()
    
    return jsonify(data)


@app.route('/site-chart.json')
def site_data():
    """Return json object for aggregated site data"""
    
    sites = format_site_chart()
    
    data = {
        'labels': sites.keys(),
        'datasets': [
          {
            'label': "Reading Engagement by Site in Minutes",
            'fillColor': '#4B5DC3',
            'strokeColor': '#3C3295',
            'highlightFill': '#7DBBD4',
            'highlightStroke': '#A7C9E2',
            'data': sites.values()
          }
         ]
         }
    
    return jsonify(data)


if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    connect_to_db(app)
    
    
    # Queries to db to be available for other files
    user_list = query_all_users()
    book_list = query_all_books()
    session_list = query_all_reading_sessions()
    sidekicks_list = query_all_sidekick()
    ratings_list = query_all_ratings()
    badges_list = query_all_badges()
    sites_list = query_all_sites()

    
    # Flask debugging toolbar
    DebugToolbarExtension(app)
    

    # app config for Cloud9
    # app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

    #app config for local machine
    app.run(debug=True)
