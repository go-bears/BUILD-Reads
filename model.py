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
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(25), nullable=False, unique=True)
    
    # set site_id foreign key
    site_id = db.Column(db.Integer, db.ForeignKey('site.site_id'), nullable=False)
    
    # set seit relationship in database
    site = db.relationship('User', backref=db.backref("Site", order_by=user))


    def __repr__(self):
        """Show info about reader."""

        return "<user_id=%d first_name=%s last_name=%s birthday=%d grade=%d> password=%s" % \
                                                                                (self.user_id, 
                                                                                 self.first_name, 
                                                                                 self.last_name, 
                                                                                 self.birthday, 
                                                                                 self.grade,
                                                                                 self.password)


# class Book(db.Model):
#     """Book information table."""

#     __tablename__ = "book"

#     book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(150), nullable=False)
#     description = db.Column(db.String(500), nullable=False)
#     isbn = db.Column(db.String(150), nullable=False, unique=True)
#     image_url = db.Column(db.String(150), nullable=False, unique=True)
#     book_type = db.Column(db.String(10), nullable=False)


#     def __repr__(self):
#         """Show info about book."""

#         return "<book_id=%d title=%s description=%s isbn=%s image_url=%s book_type=%s >" % \
#                                                                                 (self.book_id, 
#                                                                                  self.title, 
#                                                                                  self.description, 
#                                                                                  self.isbn, 
#                                                                                  self.image_url,
#                                                                                  self.book_type)


# class Reading_session(db.Model):
#     """Book information table."""

#     __tablename__ = "reading_session"


#     session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     date = db.Column(db.DateTime, nullable=False)
#     time_length = db.Column(db.Integer, nullable=False)
#     badges_awarded = db.Column(db.Integer, nullable=False)
#     rating_score = db.Column(db.Integer, nullable=False)
    
#     # set foreign keys from users and books tables
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False) 
#     sidekick_id = None #fill this in

#     # set relationship between Reading_sessions and User & Book classes
#     user = db.relationship('User', backref=db.backref("reading_session", order_by=session_id))
#     book = db.relationship('Book', backref=db.backref("reading_session", order_by=session_id))


#     def __repr__(self):
#         """Show info about reading_session."""

#         return "<session_id=%d date=%d time_length =%d badges_awarded=%s rating_score=%s \
#                 user_id=%d book_id=%d >" %  (self.session_id, 
#                                              self.date, 
#                                              self.time_length, 
#                                              self.badges_awarded, 
#                                              self.rating_score,
#                                              self.user_id,
#                                              self.book_id)


# class Sidekick(db.Model):
#     """Reading Mentors (aka Sidekicks) information table."""

#     __tablename__ = "sidekick"

#     sidekick_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     password = db.Column(db.String(25), nullable=False, unique=True)

#     # set foreign keys from user table
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

#     # set relationship between Reading_sessions and User & Book classes
#     user = db.relationship('User', backref=db.backref("sidekick", order_by=sidekick_id))


#     def __repr__(self):
#         """Show info about sidekick."""

#         return "<sidekick_id=%d first_name=%s last_name=%s password=%s >" % (self.sidekick_id, 
#                                                                              self.first_name, 
#                                                                              self.last_name, 
#                                                                              self.password)


# class Site(db.Model):
#     """Reading sites information table."""

#     __tablename__ = "site"

#     site_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(50), nullable=False)
#     location = db.Column(db.String(50), nullable=False)


#     def __repr__(self):
#         """Show info about site."""

#         return "<site_id=%d name=%s location=%s >" % (self.site_id, 
#                                                       self.name, 
#                                                       self.location)


# class Rating(db.Model):
#     """Ratings information table"""

#     __tablename__ = "rating"

#     rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     comment = db.Column(db.String(350), nullable=True,)

#     # set foreign keys from users and books tables
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)

#     # set relationship between Ratings with User & Book classes
#     user = db.relationship('User', backref=db.backref("rating", order_by=rating_id))
#     book = db.relationship('Book', backref=db.backref("rating", order_by=rating_id))


#     def __repr__(self):
#         """Show info about rating."""

#         return "<rating_id=%d comment=%s user_id=%d book_id=%d >" % (self.rating_id, 
#                                                                      self.comment, 
#                                                                      self.user_id, 
#                                                                      self.book_id)

# class Badge(db.Model):
#     """Badges information table"""

#     __tablename__ = "badge"

#     badge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     description = db.Column(db.String(20), nullable=False,)
#     image_url = db.Column(db.String(150), nullable=False, unique=True)


#     def __repr__(self):
#         """Show info about rating."""

#         return "<badge_id=%d description=%s image_url=%s >" % (self.badge_id, 
#                                                               self.description, 
#                                                               self.image_url)



# ####################################################################
# # Association Tables

# class SiteRating(db.Model):
#     """Association table for Sites and Ratings"""

#     __tablename__ = "site_rating"

#     # TODO add primary keys 

#     site_id = db.Column(db.Integer, db.ForeignKey('site.site_id'), nullable=False)
#     rating_id = db.Column(db.Integer, db.ForeignKey('rating.rating_id'), nullable=False)


#     def __repr__(self):
#         """Show info about site_rating."""

#         return "<site_id=%d rating_id=%d >" % (self.site_id, self.rating_id)


# # TODO add primary keys
# class BookRating(db.Model):
#     """Association table for Books and Ratings"""

#     __tablename__ = "book_rating"

#     book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
#     rating_id = db.Column(db.Integer, db.ForeignKey('ratings.rating_id'), nullable=False)


#     def __repr__(self):
#         """Show info about book_rating."""

#         return "<book_id=%d rating_id=%d >" % (self.book_id, self.rating_id)

# #TODO add primary keys
# class UserBadge(db.Model):
#     """Association table for Users and Badges"""

#     __tablename__ = "user_badge"

#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#     badge_id = db.Column(db.Integer, db.ForeignKey('badge.badge_id'), nullable=False)


#     def __repr__(self):
#         """Show info about user_rating."""

#         return "<book_id=%d rating_id=%d >" % (self.user_id, self.badge_id)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:build/ratings'
    db.app = app
    db.init_app(app)
postgresql://[[:password][@host][:port]/[database-name]

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."