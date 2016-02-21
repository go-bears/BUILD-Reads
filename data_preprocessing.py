# import pandas library
import pandas as pd
import csv
import codecs
import numpy as np
import numexpr

"""Preprocessing Book Crossing Dataset to select youth age range"""

def open_users_csv():
    """Open csv separating on semi-colons, set headers."""
    
    # open csv and format dataframe
    users_df = pd.read_csv('BX-Dump/BX-Users.csv',
                           sep=';',
                           header=None,
                           names=["user_id","location","age"])

    # type cast age to numeric value, strings are coereced to NaaN ('not a number')
    users_df['age'] = pd.to_numeric(users_df['age'], errors='coerce')

    return users_df


def open_books_csv():
    """Open csv separating on semi-colons, set datatype, set headers."""
    
    # open csv and format dataframe
    books_df = pd.read_csv('BX-Dump/BX-Books.csv',
                     sep=';',
                     dtype=object,
                     header=None,
                     names=["isbn","title", "author", "year", "publisher",
                            "image-sm link","image-md link", "image-lg link"])
    
    return books_df

def open_ratings_csv():
    """Open csv separating on semi-colons, set datatype, set headers."""
    
    # open csv and format dataframe
    ratings_df = pd.read_csv('BX-Dump/BX-Book-Ratings.csv',
                     sep=';',
                     header=None,
                     names=["user_id","isbn", "rating"])

    # change ratings column to number from string        
    ratings_df['rating'] = pd.to_numeric(ratings_df['rating'])
    
    return ratings_df


def merge_user_ratings(df1, df2):
    """ Merges of users and ratings dataframes"""
    
    # merges user and ratings dataframe on left join
    User_Ratings_df= pd.merge(users_df, ratings_df,
                            left_on='user_id',
                            right_on='user_id',
                            sort=True, 
                            indicator=True,
                            )
    return User_Ratings_df
    

def merge_userratings_books(df1, df2):
    """ Merges of user_ratings and dataframes"""
    
    # Merges User_Ratings and book dataframes on left join
    User_Ratings_Books = pd.merge(User_Ratings_df,
                         books_df,
                         left_on='isbn',
                         right_on='isbn',
                         sort=True)
    
    return User_Ratings_Books
    



def generate_youth_book_ratings(merged_df):
    """Filter query to limit results to ages 3-18, with ratings >0"""

    y_user_book_ratings_df = User_Ratings_Books[(User_Ratings_Books['age'] > 3) &
            (User_Ratings_Books['age']< 19) &
            (User_Ratings_Books['rating'] > 0)]
 
    return y_user_book_ratings_df


################## run all the preprocessing functions  ############
users_df = open_users_csv()
ratings_df = open_ratings_csv()
books_df = open_books_csv()
User_Ratings_df = merge_user_ratings(users_df, ratings_df)
User_Ratings_Books = merge_userratings_books(User_Ratings_df, books_df)
y_user_book_ratings = generate_youth_book_ratings(User_Ratings_Books)

# ratings are 1-10
# produces 13554 entries, mean age: 15, mean rating: 7.66

