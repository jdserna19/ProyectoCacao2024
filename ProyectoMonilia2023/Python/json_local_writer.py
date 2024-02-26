import json
import os


class JSONLocalWriter:
    DATA_ROOT_DIR_NAME = "data/"
    DATE_TIME_FORMAT = "%d%m%Y%H%M%S/"

    def __init__(self):
        None

    def create_data_dir(self, current_timestamp):
        """Creates a new directory for the data according to the current date and time."""
        data_dir = current_timestamp.strftime(self.DATE_TIME_FORMAT)
        os.makedirs(self.DATA_ROOT_DIR_NAME + data_dir)
        # Returns the path to the created directory.
        return data_dir

    def create_data_sub_dir(self, data_dir, data_sub_dir):
        """Creates a new subdirectory for the data according to the given directory names."""
        os.makedirs(self.DATA_ROOT_DIR_NAME + data_dir + data_sub_dir)
        # Returns the path to the created directory.
        return data_sub_dir

    def write_json_to_file(self, data_dir, data_sub_dir, filename, document):
        """Writes the given document into a JSON file according to the given directory and file names."""
        try:
            document_path = self.DATA_ROOT_DIR_NAME + data_dir + data_sub_dir + filename
            with open(document_path, "w") as outfile:
                json.dump(obj=document, fp=outfile, indent=4)
        except:
            document_path = None
        return document_path
