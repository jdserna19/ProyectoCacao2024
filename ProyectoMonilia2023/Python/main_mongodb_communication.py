from mongodb_communication import MongoDBCommunication
import pprint
import datetime

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
DB_NAME = "coffee_leaf_rust_diagnosis"
DB_COLLECTION_LOT_DATA = "lot_data"
DB_COLLECTION_GENERAL_DATA = "general_data"

# Captures the current timestamp and creates some documents for insertion.
mongodb_communication = MongoDBCommunication(mongodb_host=MONGODB_HOST, mongodb_port=MONGODB_PORT)
current_timestamp = datetime.datetime.utcnow()
document_1 = {"lot_sensor_1": 23, "lot_sensor_2": 14, "timestamp": current_timestamp}
current_timestamp = datetime.datetime.utcnow()
document_2 = {"lot_sensor_1": 46, "lot_sensor_2": 22, "timestamp": current_timestamp}
current_timestamp = datetime.datetime.utcnow()
document_3 = {"general_sensor_1": 28, "general_sensor_2": 31, "timestamp": current_timestamp}
document_list = [document_1, document_2]
db_collection_lot_data = mongodb_communication.get_db_collection(db_name=DB_NAME, db_collection=DB_COLLECTION_LOT_DATA)
db_collection_general_data = mongodb_communication.get_db_collection(db_name=DB_NAME,
                                                                     db_collection=DB_COLLECTION_GENERAL_DATA)
'''
inserted_documents_ids = mongodb_communication.insert_document_list(db_collection=db_collection_lot_data,
                                                                    document_list=document_list)
print(inserted_documents_ids)
document_3_id = mongodb_communication.insert_document(db_collection=db_collection_general_data, document=document_3)
print(document_3_id)
'''
# Counts the number of documents in a given DB collection and retrieves its first document.
print(mongodb_communication.count_documents_in_db_collection(db_collection_lot_data))
pprint.pprint(mongodb_communication.find_first(db_collection_lot_data))
# Retrieves all documents inside a given range of timestamps.
# Timestamp's format is [day, month, year, hour, minute, second].
timestamp_1_array = [26, 6, 2018, 10, 0, 0]
timestamp_2_array = [26, 6, 2018, 11, 0, 0]
query_result = mongodb_communication.get_documents_btw_timestamps(db_collection=db_collection_lot_data,
                                                                  timestamp_1_array=timestamp_1_array,
                                                                  timestamp_2_array=timestamp_2_array)
for document in query_result:
    pprint.pprint(document)
# Retrieves all documents inside a given range of timestamps in order to update them.
query_result = mongodb_communication.get_documents_btw_timestamps(db_collection=db_collection_lot_data,
                                                                  timestamp_1_array=timestamp_1_array,
                                                                  timestamp_2_array=timestamp_2_array)
for document in query_result:
    document_id = document["_id"]
    # The update that is want to be made.
    update = {"development_stage": 2}
    updated_document = mongodb_communication.update_document(db_collection=db_collection_lot_data,
                                                             document_id=document_id, update=update)
    pprint.pprint(updated_document)
'''
Deletes the document that has the given document id and returns True if it was deleted successfully or False otherwise.
'''
query_result = mongodb_communication.get_documents_btw_timestamps(db_collection=db_collection_lot_data,
                                                                  timestamp_1_array=timestamp_1_array,
                                                                  timestamp_2_array=timestamp_2_array)
# print(mongodb_communication.delete_document(db_collection=db_collection_lot_data, document_id=query_result[0]["_id"]))
