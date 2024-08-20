import json
import os

from pymongo import MongoClient

from feedbacks.constants import (PIPELINE_FILE_RELATIVE_PATH,
                                 FEEDBACK_COLLECTION_NAME,
                                 SEEDING_FILE_RELATIVE_PATH)


class MongoService:
    def __init__(self):
        MONGO_DB_HOST = os.getenv('MONGO_DB_HOST', 'localhost')
        MONGO_DB_PORT = os.getenv('MONGO_DB_PORT', 27017)
        MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'dev')

        self.mongo_client = MongoClient(
            host=MONGO_DB_HOST,
            port=int(MONGO_DB_PORT),
        )

        self.db = self.mongo_client[MONGO_DB_NAME]
    
    def get_collection(self, collection_name):
        """
        Fetches collection with specified collection name
        """
        return self.db[collection_name]
    
    def get_all_data(self, collection_name):
        """
        Fetches all data from specified collection name
        """
        collection = self.get_collection(collection_name)
        result = collection.find()
        return list(result)
    
    def get_feedback_data(self):
        """
        Fetches all feedback data
        """
        return self.get_all_data(FEEDBACK_COLLECTION_NAME)

    def _get_file_path(self, relative_path):
        """
        Returns absolute path from given relative path
        """
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, relative_path)
        file_path = os.path.abspath(file_path)
        return file_path

    def get_branch_services_scores_data(self):
        """
        Fetches score data based on aggregation pipelines.
        Returns list of dictionaries (with the keys "brach_name", "services")
        """
        file_path = self._get_file_path(PIPELINE_FILE_RELATIVE_PATH)
        pipelines  = self._get_json_file_content(file_path)
        feedback_collection = self.get_collection(FEEDBACK_COLLECTION_NAME)
        result = list(feedback_collection.aggregate(pipelines))
        return result
    
    def _get_json_file_content(self, file_path):
        """
        Reads the json file in the given location and
        returns native python content data of the file
        """
        with open(file_path, "r") as file:
            content = file.read()
            data = json.loads(content)
            return data

    def seed_data(self, collection_name):
        """
        Inserts many documents to the specified collection in one go
        """
        file_path = self._get_file_path(SEEDING_FILE_RELATIVE_PATH)
        data = self._get_json_file_content(file_path)
        collection = self.get_collection(collection_name)
        collection.insert_many(data)

    def seed_feedback_data(self):
        """
        Insert many documents into feedback collection
        """
        self.seed_data(FEEDBACK_COLLECTION_NAME)
