# TODO re-write Books model to include author, year, publisher, and open library cover images
# # Add new model for training data table
# re-write user for avatar image

from datetime import date

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import backref, relationship


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
    avatar = db.Column(db.String(50), nullable=True)
    
    
    
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
        grade=%s site=%s password=%s avatar=%s>" %(self.first_name, 
                                            self.last_name, 
                                            self.birthday, 
                                            self.grade,
                                            self.site,
                                            self.password,
                                            self.avatar)

# Book class adds to build_reads db successfully
class Book(db.Model):
    """Book information table."""

    __tablename__ = "books"

    #values set to nullable for testing
    title = db.Column(db.String(150), nullable=True)
    author = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    isbn = db.Column(db.String(15), primary_key=True, 
                     nullable=True, unique=True)
    image_url_sm = db.Column(db.String(200), nullable=True)
    image_url_md = db.Column(db.String(200), nullable=True)

    
    def commit_to_db(self):
        """ add instance of user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited", self.title, "to the database"
        


    def __repr__(self):
        """Show info about book."""

        return "<title=%s author=%s description=%s isbn=%s \
                image_url_sm =%s image_url_md=%s >" %(self.title, 
                                                      self.author,
                                                      self.isbn,
                                                      self.description,
                                                      self.image_url_sm,
                                                      self.image_url_md)
                                                           

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
    
    ratings = db.session


    def commit_to_db(self):
        """ add instance of user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited the sidekick", self.name, "to the database"

    def __repr__(self):
        """Show info about site."""

        return "<name=%s location=%s >" % (self.name, self.location)


class Badge(db.Model):
    """Badges information table"""

    __tablename__ = "badges"

    badge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(300), nullable=True)
    badge_url = db.Column(db.String(100), nullable=True)


    def commit_to_db(self):
        
        """ add instance of Rating to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited the badge", self.description, "to the database"

    def __repr__(self):
        """Show info about rating."""

        return "<description=%s>" % (self.description)


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
                        nullable=False)
    isbn = db.Column(db.String(15), 
                        db.ForeignKey('books.isbn'), 
                        nullable=False) 
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
                user_id=%d isbn=%s >" %  (self.date, 
                                             self.time_length, 
                                             self.badges_awarded, 
                                             self.rating_score,
                                             self.user_id,
                                             self.isbn)


class Rating(db.Model):
    """Ratings information table"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(350), nullable=True,)

    # set foreign keys from users and books tables
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=False)
                        
    isbn = db.Column(db.String(15), 
                        db.ForeignKey('books.isbn'), 
                        nullable=False)
    
    session_id = db.Column(db.Integer, 
                           db.ForeignKey('reading_sessions.session_id'), 
                           nullable=False) 
    
    # set backref relationship between Ratings with User & Book classes
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

        print "I commited the rating", self.rating_id,\
              "with comment", self.comment, "to the database"


    def __repr__(self):
        """Show info about rating."""

        return "<rating_id=%d comment=%s user_id=%d isbn=%s >" \
                                                            %(self.rating_id, 
                                                              self.comment, 
                                                              self.user_id, 
                                                              self.isbn)


class Bookx_data(db.Model):
    """Book Crossing table creating """
    
    __tablename__ = "bookx_data"
    
    record_id = db.Column(db.String(10), primary_key=True, nullable=True) 
    user_id = db.Column(db.String(10), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    isbn = db.Column(db.String(15), 
                     db.ForeignKey('books.isbn'),
                     nullable=True, 
                     unique=True)
                     
    rating = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(150), nullable=True)
    author = db.Column(db.String(50), nullable=True)
    year =  db.Column(db.Integer, nullable=True)
    publisher = db.Column(db.String(50), nullable=True)
    image_link = db.Column(db.String(200), nullable=True)
    

    
    # set backref relationship between Bookx_data with Book classes
    book = db.relationship('Book', 
                            backref=db.backref("Bookx_data",
                            order_by=isbn))


    def __repr__(self):
        """Show info about Bookx_data."""
    
        return "<user_id=%s location=%s age=%d isbn=%s rating=%d <title=%s \
                author=% year=%d publisher=%s image_link=%s>"  % (self.record_id, 
                                                                  self.user_id, 
                                                                  self.location, 
                                                                  self.age,
                                                                  self.isbn,
                                                                  self.rating,
                                                                  self.title,
                                                                  self.author,
                                                                  self.year,
                                                                  self.publisher,
                                                                  self.image_link)

# ####################################################################
# # Association Tables

class SiteRating(db.Model):
    """Association table for Sites and Ratings"""

    __tablename__ = "site_rating"

     
    SiteRating = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    site_id = db.Column(db.Integer,
                        db.ForeignKey('sites.site_id'), 
                        nullable=True)
    rating_id = db.Column(db.Integer,
                          db.ForeignKey('ratings.rating_id'),
                          nullable=True)


    def __repr__(self):
        """Show info about site_rating."""

        return "<site_id=%d rating_id=%d >" % (self.site_id, self.rating_id)



class BookRating(db.Model):
    """Association table for Books and Ratings"""

    __tablename__ = "book_rating"

    BookRating = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
                               
    isbn = db.Column(db.String(15),
                        db.ForeignKey('books.isbn'),
                        nullable=True)
    rating_id = db.Column(db.Integer,
                          db.ForeignKey('ratings.rating_id'),
                          nullable=True)


    def __repr__(self):
        """Show info about book_rating."""
        
        return "<isbn=%s rating_id=%d >" % (self.isbn, self.rating_id)


class UserBadge(db.Model):
    """Association table for Users and Badges"""

    __tablename__ = "user_badge"

    UserBadge = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=True)
   

    def __repr__(self):
        """Show info about user_rating."""

        return "<user_id=%d rating_id=%d >" % (self.user_id, self.badge_id)



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