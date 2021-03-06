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
        img_src = ' <img class="img-responsive" src="%s"></img> ' % url
        return img_src
    

def calculates_total_badges(badges_list, user_ratings_list):
    """Calculates total and types of badges a reader earns. """
    
    badges_dict = {}
    for user_rating in user_ratings_list:
        
        for badge in badges_list:
            if user_rating.session.badges_awarded == badge.badge_id:
                if badge.name not in badges_dict:
                    print badge.name
                    badges_dict[badge.name] = {"url": badge.badge_url, "count":1}
                else:
                    badges_dict[badge.name]['count'] += 1
    print badges_dict
    return badges_dict
    
def calculates_total_reading_time(user_ratings_list):
    """Calculates the total time length a student has read"""
    
    total_time = 0
    for user_rating in user_ratings_list:
        if user_rating.session.time_length:
            total_time += user_rating.session.time_length
    
    return total_time
    

def tally_book_ratings(book_list, user_ratings_list):
    """ Tally book ratings, stores img, avg score, return dictionary"""
    
    book_rating_dict ={}
    
    for user_rating in user_ratings_list:
        for book in book_list:
            title = book.title
            if user_rating.book.isbn == book.isbn:
                
                if title not in book_rating_dict:
                    # collects scores from ratings, and url from book attribute
                    book_rating_dict[title] = \
                                    {
                                    'score': [user_rating.session.rating_score],
                                    'img': book.image_url_sm,
                                    'description': book.description,
                                    'time_spent': [user_rating.session.time_length],
                                    'comments': []
                                     }
                                          
                else:
                    book_rating_dict[title]['score'].append(user_rating.session.rating_score)
                    book_rating_dict[title]['time_spent'].append(user_rating.session.time_length)
                    
                if len(user_rating.comment) > 2 and user_rating.comment not in book_rating_dict[title]['comments']:
                    book_rating_dict[title]['comments'].append(user_rating.comment)
                    
                # calculates average score                          
                book_rating_dict[title]['avg_score'] = int(numpy.mean(book_rating_dict[title]['score']))
            
                # calculates total time spent reading a specific book
                book_rating_dict[title]['total_time'] = sum(book_rating_dict[title]['time_spent'])

    print book_rating_dict
    return book_rating_dict

def format_chart_colors(book_rating_dict):
    """Assigns color values to different books for doughnut chart """
    
    # color and highlight pairs for charts
    color_list = [('#3E6CBB', '#81C8D5'), ('#976ACD', '#CBC9ED'), 
                  ('#697728', '#BCC247'), ('#BB3E55', '#D685A5'),
                  ('#1B504F', '#349D8B'), ('#774628', '#C68C53'),
                  ('#302267', '#C3BAE8'), ('#19354D', '#5B74C8')
                  ]
    counter = 0
    books_data = {}
    books_data['books'] = []
    
    for key, value in book_rating_dict.iteritems():
        
        key =  {
                "value": value['total_time'],
                "color": color_list[counter][0], 
                "highlight": color_list[counter][1], 
                "label": key
                }
                
        books_data['books'].append(key)    
        counter += 1

    return books_data

def display_book_data(book_list, rec_list):
    """Queries db for top recommended books data"""
                
    display_data = []
    
    for book in book_list:
        for isbn in rec_list:
            if isbn == book.isbn:
                display_data.append(book)
                
    return display_data

# TODO amend database to store reading period data
def display_badges(badges_list):
    """formats badge data for mentor page"""
    
    badge_data = []
    
    for badge in badges_list:
        if badge.badge_id == 0:
            badge.name = {
                'reading period': '0 to 20 minutes',
                'description': badge.description,
                'img': badge.badge_url
                }
        if badge.badge_id ==1:
            badge.name = {
            'reading period': '21 to 40 minutes',
            'description': badge.description,
            'img': badge.badge_url
            }
        if badge.badge_id ==2:
            badge.name = {
            'reading period': '41 to 60 minutes',
            'description': badge.description,
            'img': badge.badge_url
            }
        if badge.badge_id ==3:
            badge.name = {
            'reading period': '61 to 80 minutes',
            'description': badge.description,
            'img': badge.badge_url
            }
        if badge.badge_id ==4:
            badge.name = {
            'reading period': '81 to 100 minutes',
            'description': badge.description,
            'img': badge.badge_url
            }
        if badge.badge_id ==5:
            badge.name = {
            'reading period': '101 to 120 minutes',
            'description': badge.description,
            'img': badge.badge_url
            }
        badge_data.append(badge.name)
            
    return badge_data
    
def format_site_chart():
    """formatting data of session logs per site"""
    
    sites = {
            "Bahia School Age Program": 1100,
            "Berkeley Arts Magnet":2000,
            "Berkeley Maynard Academy":900,
            "Berkeley Youth Alternatives":800,
            "Cragmont Elementary":1000,
            "Emerson Elementary--Oakland":950,
            "Emerson Elementary":950,
            "James Kenney Recreation Center":700,
            "Jefferson Elementary":800,
            "John Muir Elementary":1500,
            "Lafayette Elementary":800,
            "LeConte Elementary School":1000,
            "Malcolm X Elementary School":500,
            "Martin Luther King, Jr. Elementary School":600,
            "Oxford Elementary":650,
            "Rosa Parks":400,
            "Sankofa":1000,
            "Think College Now":750,
            "Thousand Oaks":1300,
            "Washington Elementary":500,
            "Young Adult Project":200,
            }
            
            
    return sites

def reading_confidence():
    """Returns JSON object of BUILD reading confidence data """
    
    data = {}
    data['interest'] =[
        {
            "value": 8,
            "color":"#F7464A",
            "highlight": "#FF5A5E",
            "label": "A Little"
        },
        {
            "value": 36,
            "color": "#46BFBD",
            "highlight": "#5AD3D1",
            "label": "Somewhat"
        },
        {
            "value": 57,
            "color": "#FDB45C",
            "highlight": "#FFC870",
            "label": "A Lot"
        }
        ]
        
    return data