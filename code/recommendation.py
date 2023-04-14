# Use models to make predictions about customers' preferences
import world
import utils
from world import cprint
import torch
import numpy as np
from os.path import join
import register
from register import dataset
from idIndex import UserQuery, ItemQuery
import pandas as pd
from scipy.sparse import csr_matrix
from pandas.api.types import CategoricalDtype
import matplotlib as plt
import matplotlib.pyplot as plt
from surprise import SVD
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import cross_validate

def recommend_restaurant(UID, num):
    # Load the model from checkpoint
    Recmodel = register.MODELS[world.model_name](world.config, dataset)
    Recmodel = Recmodel.to(world.device)
    bpr = utils.BPRLoss(Recmodel, world.config)

    # load the user and item query
    user_query = UserQuery('../data/yelp2018/user_list.txt')
    item_query = ItemQuery('../data/yelp2018/item_list.txt')

    weight_file = utils.getFileName()
    print(f"load and save to {weight_file}")

    Recmodel.load_state_dict(torch.load(weight_file,map_location=torch.device('cpu')))
    world.cprint(f"loaded model weights from {weight_file}")

    # Get the user id you want to make recommendations for
    user_id = [UID]
    # Get the top 50 recommendations for each user
    top_k = num
    users_number = user_query.get_user_num(user_id)
    users_number = torch.LongTensor(users_number)
    users_number = users_number.to(world.device)
    scores = Recmodel.getUsersRating(users_number)
    scores = scores.cpu().detach().numpy()
    top_k_items = np.argsort(-scores, axis=1)[:, :top_k]
    top_k_items_id = []
    #for i in range(len(user_id)):
    #print(f"Recommendations for {user_id}")
    top_k_items_id.append(item_query.get_item_id(top_k_items))
    for i in range(len(user_id)):
        #print(f"Recommendations for {user_id[i]}")
        top_k_items_id.append(item_query.get_item_id(top_k_items[i]))
        #for j in range(top_k):
        #    print(f"restaurant{j+1}:    {top_k_items_id[i][j]}")
    return top_k_items_id[0]

def recommend_hotel(UID,num):
    # Load in the data
    business = pd.read_csv('../output_csv/business_PA_Philly_clean.csv')
    review = pd.read_csv('../output_csv/review_PA_Philly_clean.csv')

    business = business[['business_id','name']]
    #Building Rating Matrix
    user_u = list(sorted(review.user_id.unique()))
    business_u = list(sorted(review.business_id.unique()))

    cat_type_user = CategoricalDtype(categories=user_u, ordered=True)
    cat_type_business = CategoricalDtype(categories=business_u, ordered=True)

    row = review.user_id.astype(cat_type_user).cat.codes
    col = review.business_id.astype(cat_type_business).cat.codes

    data = review['stars'].tolist()

    sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(business_u)))
    ratings = pd.DataFrame.sparse.from_spmatrix(sparse_matrix,index=user_u, columns=business_u)
    ratings.fillna(0, inplace = True)

    def matrix_factorization(R, P, Q, K, steps=10, alpha=0.0002, beta=0.02):
        '''
        Inputs:
        R     : The ratings (of dimension M x N)
        P     : an initial matrix of dimension M x K
        Q     : an initial matrix of dimension N x K
        K     : the number of latent features
        steps : the maximum number of steps to perform the optimization
        alpha : the learning rate
        beta  : the regularization parameter

        Outputs:
        the final matrices P and Q
        '''

        for step in range(steps):
            for i in range(R.shape[0]):
                for j in range(R.shape[1]):
                    if R[i][j] > 0: # Skipping over missing ratings
                        #Calculating error
                        eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                        for k in range(K):
                            # calculate gradient with alpha and beta parameter
                            P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                            Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
            eR = np.dot(P,Q)
            e = 0
            for i in range(R.shape[0]):
                for j in range(R.shape[1]):
                    if R[i][j] > 0:
                        e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                        for k in range(K):
                            e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
            if e < 0.001: # tolerance
                break
        print(e)
        return P, Q

    np.random.seed(862)

    # Initializations
    M = ratings.shape[0] # Number of users
    N = ratings.shape[1] # Number of items
    K = 3 # Number of latent features

    # Initial estimate of P and Q
    P = np.random.rand(M,K)
    Q = np.random.rand(K,N)
    rating_np = np.array(ratings)

    P, Q = matrix_factorization(rating_np, P, Q, K)

    predicted_rating = np.matmul(P, Q)
    predicted_rating = pd.DataFrame(predicted_rating, index = ratings.index, columns = ratings.columns)

    # Obtain the missing ratings
    missing_ratings = predicted_rating.loc[UID][ratings.loc[UID,:]==0]

    # Attach it with indices
    missing_ratings = pd.Series(missing_ratings, index = ratings.columns[ratings.loc[UID,:] == 0] )

    # Sort the ratings
    missing_ratings.sort_values(ascending = False, inplace = True)

    # Recommendations
    mat_fact = []
    for i in range(num):
        rec_rest_id = missing_ratings.index[i]
        mat_fact.append(rec_rest_id)
        #mat_fact.append(business[business['business_id'] == rec_rest_id]['name'].values[0])
        #print("my number ", i+1, " recommendation is ", business[business['business_id'] == rec_rest_id]['name'].values[0], 
        #    ", with a predicted rating of", missing_ratings.iloc[i])
    #print(mat_fact) 
    return mat_fact

def recommend_tour(UID,num):
    # Load in the data
    business = pd.read_csv('../output_csv/business_PA_Philly_clean_tour.csv')
    review = pd.read_csv('../output_csv/review_PA_Philly_clean_tour.csv')

    review = review.drop(columns = ['review_id','year'])
    business = business[['business_id','name']]
    user_u = list(sorted(review.user_id.unique()))
    business_u = list(sorted(review.business_id.unique()))

    cat_type_user = CategoricalDtype(categories=user_u, ordered=True)
    cat_type_business = CategoricalDtype(categories=business_u, ordered=True)

    row = review.user_id.astype(cat_type_user).cat.codes
    col = review.business_id.astype(cat_type_business).cat.codes

    data = review['stars'].tolist()

    sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(business_u)))
    ratings = pd.DataFrame.sparse.from_spmatrix(sparse_matrix,index=user_u, columns=business_u)
    ratings.fillna(0, inplace = True)

    # Step 1: Set up the reader class
    #reader = Reader(rating_scale=(1,5))
    reader = Reader(line_format='user item rating', rating_scale=(1, 5))
    # Step 2: Load the dataframe. Use the merged data from above (not the pivoted data)
    data = Dataset.load_from_df(review, reader)
    # Use the famous SVD algorithm.
    algo = SVD()
    # Run 5-fold cross-validation and print results.
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    svd_data = data.build_full_trainset()
    
    # Set up the model and fit the model. Note it will take a few minutes to run
    svd = SVD(n_factors = 7, lr_all = 0.01, reg_all = 0.1, biased = True,verbose = True, random_state = 862)
    svd.fit(svd_data)
    # First we need to obtain the ids of the unvisited restaurants. 
    unread_ids = ratings.columns[ratings.loc[UID,:] == 0]

    # Now we will loop over the restaurants to extract the predictions
    svd_rec = []
    for iid in unread_ids:
        svd_rec.append(svd.predict(uid=UID,iid=iid).est)

    # Put the result in a pd Series and sort
    svd_rec = pd.Series(svd_rec, index = unread_ids).sort_values(ascending=False)
    # Recommendations
    svd_pp = []
    for i in range(num):
        rec_rest_id = svd_rec.index[i]
        svd_pp.append(rec_rest_id)
    return svd_pp




if __name__ == '__main__':
    restaurant_ID = recommend_restaurant('vrKkXsozqqecF3CW4cGaVQ',100)
    print(restaurant_ID)
    tour_ID = recommend_tour('vrKkXsozqqecF3CW4cGaVQ',10)
    print(tour_ID)
    hotel_ID = recommend_hotel('MIUELcIEodpQuSMtwyKayA',10)
    print(hotel_ID)