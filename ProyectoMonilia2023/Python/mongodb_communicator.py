import pymongo
from bson.objectid import ObjectId
import datetime as dt
from time import sleep


class MongoDBCommunicator:
    ATTEMPTS_TIMEOUT = 60
    INTERVAL_BTW_ATTEMPTS = 5
    MONGODB_CONNECTION_TIMEOUT = 5000
    UTC_OFFSET_FROM_LOCAL_TIMEZONE = 5

    def __init__(self, mongodb_host, mongodb_port):
        # Saves the data to establish the connection to the DB.
        self.mongodb_host = mongodb_host
        self.mongodb_port = mongodb_port
        self.mongodb_client = None

    def get_db_collection(self, db_name, collection):
        """Returns the required DB collection."""
        try:
            self.mongodb_client = pymongo.MongoClient(host=self.mongodb_host, port=self.mongodb_port,
                                                      socketTimeoutMS=self.MONGODB_CONNECTION_TIMEOUT,
                                                      connectTimeoutMS=self.MONGODB_CONNECTION_TIMEOUT,
                                                      serverSelectionTimeoutMS=self.MONGODB_CONNECTION_TIMEOUT)
            db_collection = self.mongodb_client[db_name][collection]
        except:
            self.close_db_connection()
            db_collection = None
            print("The DB collection could not be retrieved.")
        return db_collection

    def close_db_connection(self):
        """Closes the connection to the DB."""
        if self.mongodb_client is not None:
            self.mongodb_client.close()

    def insert_document(self, db_name, collection, document, timestamp):
        """Inserts the given document into the given DB collection."""
        # Adds the timestamp to the given document.
        document["timestamp"] = timestamp
        number_of_attempts = int(self.ATTEMPTS_TIMEOUT / self.INTERVAL_BTW_ATTEMPTS)
        is_document_inserted = False
        for _ in range(number_of_attempts):
            db_collection = self.get_db_collection(db_name=db_name, collection=collection)
            try:
                if not is_document_inserted:
                    # Checks whether the document was not inserted yet before attempting an insertion.
                    inserted_document = db_collection.insert_one(document)
                    document_id = inserted_document.inserted_id
                    is_document_inserted = True
                self.close_db_connection()
                break
            except:
                self.close_db_connection()
                document_id = None
                # Waits for an interval before executing the next attempt.
                sleep(self.INTERVAL_BTW_ATTEMPTS)
        if document_id is None:
            print("The document could not be inserted into the DB collection.")
        return document_id

    def insert_document_list(self, db_name, collection, document_list, timestamp):
        """Inserts the given documents into the given DB collection."""
        # Adds the timestamp to every document within the given document list.
        for document in document_list:
            document["timestamp"] = timestamp
        number_of_attempts = int(self.ATTEMPTS_TIMEOUT / self.INTERVAL_BTW_ATTEMPTS)
        are_documents_inserted = False
        for _ in range(number_of_attempts):
            db_collection = self.get_db_collection(db_name=db_name, collection=collection)
            try:
                if not are_documents_inserted:
                    # Checks whether the documents were not inserted yet before attempting an insertion.
                    inserted_documents = db_collection.insert_many(document_list)
                    document_ids = inserted_documents.inserted_ids
                    are_documents_inserted = True
                self.mongodb_client.close()
                break
            except:
                self.close_db_connection()
                document_ids = None
                # Waits for an interval before executing the next attempt.
                sleep(self.INTERVAL_BTW_ATTEMPTS)
        if document_ids is None:
            print("The documents could not be inserted into the DB collection.")
        return document_ids

    def count_documents_in_db_collection(self, db_name, collection):
        """Counts the number of documents in the given DB collection."""
        number_of_attempts = int(self.ATTEMPTS_TIMEOUT / self.INTERVAL_BTW_ATTEMPTS)
        for _ in range(number_of_attempts):
            db_collection = self.get_db_collection(db_name=db_name, collection=collection)
            try:
                count = db_collection.count()
                self.mongodb_client.close()
                break
            except:
                self.mongodb_client.close()
                count = None
                # Waits for an interval before executing the next attempt.
                sleep(self.INTERVAL_BTW_ATTEMPTS)
        if count is None:
            print("The documents of the DB collection could not be counted.")
        return count

    def find_first(self, db_name, collection):
        """Finds the first record in the given DB collection."""
        number_of_attempts = int(self.ATTEMPTS_TIMEOUT / self.INTERVAL_BTW_ATTEMPTS)
        for _ in range(number_of_attempts):
            db_collection = self.get_db_collection(db_name=db_name, collection=collection)
            try:
                document = db_collection.find_one()
                self.mongodb_client.close()
                break
            except:
                self.mongodb_client.close()
                document = False
                # Waits for an interval before executing the next attempt.
                sleep(self.INTERVAL_BTW_ATTEMPTS)
        if not document:
            print("The first document of the DB collection could not be retrieved.")
        return document

    def find_document_by_id(self, db_name, collection, document_id_as_string):
        """Converts id from string into ObjectId and gets the query's result."""
        number_of_attempts = int(self.ATTEMPTS_TIMEOUT / self.INTERVAL_BTW_ATTEMPTS)
        for _ in range(number_of_attempts):
            db_collection = self.get_db_collection(db_name=db_name, collection=collection)
            try:
                document = db_collection.find_one({"_id": ObjectId(document_id_as_string)})
                self.mongodb_client.close()
                break
            except:
                self.mongodb_client.close()
                document = False
                # Waits for an interval before executing the next attempt.
                sleep(self.INTERVAL_BTW_ATTEMPTS)
        if not document:
            print("The document of the DB collection containing the given id could not be retrieved.")
        return document

    def find_all(self, db_name, collection):
        """Returns all documents in the given DB collection."""
        number_of_attempts = int(self.ATTEMPTS_TIMEOUT / self.INTERVAL_BTW_ATTEMPTS)
        for _ in range(number_of_attempts):
            db_collection = self.get_db_collection(db_name=db_name, collection=collection)
            try:
                document_list = db_collection.find()
                self.mongodb_client.close()
                break
            except:
                self.mongodb_client.close()
                document_list = False
                # Waits for an interval before executing the next attempt.
                sleep(self.INTERVAL_BTW_ATTEMPTS)
        if not document_list:
            print("The documents of the DB collection could not be retrieved.")
        return document_list

    def add_development_stage(self, db_name, collection, timestamp_1_array, timestamp_2_array, lot_number,
                              development_stage):
        """
        Looks for the documents between the two given timestamps having the given lot number and adds the given
        development stage to them.
        """
        timestamp_1 = dt.datetime(day=timestamp_1_array[0], month=timestamp_1_array[1], year=timestamp_1_array[2],
                                  hour=timestamp_1_array[3], minute=timestamp_1_array[4], second=timestamp_1_array[5])
        timestamp_2 = dt.datetime(day=timestamp_2_array[0], month=timestamp_2_array[1], year=timestamp_2_array[2],
                                  hour=timestamp_2_array[3], minute=timestamp_2_array[4], second=timestamp_2_array[5])
        # Converts the time into UTC adding the corresponding offset to the given local time.
        timestamp_1 = timestamp_1 + dt.timedelta(hours=self.UTC_OFFSET_FROM_LOCAL_TIMEZONE)
        timestamp_2 = timestamp_2 + dt.timedelta(hours=self.UTC_OFFSET_FROM_LOCAL_TIMEZONE)
        number_of_attempts = int(self.ATTEMPTS_TIMEOUT / self.INTERVAL_BTW_ATTEMPTS)
        for _ in range(number_of_attempts):
            db_collection = self.get_db_collection(db_name=db_name, collection=collection)
            try:
                documents_to_update = db_collection.find({"timestamp": {"$gte": timestamp_1, "$lt": timestamp_2},
                                                          "lot_number": lot_number})
                if documents_to_update is not None:
                    update = {"development_stage": development_stage}
                    updated_documents = list()
                    for document in documents_to_update:
                        document_id = document["_id"]
                        updated_documents.append(self.update_document(db_collection=db_collection,
                                                                      document_id=document_id, update=update))
                    self.mongodb_client.close()
                    break
                else:
                    # No documents between the given timestamps were found.
                    updated_documents = None
                    break
            except:
                self.mongodb_client.close()
                updated_documents = None
                # Waits for an interval before executing the next attempt.
                sleep(self.INTERVAL_BTW_ATTEMPTS)
        if updated_documents is None:
            print("The documents of the DB collection between the given timestamps could not be updated.")
        return updated_documents

    def update_document(self, db_collection, document_id, update):
        """Updates the document that has the given document id with the given update information."""
        db_collection.update_one({"_id": document_id}, {"$set": update})
        updated_document = db_collection.find_one({"_id": document_id})
        # Returns the document after updating it.
        return updated_document

    def delete_document(self, db_name, collection, document_id):
        """
        Deletes the document that has the given document id and returns whether it was successfully deleted or not.
        """
        number_of_attempts = int(self.ATTEMPTS_TIMEOUT / self.INTERVAL_BTW_ATTEMPTS)
        for _ in range(number_of_attempts):
            db_collection = self.get_db_collection(db_name=db_name, collection=collection)
            try:
                db_collection.delete_one({"_id": document_id})
                is_document_deleted = False
                if db_collection.find_one({"_id": document_id}) is None:
                    # A document with the given document id was not found.
                    is_document_deleted = True
                self.mongodb_client.close()
                break
            except:
                self.mongodb_client.close()
                is_document_deleted = None
                # Waits for an interval before executing the next attempt.
                sleep(self.INTERVAL_BTW_ATTEMPTS)
        if is_document_deleted is None:
            print("The document of the DB collection could not be deleted.")
        return is_document_deleted
