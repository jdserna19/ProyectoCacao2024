import requests


class CropDataUpdating:
    REQUEST_URL = "http://iot.dis.eafit.edu.co/Thingworx/Things/CoffeeCrop/Services/"
    HEADERS = {"Content-Type": "application/json", "Accept": "application/json",
               "appKey": ""}

    def __init__(self):
        None

    def generate_empty_lot_x_data(self, lot_name):
        """Generates empty data for the given lot name."""
        # Creates the main key for the data.
        lot_name_data = lot_name + "_data"
        # Creates the base structure.
        lot_x_data = {lot_name_data: {}}
        return lot_x_data

    def generate_lot_x_data(self, lot_name):
        """Generates sample data for the given lot name."""
        # Creates the main key for the data.
        lot_name_data = lot_name + "_data"
        # Creates the base structure.
        lot_x_data = {lot_name_data: {}}
        lot_x_data[lot_name_data]["soil_moisture"] = 25
        lot_x_data[lot_name_data]["soil_temperature"] = 43
        lot_x_data[lot_name_data]["ph"] = 4
        lot_x_data[lot_name_data]["rotary_platform_extensions_state"] = 1
        lot_x_data[lot_name_data]["illuminance"] = 26
        lot_x_data[lot_name_data]["env_temperature"] = 31
        lot_x_data[lot_name_data]["env_humidity"] = 45
        lot_x_data[lot_name_data]["rotary_platforms_angle"] = 30
        return lot_x_data

    def generate_empty_general_data(self):
        """Generates empty data for the general data."""
        # Creates the base structure.
        general_data = {"general_data": {}}
        return general_data

    def generate_general_data(self):
        """Generates sample data for the general data."""
        # Creates the base structure.
        general_data = {"general_data": {}}
        general_data["general_data"]["rotary_arms_angle"] = 20
        general_data["general_data"]["flow_rate"] = 39
        general_data["general_data"]["solenoid_valves_state"] = 1
        general_data["general_data"]["wind_speed"] = 3
        return general_data

    def post_update(self, service, data):
        """Posts the given data to the REQUEST_URL's service."""
        response = requests.post(self.REQUEST_URL + service, headers=self.HEADERS, json=data)
        print("Result: %s - %s" % (str(response.status_code), response.reason))
        return response.json()
