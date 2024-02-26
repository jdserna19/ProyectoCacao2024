import pymongo
from bson.objectid import ObjectId
import datetime


class MongoDBCommunication:
    def __init__(self, mongodb_host, mongodb_port):
        # Establishes the connection to the DB.
        self.mongodb_client = pymongo.MongoClient(host=mongodb_host, port=mongodb_port)

    def get_db_collection(self, db_name, db_collection):
        """Returns the required DB collection."""
        db = self.mongodb_client[db_name]
        return db[db_collection]

    def insert_document(self, db_collection, document):
        """Inserts the given document into the given DB collection."""
        inserted_document = db_collection.insert_one(document)
        document_id = inserted_document.inserted_id
        return document_id

    def insert_document_list(self, db_collection, document_list):
        """Inserts the given documents into the given DB collection."""
        inserted_documents = db_collection.insert_many(document_list)
        document_ids = inserted_documents.inserted_ids
        return document_ids

    def count_documents_in_db_collection(self, db_collection):
        """Counts the number of documents in the given DB collection."""
        return db_collection.count()

    def find_first(self, db_collection):
        """Finds the first record in the given DB collection."""
        return db_collection.find_one()

    def find_document_by_id(self, db_collection, document_id_as_string):
        """Converts id from string into ObjectId and gets the query's result."""
        result = db_collection.find_one({"_id": ObjectId(document_id_as_string)})
        return result

    def find_all(self, db_collection):
        """Returns all documents in the given DB collection."""
        return db_collection.find()

    def get_documents_btw_timestamps(self, db_collection, timestamp_1_array, timestamp_2_array):
        """
        Looks for the documents between the two given timestamps and sorts them by the timestamp field in ascendant
        order.
        """
        timestamp_1 = datetime.datetime(day=timestamp_1_array[0], month=timestamp_1_array[1], year=timestamp_1_array[2],
                                        hour=timestamp_1_array[3], minute=timestamp_1_array[4],
                                        second=timestamp_1_array[5])
        timestamp_2 = datetime.datetime(day=timestamp_2_array[0], month=timestamp_2_array[1], year=timestamp_2_array[2],
                                        hour=timestamp_2_array[3], minute=timestamp_2_array[4],
                                        second=timestamp_2_array[5])
        # Converts the datetime from Eastern time into UTC adding 5 hours to it.
        timestamp_1 = timestamp_1.replace(hour=timestamp_1.hour + 5)
        timestamp_2 = timestamp_2.replace(hour=timestamp_2.hour + 5)
        return db_collection.find({"timestamp": {"$gte": timestamp_1, "$lt": timestamp_2}}).sort("timestamp")

    def update_document(self, db_collection, document_id, update):
        """Updates the document that has the given document id with the given update information."""
        db_collection.update_one({"_id": document_id}, {"$set": update})
        updated_document = db_collection.find_one({"_id": document_id})
        # Returns the document after updating it.
        return updated_document

    def delete_document(self, db_collection, document_id):
        """
        Deletes the document that has the given document id and returns whether it was successfully deleted or not.
        """
        db_collection.delete_one({"_id": document_id})
        is_document_deleted = False
        if db_collection.find_one({"_id": document_id}) is None:
            # A document with the given document id was not found.
            is_document_deleted = True
        return is_document_deleted
