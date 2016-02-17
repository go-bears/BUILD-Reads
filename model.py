from datetime import date

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.postgresql import JSON


# This is the connection to the SQLite database; we're getting this
# through the Flask-SQLAlchemy helper library. On this, we can find
# the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


####################################################################
# Model definitions


# creating database tables for BUILD-reads: Readers, Books, Mentors as "Sidekicks"
# Sites, Ratings, Reading_sessions, Badges

# User class adds to build_reads db successfully
class User(db.Model):
    """Reader information table."""

    __tablename__ = "users"

    # values set to nullable for testing
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    #birthday needs to be passed to sqlalchemy as a datetime object
    birthday = db.Column(db.Date, nullable=True)
    grade = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(25), nullable=True)
    
    # set site_id foreign key
    site_id = db.Column(db.Integer, 
                        db.ForeignKey('sites.site_id'), 
                        nullable=True)
    site = db.relationship('Site', 
                            backref=db.backref("sites", order_by=user_id))
    

    
    def commit_to_db(self):
        """ add user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited", self.first_name, "to the database"
        
    


    def __repr__(self):
        """Show info about reader."""

        return "<first_name=%s last_name=%s birthday=%s\
        grade=%s site=%s password=%s>" %(self.first_name, 
                                            self.last_name, 
                                            self.birthday, 
                                            self.grade,
                                            self.site,
                                            self.password)

# Book class adds to build_reads db successfully
class Book(db.Model):
    """Book information table."""

    __tablename__ = "books"

    #values set to nullable for testing
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    isbn = db.Column(db.String(150), nullable=True)
    image_url = db.Column(db.String(150), nullable=True)
    book_type = db.Column(db.String(10), nullable=True)

    
    def commit_to_db(self):
        """ add instance of user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited", self.title, "to the database"
        


    def __repr__(self):
        """Show info about book."""

        return "<title=%s description=%s isbn=%s image_url=%s book_type=%s >"\
                                                           %(self.title, 
                                                             self.description, 
                                                             self.isbn, 
                                                             self.image_url,
                                                             self.book_type)


class Sidekick(db.Model):
    """Reading Mentors (aka Sidekicks) information table."""

    __tablename__ = "sidekicks"

    sidekick_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(25), nullable=True)

    # set foreign keys from user table
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=True)

    # set relationship between Reading_sessions and User & Book classes
    user = db.relationship('User', 
                           backref=db.backref("sidekicks", 
                           order_by=sidekick_id))


    def commit_to_db(self):
        """ add instance of user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited the sidekick", self.first_name, "to the database"


    def __repr__(self):
        """Show info about sidekick."""

        return "<first_name=%s last_name=%s password=%s >" % (self.first_name, 
                                                              self.last_name,
                                                              self.password)

class Site(db.Model):
    """Reading sites information table."""

    __tablename__ = "sites"

    site_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(50), nullable=True)


    def commit_to_db(self):
        """ add instance of user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited the sidekick", self.name, "to the database"

    def __repr__(self):
        """Show info about site."""

        return "<name=%s location=%s >" % (self.name, self.location)


class Reading_session(db.Model):
    """Book information table."""

    __tablename__ = "reading_sessions"


    session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # date needs to be passed to sqlalchemy as a datetime object
    date = db.Column(db.DateTime, nullable=True)
    
    time_length = db.Column(db.Integer, nullable=True)
    badges_awarded = db.Column(db.Integer, nullable=True)
    rating_score = db.Column(db.Integer, nullable=True)
    
    # set foreign keys from users and books tables
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=True)
    book_id = db.Column(db.Integer, 
                        db.ForeignKey('books.book_id'), 
                        nullable=True) 
    sidekick_id = db.Column(db.Integer, 
                            db.ForeignKey('sidekicks.sidekick_id'), 
                            nullable=True) 

    # set relationship between Reading_sessions and User & Book classes
    user = db.relationship('User', 
                           backref=db.backref("reading_sessions", 
                           order_by=session_id))
    book = db.relationship('Book', 
                           backref=db.backref("reading_sessions", 
                           order_by=session_id))
    sidekick = db.relationship('Sidekick', 
                               backref=db.backref("reading_sessions", 
                               order_by=session_id))



    def commit_to_db(self):
        """ add instance of user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited the session at", self.date,\
              "with", self.badges_awarded, "badges to the database"

    def __repr__(self):
        """Show info about reading_session."""

        return "<date=%s time_length =%s badges_awarded=%s rating_score=%s \
                user_id=%d book_id=%d >" %  (self.date, 
                                             self.time_length, 
                                             self.badges_awarded, 
                                             self.rating_score,
                                             self.user_id,
                                             self.book_id)


class Rating(db.Model):
    """Ratings information table"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(350), nullable=True,)

    # set foreign keys from users and books tables
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=True)
                        
    book_id = db.Column(db.Integer, 
                        db.ForeignKey('books.book_id'), 
                        nullable=True)
    
    session_id = db.Column(db.Integer, 
                           db.ForeignKey('reading_sessions.session_id'), 
                           nullable=True) 
    
    # set relationship between Ratings with User & Book classes
    user = db.relationship('User', 
                            backref=db.backref("ratings", 
                                                order_by=rating_id))
                                                      
    book = db.relationship('Book', 
                            backref=db.backref("ratings", 
                                               order_by=rating_id))
                                                      
    session = db.relationship('Reading_session', 
                             backref=db.backref("ratings", 
                                                order_by=rating_id))


    def commit_to_db(self):
        """ add instance of Rating to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited the rating", self.rating_score,\
              "with comment", self.comment, "to the database"


    def __repr__(self):
        """Show info about rating."""

        return "<rating_id=%d comment=%s user_id=%d book_id=%d >" \
                                                            %(self.rating_id, 
                                                              self.comment, 
                                                              self.user_id, 
                                                              self.book_id)






class Badge(db.Model):
    """Badges information table"""

    __tablename__ = "badges"

    badge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(50), nullable=True,)
    # badge_data = db.Column('data', JSON, nullable=True)



    def commit_to_db(self):
        
        """ add instance of Rating to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited the badge", self.description, "to the database"

    def __repr__(self):
        """Show info about rating."""

        return "<description=%s>" % (self.description)



# ####################################################################
# # Association Tables

class SiteRating(db.Model):
    """Association table for Sites and Ratings"""

    __tablename__ = "site_rating"

    # TODO add primary keys 
    SiteRating = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.site_id'), nullable=True)
    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.rating_id'), nullable=True)


    def __repr__(self):
        """Show info about site_rating."""

        return "<site_id=%d rating_id=%d >" % (self.site_id, self.rating_id)



class BookRating(db.Model):
    """Association table for Books and Ratings"""

    __tablename__ = "book_rating"

    BookRating = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=True)
    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.rating_id'), nullable=True)


    def __repr__(self):
        """Show info about book_rating."""
        
        return "<book_id=%d rating_id=%d >" % (self.book_id, self.rating_id)


class UserBadge(db.Model):
    """Association table for Users and Badges"""

    __tablename__ = "user_badge"

    UserBadge = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
   

    def __repr__(self):
        """Show info about user_rating."""

        return "<book_id=%d rating_id=%d >" % (self.user_id, self.badge_id)


#####################################################################################
# Helper Functions

# These functions get last value in a database table and 
# then gives a new id for a new entry
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





def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database     
    # postgresql://[[:password][@host][:port]/[database-name]

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///build_reads'
    
    # config for Cloud9
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:build@localhost/build_reads'
    
    db.app = app
    db.init_app(app)
    

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)

    # create tables 
    db.create_all()

    # import a user_id new user
    # set_val_user_id()

    print "Connected to DB."