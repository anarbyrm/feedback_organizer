from django.conf import settings


class MongoService:
    def get_db(self):
        return settings.MONGO_DB
    
    def get_collection(self, collection_name):
        return settings.MONGO_DB[collection_name] 

    def get_all_feedbacks(self):
        feedback_collection = self.get_collection('feedbacks')
        feedbacks = feedback_collection.find()
        return feedbacks
    