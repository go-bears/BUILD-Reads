# library for assigning avatars
import random
import numpy

from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy


def pick_avatar():
    """Selects avatar for reader.Selects"""
    
    # avatar choices from font awesome
    ICON_LIST =["fa fa-camera-retro fa-4x", 
                "fa fa-hand-peace-o fa-4x", 
                "fa fa-plane fa-4x",
                "fa fa-rocket fa-4x",
                "fa fa-space-shuttle fa-4x",
                "fa fa-taxi fa-4x",
                "fa fa-bicycle fa-4x",  
                "fa fa-truck fa-4x",
                "fa fa-lightbulb-o fa-4x",
                "fa fa-birthday-cake fa-4x"]
            
    
    user_avatar = random.choice(ICON_LIST)
    
    return user_avatar

def calculate_badges(time_length):
    """Calculates which badge is awarded per reading session."""

    if time_length < 20:
        badge_id = 0
    elif time_length >= 20 and time_length < 40:
        badge_id = 1
    elif time_length > 40 and time_length <= 60:
        badge_id = 2
    else:
        badge_id = 3
    
    return badge_id


def birthday_format(str_birthday):
    """Formats birthday to date time object. """   
    
    print "this string", str_birthday
    
    year, month, day = str_birthday.split('-')
    print 'this is the split string,', year, month, day
    # converting string into datetime object for db
    birthday = date(int(year), int(month), int(day))
    print "this is the birthday date obj", birthday
    
    return birthday


def convert_url_to_img_tag(url):
    """Adds html tags to http urls, returns list"""
    
    if url.startswith('http'):
        img_src = ' <img src="%s"></img> ' % url
        return img_src
    

def calculates_total_badges(badges_list, user_ratings_list):
    """Calculates total and types of badges a reader earns. """
    
    badges_dict = {}
    for user_rating in user_ratings_list:
        for badge in badges_list:
            if user_rating.session.badges_awarded == badge.badge_id:
                if badge.name not in badges_dict:
                    badges_dict[badge.name] = {"url": badge.badge_url, "count":1}
                else:
                    badges_dict[badge.name]['count'] += 1
                    
            
    return badges_dict
    
def calculates_total_reading_time(user_ratings_list):
    """Calculates the total time length a student has read"""
    
    total_time = 0
    for user_rating in user_ratings_list:
        if user_rating.session.time_length:
            total_time += user_rating.session.time_length
    
    return total_time
    

def tally_book_ratings(book_list, user_ratings_list):
    """ Tally individual book ratings, stores img, avg score, return dictionary"""
    
    book_rating_dict ={}
    
    for user_rating in user_ratings_list:
        for book in book_list:
            title = book.title
            if user_rating.book.isbn == book.isbn:
                # collects scores from ratings, and url from book attribute
                book_rating_dict[title] = {'score': [user_rating.session.rating_score],
                                          'img': book.image_url_sm,
                                          'description': book.description}
                                          
                # calcuates average score                          
                book_rating_dict[title]['avg_score'] = int(numpy.ceil(book_rating_dict[title]['score']))
    
    print book_rating_dict
    return book_rating_dict



