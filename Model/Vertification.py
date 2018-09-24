from pymongo import MongoClient
import random
class Vertification:
    def __init__(self):
        client = MongoClient()
        self.correctColl = client.TraceSecret.StayPoint
        self.confuseColl = client.TraceSecret.ConfusePoint

    def getQuestion(self, id):
        correctNum = random.randint(1, 5)
        corrList = list(self.correctColl.find({'user': id}))
        confuseList = list(self.confuseColl.find({}))
        corr = random.sample(corrList, correctNum)
        confuse = random.sample(confuseList, 9-correctNum)
        corrQ = [c['url'] for c in corr]
        confuseQ = [c['url'] for c in confuse]
        return {'state': 0, 'corr':corrQ, 'confuse': confuseQ}