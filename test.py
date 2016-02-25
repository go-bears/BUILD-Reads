import random
from flask import request
import json
import pprint
import urllib2
# from data_preprocessing import generate_youth_book_ratings

# data frame 
# BOOK_DATA = y_user_book_ratings_df


GOOGLE_BOOKS_SEARCH_ISBN = "https://www.googleapis.com/books/v1/volumes?q=isbn+"
KHAN_ACADEMY_BADGES = 'http://www.khanacademy.org/api/v1/badges/categories'

def book_search(title):
    """Searches for an isbn number by title in Bookx_data or in Open library"""
    pass
    # book_data .str.lower()

def generate_google_books_requests(isbn_list):
    """Builds google books api query urls."""
    
    url_list = []
    
    for isbn in isbn_list:
        api_url = GOOGLE_BOOKS_SEARCH_ISBN + isbn
        url_list.append(api_list)
    
    return url_list
    

def get_book_info(url_list):
    """Takes in a list of urls and searches Google Books API."""
    
    """collects a book cover links, description, & title
    generates placeholder values for ISBN not found"""

    default_book_title = 'ISBN is not matched with title'
    default_book_cover_sm = '<i class="fa fa-book 3x"></i>'
    default_book_cover_md = '<i class="fa fa-book 4x"></i>'
    default_book_description = "ISBN is not matched with a description"

    for isbn in isbn_list:
        book_request = urllib2.urlopen(GOOGLE_BOOKS_SEARCH_ISBN + isbn)
        book_dict = json.load(book_request)
        
        if book_dict['totalItems'] > 0:
        
            if 'title'in book_dict['items'][0]['volumeInfo'].keys():
                book_title = book_dict['items'][0]['volumeInfo']['title']
            
            if 'imageLinks' in book_dict['items'][0]['volumeInfo'].keys():
                book_cover_sm = book_dict['items'][0]['volumeInfo']['imageLinks']['smallThumbnail']
                book_cover_md = book_dict['items'][0]['volumeInfo']['imageLinks']['thumbnail']
            else:
                book_cover_sm = default_book_cover_sm
                book_cover_md = default_book_cover_md
                
                
                # book_cover = '<i class="fa fa-book"></i>'
                # book_description = "A description is not available for this title"
            if 'description' in book_dict['items'][0]['volumeInfo'].keys():
                book_description = book_dict['items'][0]['volumeInfo']['description']
            
        else:
            # default values in case book cover or information is not available
            book_title = default_book_title
            book_cover_sm = default_book_cover_sm
            book_cover_md = default_book_cover_md
            book_description = default_book_description
            
        
        print book_dict['totalItems']
        # print book_dict['items'][0]['volumeInfo']
        print book_title
        print book_cover_sm
        print book_cover_md
        print book_description
        # pprint.pprint(book_response)




def get_badges():
    """Gets image urls and description for Khan Academy Badges """
    
    badges_request = urllib2.urlopen(KHAN_ACADEMY_BADGES)
    badges_list = json.load(badges_request)
    
    for i in range(len(badges_list)):
        category = badges_list[i]['category']
        img_url = badges_list[i]['email_icon_src']
        description = badges_list[i]['description']
        
        print category
        print img_url
        print description
    
    
    # pprint.pprint(badges_list[0])
get_badges()



# books in isbn list: care and feeding of your gerbil, the phantom tollboooth, null
isbn_list = ['9781484602607', '9780001846531', '9781484602617']
# get_book_info(isbn_list)

