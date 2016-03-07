import pandas as pd
import csv
import codecs
import numpy as np
import numexpr

from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer

from scipy.stats.stats import pearsonr

import graphlab as gl
from graphlab import SFrame
from graphlab import ranking_factorization_recommender

# ratings = "/home/ubuntu/workspace/test-data/BX-Dump/BX-Book-Ratings.csv"
y_users = "/home/ubuntu/workspace/test-data/y_book_rating.csv"
# books = "/home/ubuntu/workspace/test-data/BX-Dump/BX-Books.csv"

# create SFrame data set from csv, only need to run once, & then work from saved model
# y_df = gl.SFrame.read_csv(y_users,
#                          delimiter=',',
#                          header=True) 
# print y_df.head()
# y_df.save('./y_book_set')

# load SFframe of youth subset of Book Crossing dataset
y_ratings_df = gl.load_sframe('./y_book_set')
(train_set, test_set) = y_ratings_df.random_split(0.8)

# rename isbn column to 'item_id',required for processing by graphlabs library
y_ratings_df.rename({'isbn': 'item_id'})

# copy of original SFrame
y_rating = y_ratings_df.copy()

# filter larger dataset for only user ratings data
user_rec_data = gl.SFrame({y_rating['user_id'], 
                          y_rating['item_id'], 
                          y_rating['rating'],
                          })

# rename columns to relevant name                           
user_rec_data.rename({'X1': 'item_id',
                      'X2': 'rating',
                      'X3': 'user_id'
                      })

# create data subset for side item processing by model
user_data = gl.SFrame({'user_id':y_rating['user_id'], 
                         'age': y_rating['age'],
                          })

########### training and testing models for accuracy testing #############                          
# 80/20 split for training and test data
# (train_set, test_set) = user_rec_data.random_split(0.8)


# # creating the model for the recommendation system
# m = gl.popularity_recommender.create(
#                                      train_set,
#                                      train_set['user_id'], 
#                                      train_set['item_id'], 
#                                      target = train_set['rating'],
#                                      )
                                     
# # baseline root mean square error calculation                                     
# baseline_rmse = gl.evaluation.rmse(
#                                   test_set['rating'], 
#                                   m.predict(test_set)
#                                   )

# regularization_vals = [0.001, 0.0001, 0.00001, 0.000001]

# # creating training model
# models = [gl.factorization_recommender.create(train_set, 'user_id', 'item_id', 'rating',
#                                               max_iterations=50, num_factors=5, regularization=r)
#           for r in regularization_vals]


# # Save the train and test RMSE, for each model
# (rmse_train, rmse_test) = ([], [])
# for m in models:
#     rmse_train.append(m['training_rmse'])
#     rmse_test.append(gl.evaluation.rmse(test_set['rating'], m.predict(test_set)))                           




##############Creating User Profiles ##########################
# pre-processing: filtering data frame to select for elementary readers and books
# elementary = y_ratings_df[(y_ratings_df['age'] <=11)]
# elementary_books = gl.SFrame([elementary['title'], elementary['item_id']])
# elementary_books.print_rows(num_rows=len(elementary))


elementary_books = ['0307121259', '0307122522', '0307302016', 
'0380703254', '0394909674', '0440414806', '0553152289', '1575840146',
 '1587288605', ' 1569315078', '0895656914', '0679808477 ']


# # filtering data frame for teen readers and books
# # teen = y_ratings_df[(y_ratings_df['age'] > 12)]
# # teen_books = gl.SFrame([elementary['title'], elementary['item_id']])
# # teen_books.print_rows(num_rows=len(elementary))


teen_books = ['0786817070', '0786845384', '0590494465' , '059035342X', 
              '0451628055', '0866119698', '1841210307', '0312367546', 
              '0679879242', '0866119698 ', '0816704651', '0439136369', 
              '0671798324']


def ratings(book_list, user, rating):
    """Create SFrame for users' data """
    num = len(book_list)
    records = {'user_id': [user] * num,
              'rating': [rating] * num,
              'item_id': book_list,
              }
    return gl.SFrame(records)

# # create young reader profile
elementary_scholar = 276726
elementary_scholar_ratings = ratings(elementary_books, 
                                     elementary_scholar,
                                     10)
elementary_scholar_ratings = elementary_scholar_ratings.append(ratings(teen_books, 
                                                                     elementary_scholar, 
                                                                      1))
elem_user = { 'age':[7.0], 'user_id':[276726],}
elem_user = gl.SFrame(elem_user)
print elem_user.dtype()
print elem_user


print user_data.dtype()
print user_data.head()
user_data.append(elem_user)

# # create teen reader profile
teen_scholar = 276727
teen_scholar_ratings = ratings(teen_books, teen_scholar, 10)
teen_scholar_ratings = teen_scholar_ratings.append(ratings(elementary_books, 
                                                           teen_scholar, 1))
teen_user = {'age':[15.0], 'user_id':[276727]}
teen_user = gl.SFrame(teen_user)
user_data.append(teen_user)

# add young and teen reader ratings to larger dataset
user_rec_data = user_rec_data.append(elementary_scholar_ratings)

# # training model with data, only need to run once. save & work from loaded model later
# m2 = gl.ranking_factorization_recommender.create(user_rec_data,
#                                                 # 'item_id', 
#                                                 target = 'rating', 
#                                                 user_data = user_data,
#                                                 max_iterations=50,
#                                                 num_factors=5,
#                                                 regularization=0.00001)


# m2 = m2.save("m2")

# loading model from memory
m2 = gl.load_model('m2')

# make recommendation based on user profile, nearest-k similar items
teen_recommendations = m2.recommend(users=[276727], k=10)
print teen_recommendations

elem_recommendations = m2.recommend(users=[276726], k=10)
print elem_recommendations

# top recommendations, based a new user with no rated items
top_rec = m2.recommend(users=[276728],k=10)
print top_rec

#### more testing of recommenations #####
# sim_books = m2.get_similar_items(items=elementary_books, k=10)
# print sim_books

# readers = m2.get_similar_users(276727, k=20)
# print readers

# # summary statistics and details about recommendation model
print m2.summary()


