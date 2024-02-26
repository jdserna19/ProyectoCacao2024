import requests


class ThingworxCommunicator:
    LOT_1_DATA = ["L1\n", "RPL1P0\n", "RPL1P1\n", "RPL1P2\n", "RPL1P3\n", "RPL1P4\n"]
    LOT_2_DATA = ["L2\n", "RPL2P0\n", "RPL2P1\n", "RPL2P2\n", "RPL2P3\n", "RPL2P4\n"]
    LOT_3_DATA = ["L3\n", "RPL3P0\n", "RPL3P1\n", "RPL3P2\n", "RPL3P3\n", "RPL3P4\n"]
    LOT_4_DATA = ["L4\n", "RPL4P0\n", "RPL4P1\n", "RPL4P2\n", "RPL4P3\n", "RPL4P4\n"]
    GENERAL_DATA = ["GD\n", "RAL1\n", "RAL2\n", "RAL3\n", "RAL4\n", "RB\n", "RE\n"]
    TWX_CONNECTION_TIMEOUT = 5
    STATUS_CODE_OK = 200

    def __init__(self, request_url, app_key):
        self.request_url = request_url
        self.headers = {"Content-Type": "application/json", "Accept": "application/json", "appKey": app_key}

    def structure_and_post_data(self, command, data):
        """Structures and posts the given data according to the kind of data that the given command indicates."""
        data_dictionary = dict()
        if command in self.LOT_1_DATA:
            data_dictionary["lot_1_data"] = data
            self.post("update_lot_1", data_dictionary)
        elif command in self.LOT_2_DATA:
            data_dictionary["lot_2_data"] = data
            self.post("update_lot_2", data_dictionary)
        elif command in self.LOT_3_DATA:
            data_dictionary["lot_3_data"] = data
            self.post("update_lot_3", data_dictionary)
        elif command in self.LOT_4_DATA:
            data_dictionary["lot_4_data"] = data
            self.post("update_lot_4", data_dictionary)
        elif command in self.GENERAL_DATA:
            data_dictionary["general_data"] = data
            self.post("update_general_data", data_dictionary)
        else:
            # The given command is unknown and the data dictionary cannot be posted.
            print("Unknown command.")

    def post(self, service, data):
        """Posts the given data to the request url's service."""
        try:
            response = requests.post(url="{}{}".format(self.request_url, service), headers=self.headers, json=data,
                                     timeout=self.TWX_CONNECTION_TIMEOUT)
            status_code = response.status_code
            if status_code != self.STATUS_CODE_OK:
                # The given data could not be posted.
                print("Result: {} - {}".format(str(status_code), response.reason))
        except:
            print("The given data could not be posted.")
