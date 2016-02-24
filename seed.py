

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

