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

class Readers(db.Model):
    """Reader information table."""

    __tablename__ = "Readers"

    reader_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    birthday = db.Column(db.Date, nullable=False)
    grade = db.Column(db.Integer, nullable=False)


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