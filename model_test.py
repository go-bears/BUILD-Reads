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


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:build@localhost/build-reads'
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