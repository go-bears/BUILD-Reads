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
    """Open BX-Books.csv separating on semi-colons, set datatype, set headers."""
    
    # open csv and format dataframe
    books_df = pd.read_csv('BX-Dump/BX-Books.csv',
                     sep=';',
                     dtype=object,
                     header=None,
                     names=["isbn","title", "author", "year", "publisher",
                            "image-sm link","image-md link", "image-lg link"])
    
    return books_df

def open_ratings_csv():
    """Open BX-Book-Ratings.csv separate on semi-colons, set datatype, set headers."""
    
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
    """ Merges of user_ratings and books dataframes"""
    
    # Merges User_Ratings and book dataframes on left join
    User_Ratings_Books = pd.merge(User_Ratings_df,
                         books_df,
                         left_on='isbn',
                         right_on='isbn',
                         sort=True)
    
    return User_Ratings_Books
    

def generate_youth_book_ratings(merged_df):
    """Filter query to limit results to ages 3-18, with ratings > 0."""

    y_user_book_ratings_df = User_Ratings_Books[(User_Ratings_Books['age'] > 3) &
            (User_Ratings_Books['age']< 19) &
            (User_Ratings_Books['rating'] > 0)]
 
    return y_user_book_ratings_df


def parse_countries(dataframe):
    """Parses location string into city, state, country; returns list of tuples."""
    
    dataframe = y_user_book_ratings_df
    locations = dataframe['location'].tolist()
    # print locations
    parsed_loc_list = []
    for locate in locations:
        place = locate.split(',')
        city = place[0].strip()
        state = place[1].strip()
        country = place[2].strip()
        
        parsed_loc_list.append((city, state, country))
    
    
    return parsed_loc_list


def count_countries(parsed_loc):
    """Counts readers per country."""
    
    country_count= {}
    for loc_tuple in parsed_loc_list:
        city, state, country = loc_tuple
        if country not in country_count:
            country_count[country] = 1
        elif country == 'wisconsin':
            country_count['usa'] += 1
        elif country == 'dc':
            country_count['usa'] += 1
        elif country == 'califronia':
            country_count['usa'] += 1
            
        else:
            country_count[country] += 1
    
   
    return country_count
    
def count_states(parsed_loc):
    """Count number of readers in each state."""
    
    states_dict = {}
    for loc_tuple in parsed_loc_list:
        city, state, country = loc_tuple
        
        for count in country:
            if country == 'usa':
                if state not in states_dict:
                    states_dict[state] = 1
                else:
                    states_dict[state] += 1
           # if statements to handle some malformed entries
            elif country == 'wisconsin':
                    states_dict['wisconsin'] += 1
            elif country == 'california':
                states_dict['california'] += 1
            elif country == 'dc':
                if 'dc' not in states_dict:
                    states_dict['dc'] = 1
                else:
                    states_dict['dc'] += 1
                    
    
    return states_dict

def count_CA(parsed_loc):
    """Count readers in different CA cities """
    
    CA_dict = {}
    for loc_tuple in parsed_loc_list:
        city, state, country = loc_tuple
        if state == 'california':
            if city not in CA_dict:
                CA_dict[city] = 1
            else:
                CA_dict[city] = 1
            
    return CA_dict
    
    


################## run all the preprocessing functions  ############
users_df = open_users_csv()
ratings_df = open_ratings_csv()
books_df = open_books_csv()
User_Ratings_df = merge_user_ratings(users_df, ratings_df)
User_Ratings_Books = merge_userratings_books(User_Ratings_df, books_df)
y_user_book_ratings_df = generate_youth_book_ratings(User_Ratings_Books)
parsed_loc_list = parse_countries(y_user_book_ratings_df)
count_countries(parsed_loc_list)
count_states(parsed_loc_list)
count_CA(parsed_loc_list)

# y_user_book_ratings_df features: ratings are 1-10
# produces 13554 entries, mean age: 15, mean rating: 7.66


# ############ data exploration with pandas below #######################
# groups by title and displays mean and sample rating size for each title
# top = y_user_book_ratings_df.groupby('title').agg({'rating': [np.size, np.mean]})
# print top.sort([('rating', 'mean')], ascending=False).head()
# 
# 
# groups data by age
# age_group = y_user_book_ratings_df.groupby('age')
# print age_group.head()
# print age_group.describe()

# top 25 most rated books
# most_rated = y_user_book_ratings_df.groupby('title').size().sort_values(ascending=False)[:25]
# print most_rated

#counts how many ratings each book received
# print y_suser_book_ratings_df.title.value_counts() #[:25]

# finds sample size and mean of book ratings and selects 20 highest mean scores
# mean_rating = y_user_book_ratings_df.loc[:,['rating',
                                                # 'title']].groupby('title').agg({'rating':[np.size,
                                                                                    #   np.mean]})
# print y_user_book_ratings_df.loc['isbn','title'].head()
# print y_user_book_ratings_df.head() 
# print mean_rating
# print mean_rating.sort([('rating', 'mean')], ascending=False).head()


# filter for books with rating:size with more than 10 ratings
# atleast_3 = mean_rating['rating']['size'] >= 3
# print atleast_3.describe()
# produces 698 entries


# print top 20 scores with rating sample size > 3
# print mean_rating[atleast_3].sort([('rating', 'mean')], ascending=False).head(20)

# converts dataframe to csv file
# y_user_book_ratings_df.to_csv('y_book_rating.csv')

# most_50 = atleast_3.groupby('title').size().order(ascending=False)[:50]
# print most_50