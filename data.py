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

# y_rec_model = gl.recommender.create(y_ratings_df,
#                                     user_id='user_id',
#                                     item_id='title',
#                                     target='rating')
                                
# y_rec_model_saved = y_rec_model.save("y_rec_model")

y_rec_model=gl.load_model('y_rec_model')

# this works!!
# y_recs = y_rec_model.recommend()
# print y_recs

# list of 3 amelia bedelia books &  1 richard scarry
my_list_of_items =['0064440192', '0064442055', '038049171', '0307157857']

similar_items = y_rec_model.get_similar_items(my_list_of_items, k=10)
print similar_items.print_rows(num_rows=40)

y_popular_model = gl.popularity_recommender.create(y_rec_model)
print y_popular_model.PopularityRecommender.predict(y_popular_model)

# item_similarity_recommender.create

# m2 = gl.factorization_recommender.create(y_rec_model, target='rating')
                                         
# m2_save = m2.save("m2")
# print m2_save.recommend()
