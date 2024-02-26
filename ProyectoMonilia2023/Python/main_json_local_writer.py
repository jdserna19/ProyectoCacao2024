from json_local_writer import JSONLocalWriter
import datetime as dt

TIMEZONE = dt.timezone(dt.timedelta(hours=-5))
UTC_TIMEZONE = dt.timezone(dt.timedelta(hours=0))
DATE_TIME_FORMAT = "%d%m%Y%H%M%S"

# Creates a directory and the corresponding subdirectory to write a document into a JSON file.
json_local_writer = JSONLocalWriter()
current_timestamp = dt.datetime.now(TIMEZONE)
# The current_utc_timestamp is used for the 'timestamp' field within the document. It must be stored as a string.
current_utc_timestamp = current_timestamp.astimezone(UTC_TIMEZONE)
data_dir = json_local_writer.create_data_dir(current_timestamp)
data_sub_dir = json_local_writer.create_data_sub_dir(data_dir=data_dir, data_sub_dir="lot_1/")
document = {"lot_sensor_1": 46, "lot_sensor_2": 22, "timestamp": current_utc_timestamp.strftime(DATE_TIME_FORMAT),
            "lot_number": 1}
document_path = json_local_writer.write_json_to_file(data_dir=data_dir, data_sub_dir=data_sub_dir,
                                                     filename="lot_1.json", document=document)
