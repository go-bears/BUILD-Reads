from flask_sqlalchemy import SQLAlchemy


# This is the connection to the SQLite database; we're getting this
# through the Flask-SQLAlchemy helper library. On this, we can find
# the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


####################################################################
# Model definitions


# creating database tables for BUILD-reads: Readers, Books, Mentors as "Sidekicks"
# Sites, Ratings, Reading_sessions, Badges, 

class Users(db.Model):
    """Reader information table."""

    __tablename__ = "readers"

    user_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    birthday = db.Column(db.Date, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(25), nullable=False, unique=True)


    def __repr__(self):
        """Show info about reader."""

        return "<reader_id=%d first_name=%s last_name=%s birthday=%d grade=%d>" % \
                                                                                (self.reader_id, 
                                                                                 self.first_name, 
                                                                                 self.last_name, 
                                                                                 self.birthday, 
                                                                                 self.grade)


class Books(db.Model):
    """Book information table."""

    __tablename__ = "books"

    book_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    isbn = db.Column(db.String(150), 
                           nullable=False, 
                           unique=True)
    image_url = db.Column(db.String(150), 
                           nullable=False, 
                           unique=True)
    book_type = db.Column(db.String(10), nullable=False)



class Reading_sessions(db.Model):
    """Book information table."""

    __tablename__ = "reading_sessions"


    session_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True)
    date = db.Column(db.Datetime, nullable=False)
    time_length = db.Column(db.Integer, nullable=False)
    badges_awarded = db.Column(db.Integer, nullable=False)
    rating_score = db.Column(db.Integer, nullable=False)

    
    # set foreign keys from users and books tables
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False) 


class Sidekicks(db.Model):
    """Reading Mentors (aka Sidekicks) information table."""

    __tablename__ = "sidekicks"

    sidekick_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False, unique=True)


class Sites(db.Model):
    """Reading sites information table."""

    __tablename__ = "sites"

    site_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)



class Ratings(db.Model):
    """Ratings information table"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    comment = db.Column(db.String(350), 
                           nullable=False,)

    # set foreign keys from users and books tables
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)


class Badges(db.Model):
    """Badges information table"""

    __tablename__ = "badges"

    badge_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    description = db.Column(db.String(20), nullable=False,)
    image_url = db.Column(db.String(150), nullable=False,)


class SiteRatings(db.Model):
    """docstring for SiteRatings" def __init__(self, arg):
        super(SiteRatings,.__init__()
        self.arg = arg
        