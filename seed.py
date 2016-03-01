from model import *

from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()

import pandas as pd

ratings = "/home/ubuntu/workspace/test-data/BX-Dump/BX-Book-Ratings.csv"
def open_ratings_csv():
    """Open BX-Book-Ratings.csv separate on semi-colons, set datatype, set headers."""
    
    # open csv and format dataframe
    ratings_df = pd.read_csv(ratings,
                     sep=';',
                     header=None,
                     names=["user_id","isbn", "rating"])

    # change ratings column to number from string        
    ratings_df['rating'] = pd.to_numeric(ratings_df['rating'])
    
    return ratings_df
    
    for rating, row in ratings_df.T.iteritems():
        print rating

open_ratings_csv()




        # bookx_data = Bookx_data(record_id=record_id,
        #             user_id=user_id, 
        #             location=location,
        #             age = age,
        #             isbn = isbn,
        #             rating = rating,
        #             title = title,
        #             author = author,
        #             year = year,
        #             publisher = publisher,
        #             image_link = None)

    #     db.session.add(bookx_data)

    # db.session.commit()


################################################################################
# Helper Functions

# These functions get last value in a database table after seeding database 
# then gives a new id for a new entry. 
# These only need to be run only AFTER seeding db sql alchemy will auto increment again

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(db.func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()
    
    
def set_val_sidekick_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(db.func.max(Sidekick.sidekick_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('sidekicks_sidekick_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_book_id():
    """Set value for the next book_id after seeding database"""

    # Get the Max book_id in the database
    result = db.session.query(db.func.max(Book.book_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('books_book_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_site_id():
    """Set value for the next site_id after seeding database"""

    # Get the Max book_id in the database
    result = db.session.query(db.func.max(Site.site_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('sites_site_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_reading_session_id():
    """Set value for the next reading_session after seeding database"""

    # Get the Max session_id in the database
    result = db.session.query(db.func.max(Reading_session.session_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('reading_sessions_session_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_rating_session_id():
    """Set value for the next rating_session record after seeding database"""

    # Get the Max session_id in the database
    result = db.session.query(db.func.max(Rating.rating_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('ratings_rating_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()



def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database     
    # postgresql://[[:password][@host][:port]/[database-name]

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///build_reads'
    
    # config for Cloud9
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:build@localhost/build_reads'
    
    db.app = app
    db.init_app(app)
    

    set_val_user_id()
    set_val_sidekick_id()
    set_val_book_id()
    set_val_site_id()
    set_val_user_id()
    set_val_reading_session_id()
    set_val_rating_session_id()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # from server import app
    connect_to_db(app)
    # create tables 
    # db.create_all()

    # load_bookx()
#     # import a user_id new user
#     set_val_user_id()

#     print "Connected to DB."