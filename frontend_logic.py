# library for assigning avatars
import random


from flask_sqlalchemy import SQLAlchemy
# from data_preprocessing import *


# data frame 
# BOOK_DATA = y_user_book_ratings_df

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
            

def pick_avatar():
    user_avatar = random.choice(ICON_LIST)
    
    print user_avatar
    return user_avatar


def calculate_badges(time_length):
    if time_length < 20:
        badge_id = 0
    elif time_length >= 20 and time_length < 40:
        badge_id = 1
    elif time_length > 40 and time_length <= 60:
        badge_id = 2
    else:
        badge_id = 3
    
    return badge_id