# import statment for running on cloud 9
#import os 

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from model_test import *

app = Flask(__name__)
#db = SQLAlchemy(app)

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


    msg = "we are the users", user_list, "<br> we are the books", book_list,\
            "<br> We are the sessions", session_list,\
            "<br> We are the sidekicks", sidekicks_list,\
            "We are ratings_list", ratings_list

    return render_template("index.html", msg=msg)



if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    connect_to_db(app)
    app.run(debug=True)

    

    # app config for Cloud9
    # app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
