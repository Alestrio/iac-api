#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import pymongo as pymongo
import yaml


class UserDb:
    def __init__(self):
        with open('./config/app_config/app.yaml', 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
            mongo_addr = self.config['mongo_addr']
            mongo_port = self.config['mongo_port']
            mongo_user = self.config['mongo_user']
            mongo_pass = self.config['mongo_pass']
            mongo_db_name = self.config['mongo_db_name']

            mongo_connection_string = 'mongodb://' + mongo_user + ':' + mongo_pass + '@' + mongo_addr + ':' + mongo_port
            self.client = pymongo.MongoClient(mongo_connection_string)
            self.database = self.client[mongo_db_name]
            self.collection = self.database['users']

    def get_all_users(self):
        return self.collection.find()

    def get_user_by_username(self, username):
        return self.collection.find_one({'username': username})

    def get_user_by_email(self, username):
        return self.collection.find_one({'email': username})

    def get_user_by_id(self, user_id):
        return self.collection.find_one({'_id': user_id})

    def update_user(self, user_id, user):
        self.collection.update_one({'username': user_id}, {'$set': user})

    def add_user(self, user):
        self.collection.insert_one(user.dict())

    def delete_user(self, username):
        self.collection.delete_one({'username': username})
