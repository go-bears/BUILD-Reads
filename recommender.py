import pandas as pd
import csv
import codecs
import numpy as np
import numexpr
from scipy.stats.stats import pearsonr
import json

from data_preprocessing import y_user_book_ratings



data = y_user_book_ratings

# Picking 2 books 
book_1 = "Harry Potter and the Chamber of Secrets" 
book_2 = "Harry Potter and the Sorcerer's Stone (Harry Potter (Paperback))"

# collect people who rated book 1 from db
book_1_raters = data[data.title == book_1].user_id
# collect people who rated book 2 from db
book_2_raters = data[data.title == book_2].user_id

# create a set of raters that have rated book 1 and book 2
common_raters = set(book_1_raters).intersection(book_2_raters)
print "%d people have reviewed these 2 books" % len(common_raters)


def get_book_ratings(title, common_raters):
    """ Collect the all ratings of the common raters with associated titles"""
    
    rated_books = (data.user_id.isin(common_raters)) &\
                  (data.title==title)
                  
    ratings = rated_books(data.ratings).sort('user_id')
    print ratings
    
    reviews = reviews[data['user_id'].duplicated()==False]
   


# Checking the table with only the common reviewers
list_common_reviewers = []

for i in common_reviewers:
    list_common_reviewers.append(i)

# collect all book ratings by the common_raters who have also rated book 1
book_1_reviews = get_book_ratings(book_1, common_raters)
print book_1_reviews

# collect all the book ratings by the common_raters who have also rated book 2
book_2_reviews = get_book_reviews(book_2, common_raters)

# calculate pearson correlelation with scipy's pearson r module
correlation_coefficient = pearsonr(book_1_reviews.rating,
                                   book_2_reviews.rating)[0]

# # We know how they related
print correlation_coefficient