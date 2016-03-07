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

# # convert csv to graph labs dataframe
# ratings_df = gl.SFrame.read_csv(ratings,
#                          delimiter=';',
#                          header=False,
#                          column_type_hints={'X2':str, 'X3': int}) 
                         
# # rename columns from default values to explict values
# ratings_df.rename({'X1':'user_id', 'X2':'isbn', 'X3':'rating'})

# # save ratings Sframe 
# ratings_df.save('./book_data')

# load Sframe created in lines 19-29
# ratings_df = gl.load_sframe('./book_data')

# selects out user_id  for it's own dataframe
# users = ratings_df['user_id']

# passes ratings_df into recommender.create() engine
# rec_model = gl.recommender.create(ratings_df,
#                               user_id="user_id",
#                               item_id="isbn",
#                               target="rating")

# print rec_model.summary()
# rec_model.save("rec_model")

# loads saved model
# loaded_model = gl.load_model('rec_model')

# will load higest ranking books for any new user as default
# print loaded_model.recommend([276724])
# m = gl.item_similarity_recommender.create(ratings_df,
#                                           user_id='user_id',
#                                           item_id='isbn',
#                                           target='rating',
#                                           similarity_type='jaccard')
# # Get 20 recommendations for each user in your list of users.

# save the model that was created by rececommender.create()
# m.save('model-m')

# ratings_df = gl.SFrame.read_csv(y_ratings,
#                          delimiter=';',
#                          header=True) 


# rec_model = model.save("rec_model")

# recs = rec_model.recommend(users, k=20)

# y_df = gl.SFrame.read_csv(y_users,
#                          delimiter=',',
#                          header=True) 
# print y_df.head()
# y_df.save('./y_book_set')


y_ratings_df = gl.load_sframe('./y_book_set')
(train_set, test_set) = y_ratings_df.random_split(0.8)

y_ratings_df.rename({'isbn': 'item_id'})

y_rating = y_ratings_df.copy()




user_rec_data = gl.SFrame({y_rating['user_id'], 
                          y_rating['item_id'], 
                          y_rating['rating'],
                          })
                          
user_rec_data.rename({'X1': 'item_id',
                      'X2': 'rating',
                      'X3': 'user_id'
                      })

user_data = gl.SFrame({'user_id':y_rating['user_id'], 
                         'age': y_rating['age'],
                          })
                          
# user_rec_data.rename({'X1': 'age',
#                       'X2': 'user_id'
#                       })
                          
# 80/20 split for training and test data
(train_set, test_set) = user_rec_data.random_split(0.8)


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





# # filtering data fraom for elementary readers and books
# # elementary = y_ratings_df[(y_ratings_df['age'] <=11)]
# # elementary_books = gl.SFrame([elementary['title'], elementary['item_id']])
# # elementary_books.print_rows(num_rows=len(elementary))


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
teen_scholar_ratings = teen_scholar_ratings.append(ratings(elementary_books, teen_scholar, 1))
teen_user = {'age':[15.0], 'user_id':[276727]}
teen_user = gl.SFrame(teen_user)
user_data.append(teen_user)

# # # add young and teen reader ratings to larger dataset
user_rec_data = user_rec_data.append(elementary_scholar_ratings)
# user_rec_data.print_rows(num_rows=40)
# user_rec_data = user_rec_data.append(teen_scholar_ratings)
print user_rec_data.dtype()
print user_rec_data.head()

# # training model with data, only need to run once and then save.
# m2 = gl.ranking_factorization_recommender.create(user_rec_data,
#                                                 # 'item_id', 
#                                                 target = 'rating', 
#                                                 user_data = user_data,
#                                                 max_iterations=50,
#                                                 num_factors=5,
#                                                 regularization=0.00001)

# m2 = m2.save("m2")

m2 = gl.load_model('m2')

# print elementary_scholar
# # 276726

# # print gl.SFrame(elementary_scholar['item_id'])

# # print gl.SArray([elementary_scholar_ratings])
# # print gl.SArray(elementary_scholar['item_id'])
teen_recommendations = m2.recommend(users=[276727], k=10)
print teen_recommendations

elem_recommendations = m2.recommend(users=[276726], k=10)
print elem_recommendations

top_rec = m2.recommend(users=[276728],k=10)
print top_rec
# sim_books = m2.get_similar_items(items=elementary_books, k=10)
# print sim_books

# readers = m2.get_similar_users(276727, k=20)
# print readers

# # print elem_recommendations['elementary_books']
print m2.summary()
# # print elem_recommendations.summary()
# m2.recommend(gl.SArray(elementary_scholar), k=20)

# print elem_recommendations

# teen_recommendations = m2.recommend(gl.SArray([teen_scholar]), k=10)
# print teen_recommendations['item_id']


