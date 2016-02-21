import random
from flask import request, session

from data_preprocessing import *




icon_list =["fa fa-camera-retro fa-4x", 
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
    user_avatar = random.choice(icon_list)
    
    print user_avatar
    return user_avatar


def get_book_covers(titles):
        titles = book_dict 
        print titles
        # user_ratings_list = Rating.query.filter(Rating.user_id == session['scholar_id']).all()




# def get_openlib_bookcover():
#     """Based on a book ISBN, fetch bookcover linke from OpenLib."""

#     # get ISBNs of books that need subject info
#     book_data = book_data['isbn']
    
#     need_subjects = Book.query.filter(Book.get_subjects==1, Book.isbn!='0').all()
#     print "need subjects for:", len(need_subjects)

#     subject_dict = {}
#     openlib_count = 0

#     for book in need_subjects:
#         current_isbn = book.isbn
#         response = requests.get("https://openlibrary.org/api/books?bibkeys=ISBN:%s&format=json&jscmd=data" % (current_isbn))
#         book_info = response.json()
        
#         if book_info.keys():
#             current_key = "ISBN:%s" % (current_isbn)
#             if book_info[current_key].get('subjects', None):
#                 openlib_count += 1
#                 categories = book_info[current_key]['subjects']
                
#                 # save categories in subject table; mark source as google-books
#                 for category in categories:
#                     category = category['name'].lower()
#                     # print "category:", category, type(category)

#                     is_subject = Subject.query.filter_by(subject=category).first()
#                     if is_subject == None:
#                         subject = Subject(subject=category, source='OpenLib')
#                         db.session.add(subject)

#                     if subject_dict.get(book.book_id, None):
#                         subject_dict[book.book_id].append(category)
#                     else:
#                         subject_dict[book.book_id] = [category]
#     print "retrieved subjects for:", openlib_count
#     db.session.commit() 
#     return subject_dict
