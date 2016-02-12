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


    msg = "we are the users", user_list, "we are the books", book_list

    return render_template("index.html", msg=msg)



if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    connect_to_db(app)
    app.run(debug=True)

    

    # app config for Cloud9
    # app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
