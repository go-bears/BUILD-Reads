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

# User class adds to build_reads db successfully
class User(db.Model):
    """Reader information table."""

    __tablename__ = "users"

    # values set to nullable for testing
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    grade = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(25), nullable=True)
    
    # set site_id foreign key
    #site_id = db.relationship('Site', backref=db.backref("sites", order_by=user_id))
    
    # site_id temporarily hardcoded
    site_id = 1

    
    def commit_to_db(self):
        """ add user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited", self.first_name, "to the database"
        
        
    def __repr__(self):
        """Show info about reader."""

        return "<first_name=%s last_name=%s birthday=%s grade=%s site_id=%s password=%s>"\
                                                                               %(self.first_name, 
                                                                                 self.last_name, 
                                                                                 self.birthday, 
                                                                                 self.grade,
                                                                                 self.site_id,
                                                                                 self.password)

# Book class adds to build_reads db successfully
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


class Reading_session(db.Model):
    """Book information table."""

    __tablename__ = "reading_sessions"


    session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # error: column "date" is of type timestamp without time zone but expression is of type integer
    #date = db.Column(db.Date, nullable=True)
    
    time_length = db.Column(db.Integer, nullable=True)
    badges_awarded = db.Column(db.Integer, nullable=True)
    rating_score = db.Column(db.Integer, nullable=True)
    
    # set foreign keys from users and books tables
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=True) 
    sidekick_id = db.Column(db.Integer, db.ForeignKey('sidekicks.sidekick_id'), nullable=True) 

    # set relationship between Reading_sessions and User & Book classes
    user = db.relationship('User', backref=db.backref("reading_sessions", order_by=session_id))
    book = db.relationship('Book', backref=db.backref("reading_sessions", order_by=session_id))
    sidekick = db.relationship('Sidekick', backref=db.backref("reading_sessions", order_by=session_id))



    def commit_to_db(self):
        """ add instance of user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited a session lasting", self.time_length, "minutes with score of",\
               self.rating_score, "to the database"

    
    def __repr__(self):
        """Show info about reading_session."""

        return "time_length =%s badges_awarded=%s rating_score=%s \
                user_id=%d book_id=%d >" %  (#self.date, 
                                             self.time_length, 
                                             self.badges_awarded, 
                                             self.rating_score,
                                             self.user_id,
                                             self.book_id)



class Sidekick(db.Model):
    """Reading Mentors (aka Sidekicks) information table."""

    __tablename__ = "sidekicks"

    sidekick_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(25), nullable=True)

    # set foreign keys from user table
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    # set relationship between Reading_sessions and User & Book classes
    user = db.relationship('User', backref=db.backref("sidekicks", order_by=sidekick_id))


    def commit_to_db(self):
        """ add instance of user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited", self.first_name, "to the database"
        


    def __repr__(self):
        """Show info about sidekick."""

        return "<first_name=%s last_name=%s password=%s >" % (self.first_name, 
                                                              self.last_name,
                                                              self.password)
        

class Rating(db.Model):
    """Ratings information table"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(350), nullable=True,)

    # set foreign keys from users and books tables
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)

    # set relationship between Ratings with User & Book classes
    user = db.relationship('User', backref=db.backref("ratings", order_by=rating_id))
    book = db.relationship('Book', backref=db.backref("ratings", order_by=rating_id))


    def commit_to_db(self):
        """ add instance of user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited", self.first_name, "to the database"


    def __repr__(self):
        """Show info about rating."""

        return "<rating_id=%d comment=%s user_id=%d book_id=%d >" % (self.rating_id, 
                                                                     self.comment, 
                                                                     self.user_id, 
                                                                     self.book_id)


class Badge(db.Model):
    """Badges information table"""

    __tablename__ = "badges"

    badge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(50), nullable=True,)
    image_url = db.Column(db.String(150), nullable=True, unique=True)


    def commit_to_db(self):
        """ add instance of user to build_reads db"""

        db.session.add(self)
        db.session.commit()

        print "I commited", self.description, "to the database"

    def __repr__(self):
        """Show info about rating."""

        return "<description=%s image_url=%s >" % (self.description, self.image_url)


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
