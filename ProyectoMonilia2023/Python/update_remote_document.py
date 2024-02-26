from mongodb_communicator import MongoDBCommunicator
from data_collection import MONGODB_HOST, MONGODB_PORT, DB_NAME, DB_COLLECTION_LOT_DATA
import pprint

# Timestamp's format is [day, month, year, hour, minute, second].
TIMESTAMP_1_ARRAY = [2, 7, 2018, 0, 0, 0]
TIMESTAMP_2_ARRAY = [2, 7, 2018, 23, 59, 0]
LOT_NUMBER = 3
DEVELOPMENT_STAGE = 1

mongodb_communicator = MongoDBCommunicator(mongodb_host=MONGODB_HOST, mongodb_port=MONGODB_PORT)
db_collection_lot_data = mongodb_communicator.get_db_collection(db_name=DB_NAME, db_collection=DB_COLLECTION_LOT_DATA)
print("MongoDB connection established.")
updated_documents = mongodb_communicator.add_development_stage(db_collection=db_collection_lot_data,
                                                               timestamp_1_array=TIMESTAMP_1_ARRAY,
                                                               timestamp_2_array=TIMESTAMP_2_ARRAY,
                                                               lot_number=LOT_NUMBER,
                                                               development_stage=DEVELOPMENT_STAGE)
if len(updated_documents) != 0:
    # The documents were updated successfully.
    print("The documents were updated.")
    for document in updated_documents:
        pprint.pprint(document)
else:
    # The documents matching the query could not be found.
    print("Documents were not found.")
