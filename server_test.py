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


# Collects the form information 
@app.route('/log_reading_session', methods=["GET","POST"])
def log_reading_session():
    """Collects reading session data and logs reading session to db."""

    # reader's name from Flask session
    user = session['first_name']

    # information message for me
    msg = "I recorded the reading log information"
    
    # 
    today = datetime.now()

    # TODO get for the data from the form fields


    # queries db for user information by first name. this is ok for now.
    #TODO make query smarter by searching by first and last name or get query from data in Flask Session
    user_data = db.session.query(User).filter((User.first_name==user)).first()
    print user_data

    book_data = db.session.query(Book).filter(Book.title==title).first()
    print book_data
    sidekick_data = db.session.query(Sidekick).filter(Book.title).first()
    print sidekick_data
    #TODO  connect form data to db requirements for reading session record
    # new_reading_session = Reading_session(new_session_id = set_val_reading_session_id()
    # session_id = new_session_id,     
    #  date = today,
    #  time_length =   #session_length
    #  badges_awarded = #write this function 1 badge for 20min 2 for 40 min3 for 60min
    #  rating_score  = #
    #  user_id  = user_data.user_id
    #  book_id  = book_data.book_id      
    #  sidekick_id = sidekick_data.sidekick_id
    # )


    flash("Great Work! I logged your reading session %s !" % user)

    return render_template("reading_session.html", msg=msg, sidekicks=sidekicks)

if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    connect_to_db(app)
    app.run(debug=True)

    # app config for Cloud9
    # app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
