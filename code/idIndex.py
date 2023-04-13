
class UserQuery:
    def __init__(self, user_file_path):
        self.user_dict = {}
        with open(user_file_path, 'r') as f:
            for line in f:
                user_id, user_num = line.strip().split()
                self.user_dict[user_id] = int(user_num)
    
    def get_user_num(self, user_ids):
        user_nums = []
        for user_id in user_ids:
            if user_id in self.user_dict:
                user_nums.append(self.user_dict[user_id])
            else:
                user_nums.append(None)
        return user_nums
    
    def get_user_id(self, user_nums):
        user_ids = []
        for user_id, num in self.user_dict.items():
            if num in user_nums:
                user_ids.append(user_id)
        return user_ids


class ItemQuery:
    def __init__(self, item_file_path):
        self.item_dict = {}
        with open(item_file_path, 'r') as f:
            for line in f:
                item_id, item_num = line.strip().split()
                self.item_dict[item_id] = int(item_num)
    
    def get_item_num(self, item_ids):
        item_nums = []
        for item_id in item_ids:
            if item_id in self.item_dict:
                item_nums.append(self.item_dict[item_id])
            else:
                item_nums.append(None)
        return item_nums
    
    def get_item_id(self, item_nums):
        item_ids = []
        for item_id, num in self.item_dict.items():
            if num in item_nums:
                item_ids.append(item_id)
        return item_ids

if __name__ == '__main__':
    user_query = UserQuery('data/yelp2018/user_list.txt')
    user_num = user_query.get_user_num(['smOvOajNG0lS4Pq7d8g4JQ'])
    print(user_num)
    user_id = user_query.get_user_id([228483, 228484])
    print(user_id)

    item_query = ItemQuery('data/yelp2018/item_list.txt')
    item_num = item_query.get_item_num(['RZtGWDLCAtuipwaZ-UfjmQ'])
    print(item_num)
    item_id = item_query.get_item_id([3,4,5])
    print(item_id)

    