class DataStructurer:
    LOT_DATA = ["L1\n", "L2\n", "L3\n", "L4\n"]
    GENERAL_DATA = ["GD\n"]
    ROTARY_PLATFORM_DATA = ["RPL1P0\n", "RPL1P1\n", "RPL1P2\n", "RPL1P3\n", "RPL1P4\n", "RPL2P0\n", "RPL2P1\n",
                            "RPL2P2\n", "RPL2P3\n", "RPL2P4\n", "RPL3P0\n", "RPL3P1\n", "RPL3P2\n", "RPL3P3\n",
                            "RPL3P4\n", "RPL4P0\n", "RPL4P1\n", "RPL4P2\n", "RPL4P3\n", "RPL4P4\n"]
    ROTARY_ARM_DATA = ["RAL1\n", "RAL2\n", "RAL3\n", "RAL4\n"]
    SOLENOID_VALVE_DATA = ["RB\n", "RE\n"]
    LOT_ID_NUMBER = {"L1\n": 1, "L2\n": 2, "L3\n": 3, "L4\n": 4}
    NONE_NUMERICAL_VALUE = -1.0

    def __init__(self):
        None

    def structure_data(self, command, data):
        """Structures the given data according to the kind of data that the given command indicates."""
        data_dictionary = dict()
        if command in self.LOT_DATA:
            data_dictionary = self.structure_lot_data(lot_data=data, lot_id=command)
        elif command in self.GENERAL_DATA:
            data_dictionary = self.structure_general_data(data)
        elif command in self.ROTARY_PLATFORM_DATA:
            data_dictionary = self.structure_rotary_platform_data(data)
        elif command in self.ROTARY_ARM_DATA:
            data_dictionary = self.structure_rotary_arm_data(data)
        elif command in self.SOLENOID_VALVE_DATA:
            data_dictionary = self.structure_solenoid_valve_data(data)
        else:
            # The given command is unknown and the data dictionary to retrieve will be empty.
            print("Unknown command.")
        data_dictionary = self.clean_data_dictionary(data_dictionary)
        return data_dictionary

    def structure_lot_data(self, lot_data, lot_id):
        """Structures the given data knowing that it represents lot data and adds it corresponding number."""
        data_dictionary = {
            "ph": self.transform_ph(lot_data[0]),
            "soil_temperature": self.transform_soil_temperature(lot_data[1]),
            "soil_moisture": self.transform_soil_moisture(lot_data[2]),
            "illuminance": self.transform_illuminance(lot_data[3]),
            "env_temperature": self.transform_env_temperature(lot_data[4]),
            "env_humidity": self.transform_env_humidity(lot_data[5]),
            "rotary_platforms_angle": self.transform_rotary_platforms_angle(lot_data[6]),
            "rotary_platform_extensions_state": self.transform_rotary_platform_extensions_state(lot_data[7]),
            "lot_number": self.LOT_ID_NUMBER[lot_id]
        }
        return data_dictionary

    def structure_general_data(self, general_data):
        """Structures the given data knowing that it represents general data."""
        data_dictionary = {
            "flow_rate": self.transform_flow_rate(general_data[0]),
            "wind_speed": self.transform_wind_speed(general_data[1]),
            "solenoid_valves_state": self.transform_solenoid_valves_state(general_data[2]),
            "rotary_arms_angle": self.transform_rotary_arms_angle(general_data[3])
        }
        return data_dictionary

    def structure_rotary_platform_data(self, rotary_platform_data):
        """Structures the given data knowing that it represents rotary platform data."""
        data_dictionary = {
            "rotary_platforms_angle": self.transform_rotary_platforms_angle(rotary_platform_data[0]),
            "rotary_platform_extensions_state": self.transform_rotary_platform_extensions_state(rotary_platform_data[1])
        }
        return data_dictionary

    def structure_rotary_arm_data(self, rotary_arm_data):
        """Structures the given data knowing that it represents arm data."""
        data_dictionary = {
            "rotary_arms_angle": self.transform_rotary_arms_angle(rotary_arm_data[0])
        }
        return data_dictionary

    def structure_solenoid_valve_data(self, solenoid_valve_data):
        """Structures the given data knowing that it represents solenoid valve data."""
        data_dictionary = {
            "solenoid_valves_state": self.transform_solenoid_valves_state(solenoid_valve_data[0])
        }
        return data_dictionary

    def transform_ph(self, arduino_ph):
        if arduino_ph == '':
            arduino_ph = self.NONE_NUMERICAL_VALUE
        return float(arduino_ph)

    def transform_soil_temperature(self, arduino_soil_temperature):
        if arduino_soil_temperature == '':
            arduino_soil_temperature = self.NONE_NUMERICAL_VALUE
        return float(arduino_soil_temperature)

    def transform_soil_moisture(self, arduino_soil_moisture):
        if arduino_soil_moisture == '':
            arduino_soil_moisture = self.NONE_NUMERICAL_VALUE
        return float(arduino_soil_moisture)

    def transform_illuminance(self, arduino_illuminance):
        if arduino_illuminance == '':
            arduino_illuminance = self.NONE_NUMERICAL_VALUE
        return float(arduino_illuminance)

    def transform_env_temperature(self, arduino_env_temperature):
        if arduino_env_temperature == '':
            arduino_env_temperature = self.NONE_NUMERICAL_VALUE
        return float(arduino_env_temperature)

    def transform_env_humidity(self, arduino_env_humidity):
        if arduino_env_humidity == '':
            arduino_env_humidity = self.NONE_NUMERICAL_VALUE
        return float(arduino_env_humidity)

    def transform_rotary_platforms_angle(self, arduino_rotary_platforms_angle):
        if arduino_rotary_platforms_angle == '':
            arduino_rotary_platforms_angle = self.NONE_NUMERICAL_VALUE
        return float(arduino_rotary_platforms_angle)

    def transform_rotary_platform_extensions_state(self, arduino_rotary_platform_extensions_state):
        if arduino_rotary_platform_extensions_state == '':
            arduino_rotary_platform_extensions_state = self.NONE_NUMERICAL_VALUE
        return float(arduino_rotary_platform_extensions_state)

    def transform_flow_rate(self, arduino_flow_rate):
        if arduino_flow_rate == '':
            arduino_flow_rate = self.NONE_NUMERICAL_VALUE
        return float(arduino_flow_rate)

    def transform_wind_speed(self, arduino_wind_speed):
        if arduino_wind_speed == '':
            arduino_wind_speed = self.NONE_NUMERICAL_VALUE
        return float(arduino_wind_speed)

    def transform_solenoid_valves_state(self, arduino_solenoid_valves_state):
        if arduino_solenoid_valves_state == '':
            arduino_solenoid_valves_state = self.NONE_NUMERICAL_VALUE
        return float(arduino_solenoid_valves_state)

    def transform_rotary_arms_angle(self, arduino_rotary_arms_angle):
        if arduino_rotary_arms_angle == '':
            arduino_rotary_arms_angle = self.NONE_NUMERICAL_VALUE
        return float(arduino_rotary_arms_angle)

    def clean_data_dictionary(self, data_dictionary):
        """Only the non-missing values will be kept in the data dictionary."""
        data_dictionary = {key: value for key, value in data_dictionary.items() if value != self.NONE_NUMERICAL_VALUE}
        return data_dictionary
