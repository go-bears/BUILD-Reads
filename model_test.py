from flask_sqlalchemy import SQLAlchemy


# This is the connection to the SQLite database; we're getting this
# through the Flask-SQLAlchemy helper library. On this, we can find
# the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


####################################################################
# Model definitions


# creating database tables for BUILD-reads: Readers, Books, Mentors as "Sidekicks"
# Sites, Ratings, Reading_sessions, Badges

class User(db.Model):
    """Reader information table."""

    __tablename__ = "user"

    # values set to nullable for testing
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    grade = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(25), nullable=True, unique=True)
    
    # set site_id foreign key
    site_id = "Berkeley Arts Magnet"


    def __repr__(self):
        """Show info about reader."""

        return "<user_id=%d first_name=%s last_name=%s birthday=%d grade=%d> password=%s" % \
                                                                                (self.user_id, 
                                                                                 self.first_name, 
                                                                                 self.last_name, 
                                                                                 self.birthday, 
                                                                                 self.grade,
                                                                                 self.password)


class Book(db.Model):
    """Book information table."""

    __tablename__ = "books"

    #values set to nullable for testing
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    isbn = db.Column(db.String(150), nullable=True, unique=True)
    image_url = db.Column(db.String(150), nullable=True, unique=True)
    book_type = db.Column(db.String(10), nullable=True)


    def __repr__(self):
        """Show info about book."""

        return "<book_id=%d title=%s description=%s isbn=%s image_url=%s book_type=%s >" % \
                                                                                (self.book_id, 
                                                                                 self.title, 
                                                                                 self.description, 
                                                                                 self.isbn, 
                                                                                 self.image_url,
                                                                                 self.book_type)





def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database for Hackbright Linux
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///build_reads'

    # config for Cloud9
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:build@localhost/build-reads'
    

    db.app = app
    db.init_app(app)
    #postgresql://[[:password][@host][:port]/[database-name]

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    
    # connect to database
    connect_to_db(app)
    
    # create tables 
    db.create_all()
    
    print "Connected to DB."