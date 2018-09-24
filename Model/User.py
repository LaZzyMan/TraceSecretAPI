import pymongo
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify

class User:
    def get_coll(self, name):
        db = self.client.TraceSecret
        coll = db[name]
        return coll

    def __init__(self, json):
        self.client = pymongo.MongoClient()
        self.json = json
        self.username = json['username']
        self.password = json['password']
        # 0:unkown;1:logined;2:register
        self.state = 0
        self.coll = self.get_coll('User')

    def login(self):
        user = self.coll.find_one({'username': self.username})
        if not user:
            return {'state': 1}
        elif not check_password_hash(user['password'], self.password):
            return {'state': 2}
        else:
            self.state = 1
            return {'state': 0,
                    'result': {'id': user['uuid'],
                               'email': user['email' ],
                               'registerTime': user['registerTime']}
                    }

    def register(self):
        user = self.coll.find_one({'username': self.username})
        if not user:
            self.coll.insert_one({'username': self.username,
                                  'password': generate_password_hash(self.password),
                                  'id': self.json['id'],
                                  'email': self.json['email'],
                                  'registerTime': self.json['registerTime']
                                  })
            self.state = 2
            self.client.close()
            return {'state': 0}
        else:
            return {'state': 1}

