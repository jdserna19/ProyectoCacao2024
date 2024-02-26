import json


class DocumentLocalWriter:
    LOT_ID_FILENAME = {"L1\n": "lot_1.json", "L2\n": "lot_2.json", "L3\n": "lot_3.json", "L4\n": "lot_4.json",
                       "GD\n": "general_data.json"}

    def __init__(self):
        None

    def write_document_to_file(self, document_path, command, document, timestamp):
        """Writes the given document into a JSON file according to the given path and command."""
        # Adds the filename to the document path.
        document_path = "{}{}".format(document_path, self.LOT_ID_FILENAME[command])
        # Adds the timestamp to the document.
        document["timestamp"] = timestamp
        try:
            with open(document_path, "w") as outfile:
                json.dump(obj=document, fp=outfile, indent=4)
        except:
            document_path = None
        return document_path

    def add_development_stage_to_document(self, document_path, command, development_stage):
        """Opens the document according to the given path and command and adds the given development stage to it."""
        # Adds the filename to the document path.
        document_path = "{}{}".format(document_path, self.LOT_ID_FILENAME[command])
        try:
            with open(document_path, "r") as json_file:
                document = json.load(fp=json_file)
            # Adds the development stage to the document.
            document["development_stage"] = development_stage
            # Overwrites the document so that it contains the given development stage.
            with open(document_path, "w") as outfile:
                json.dump(obj=document, fp=outfile, indent=4)
        except:
            document_path = None
        return document_path
