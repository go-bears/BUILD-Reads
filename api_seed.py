import random
from flask import request
import json
import pprint
import urllib2

import csv
import time
from model import Book, Badge, connect_to_db
# from data_preprocessing import generate_youth_book_ratings

# data frame 
# BOOK_DATA = y_user_book_ratings_df


GOOGLE_BOOKS_SEARCH_ISBN = "https://www.googleapis.com/books/v1/volumes?q=isbn+"
KHAN_ACADEMY_BADGES = 'http://www.khanacademy.org/api/v1/badges/categories'

isbn_filepath = '/home/ubuntu/workspace/test-data/isbn_list.csv'



def open_isbn_list(filepath):
    """Opens csv of ISBNs and generates list of ISBNs  """
    
    isbn_list = []
    with open(filepath) as file_in:
        opened_csv = csv.reader(file_in)
        for row in opened_csv:
            isbn_list.append(row[1])
    
    return isbn_list



def generate_google_books_requests(isbn_list):
    """Builds google books api query urls."""
    
    # check for number items in db to reset this number last is 315
    sample_set = set(isbn_list[3001:4000])
    
    url_list = []
    
    for isbn in sample_set:
        api_url = GOOGLE_BOOKS_SEARCH_ISBN + isbn + "&country=US"
        url_list.append(api_url)

    return url_list
    

def get_book_info(url_list):
    """Takes in a list of urls and searches Google Books API."""
    
    """collects a book cover links, description, & title
    generates placeholder values for ISBN not found"""

    default_book_title = 'ISBN is not matched with title'
    default_book_author = 'ISBN is not matched with an author'
    default_book_cover_sm = None
    default_book_cover_md = None
    default_book_description = "ISBN is not matched with a description"

    for url in url_list:
        isbn = url.split('+')[1].split('&')[0]
        
        time.sleep(1)
        if isbn not in db_isbn:
            # book_request = urllib2.urlopen(url)
            
            request = urllib2.Request(url, headers={'User-agent':'Mozilla/11.0'})
            response = urllib2.urlopen(request)
            book_dict = json.load(response)
        
        
            if book_dict['totalItems'] > 0:
            
                if 'title'in book_dict['items'][0]['volumeInfo'].keys():
                    book_title = book_dict['items'][0]['volumeInfo']['title']
                else:
                    book_title = default_book_title
                
                if 'imageLinks' in book_dict['items'][0]['volumeInfo'].keys():
                    book_cover_sm = book_dict['items'][0]['volumeInfo']['imageLinks']['smallThumbnail']
                    book_cover_md = book_dict['items'][0]['volumeInfo']['imageLinks']['thumbnail']
                else:
                    book_cover_sm = default_book_cover_sm
                    book_cover_md = default_book_cover_md
                
                if 'authors' in book_dict['items'][0]['volumeInfo'].keys():
                    book_author = book_dict['items'][0]['volumeInfo']['authors'][0]
                else:
                    book_author = default_book_author
                    
                if 'description' in book_dict['items'][0]['volumeInfo'].keys():
                    if len(book_dict['items'][0]['volumeInfo']['description']) > 750:
                        book_description = book_dict['items'][0]['volumeInfo']['description'][0:700] + "[...]"
                    else:
                        book_description = book_dict['items'][0]['volumeInfo']['description']
                else:
                    book_description = default_book_description
                
            else:
                # default values in case book cover or information is not available
                book_title = default_book_title
                book_author = default_book_author
                book_cover_sm = default_book_cover_sm
                book_cover_md = default_book_cover_md
                book_description = default_book_description
                
        
            new_book = Book(title=book_title.encode('ascii', 'replace'),
                            author=book_author.encode('ascii', 'replace'),
                            description=book_description.encode('ascii', 'replace'),
                            isbn=isbn,
                            image_url_sm=book_cover_sm,
                            image_url_md=book_cover_md)
        
            print new_book.title
            new_book.commit_to_db()



def get_badges():
    """Gets image urls and description for Khan Academy Badges & commits to db"""
    
    badges_request = urllib2.urlopen(KHAN_ACADEMY_BADGES)
    badges_list = json.load(badges_request)
    
    for i in range(len(badges_list)):
        category = badges_list[i]['category']
        name = badges_list[i]["type_label"]
        img_url = badges_list[i]['email_icon_src']
        description = badges_list[i]['description']
        
        print category
        print img_url
        print description
    
        new_badge = Badge(badge_id=category,
                          name=name,
                          description=description,
                          badge_url=img_url)
        
        new_badge.commit_to_db()
          
                      


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app, query_all_books
    connect_to_db(app)
    # get_badges()
    book_list = query_all_books()   
    
    db_isbn = [book.isbn for book in book_list]
    # print db_isbn
    isbn_list = open_isbn_list(isbn_filepath)
    # isbn_list =['9781484602607', '9780001846531', '9781484602617']
    url_list = generate_google_books_requests(isbn_list)
    
    get_book_info(url_list)
   
    # isbn_list =['9781484602607', '9780001846531', '9781484602617']

# books in isbn list: care and feeding of your gerbil, the phantom tollboooth, null
    # isbn_list = open_isbn_list(isbn_filepath)
    # get_book_info(isbn_list)