import json

# initialize dictionaries to encode users and businesses
users_encoder = {}
business_encoder = {}

# read in the businesses in Philadelphia
philadelphia_businesses = set()
with open('yelp_academic_dataset_business.json') as f:
    for line in f:
        business = json.loads(line)
        if business['city'] == 'Philadelphia':
            philadelphia_businesses.add(business['business_id'])

# initialize the adjacency list
adj_list = []
# count = 0
# read in the reviews and update the adjacency list and encoder dictionaries
with open('yelp_academic_dataset_review.json') as f:
    for line in f:
        review = json.loads(line)
        if review['business_id'] in philadelphia_businesses:
            user_id = review['user_id']
            business_id = review['business_id']
            # encode user_id and business_id
            if user_id not in users_encoder:
                users_encoder[user_id] = len(users_encoder)
                adj_list.append([])
            if business_id not in business_encoder:
                business_encoder[business_id] = len(business_encoder)
            # update the adjacency list
            user_index = users_encoder[user_id]
            business_index = business_encoder[business_id]
            adj_list[user_index].append(business_index)
            # count += 1
            # if count == 10000:
            #     break

with open('yelp_academic_dataset_tip.json') as f:
    for line in f:
        tip = json.loads(line)
        if tip['business_id'] in philadelphia_businesses:
            user_id = tip['user_id']
            business_id = tip['business_id']
            # encode user_id and business_id
            if user_id not in users_encoder:
                users_encoder[user_id] = len(users_encoder)
                adj_list.append([])
            if business_id not in business_encoder:
                business_encoder[business_id] = len(business_encoder)
            # update the adjacency list
            user_index = users_encoder[user_id]
            business_index = business_encoder[business_id]
            adj_list[user_index].append(business_index)
import os

# create yelp2018 directory if it doesn't exist
if not os.path.exists('yelp2018'):
    os.makedirs('yelp2018')

# write user_list.txt
with open('yelp2018/user_list.txt', 'w') as f:
    for user, user_num in users_encoder.items():
        f.write(f"{user} {user_num}\n")

# write item_list.txt
with open('yelp2018/item_list.txt', 'w') as f:
    for item, item_num in business_encoder.items():
        f.write(f"{item} {item_num}\n")

# write train.txt and test.txt
num_users = len(users_encoder)
train_size = int(0.8 * num_users)

with open('yelp2018/train.txt', 'w') as train_f, open('yelp2018/test.txt', 'w') as test_f:
    for i, adj_row in enumerate(adj_list):
        user_num = i
        adj_items = ' '.join(map(str, adj_row))
        if i < train_size:
            train_f.write(f"{user_num} {adj_items}\n")
        else:
            test_f.write(f"{user_num} {adj_items}\n")
