import json
import os

from django.conf import settings

from feedbacks.constants import (PIPELINE_FILE_RELATIVE_PATH,
                                 FEEDBACK_COLLECTION_NAME)


class MongoService:
    def get_db(self):
        return settings.MONGO_DB
    
    def get_collection(self, collection_name):
        db = self.get_db()
        return db[collection_name]
    
    def get_all_data(self, collection_name):
        collection = self.get_collection(collection_name)
        result = collection.find()
        return result
    
    def get_feedback_data(self):
        return self.get_all_data(FEEDBACK_COLLECTION_NAME)

    def _get_file_path(self, relative_path):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, relative_path)
        file_path = os.path.abspath(file_path)
        return file_path

    def get_branch_services_scores_data(self):
        file_path = self._get_file_path(PIPELINE_FILE_RELATIVE_PATH)

        with open(file_path, "r") as file:
            content = file.read()
            pipelines = json.loads(content)
            feedback_collection = self.get_collection(FEEDBACK_COLLECTION_NAME)
            result = list(feedback_collection.aggregate(pipelines))
            return result
