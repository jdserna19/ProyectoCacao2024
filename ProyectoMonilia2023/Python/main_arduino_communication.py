from arduino_communication import ArduinoCommunication
from data_transformation import DataTransformation

ARDUINO_COMMAND = "L1\n"
COMMAND_DATA_LENGTH = {"L1\n": 8, "L2\n": 8, "L3\n": 8, "L4\n": 8, "GD\n": 4, "RPL1P1\n": 2, "RPL1P2\n": 2,
                       "RPL1P3\n": 2, "RPL1P4\n": 2, "RPL2P1\n": 2, "RPL2P2\n": 2, "RPL2P3\n": 2, "RPL2P4\n": 2,
                       "RPL3P1\n": 2, "RPL3P2\n": 2, "RPL3P3\n": 2, "RPL3P4\n": 2, "RPL4P1\n": 2, "RPL4P2\n": 2,
                       "RPL4P3\n": 2, "RPL4P4\n": 2, "RAL1\n": 1, "RAL2\n": 1, "RAL3\n": 1, "RAL4\n": 1, "RB\n": 1,
                       "RE\n": 1}

# Gets the Arduino's response to a given command.
arduino_communication = ArduinoCommunication()
arduino_communication.establish_arduino_connection()
arduino_response = arduino_communication.write_to_arduino(command=ARDUINO_COMMAND,
                                                          data_length=COMMAND_DATA_LENGTH[ARDUINO_COMMAND])

# Structures a dictionary with the retrieved data.
data_transformation = DataTransformation()
data_dictionary = data_transformation.structure_data(command=ARDUINO_COMMAND, data=arduino_response)
print(data_dictionary)
