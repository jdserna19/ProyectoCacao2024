from data_subdirectory_creator import DataSubdirectoryCreator
from arduino_communicator import ArduinoCommunicator
from data_structurer import DataStructurer
from time import sleep
NUMBER_OF_LOTS = 4
ARDUINO_1_PORT = "/dev/ttyACM0"
ARDUINO_1_BAUD_RATE = 115200
ARDUINO_1_TIMEOUT = 60
ARDUINO_2_PORT = "/dev/ttyACM1"
ARDUINO_2_BAUD_RATE = 9600
ARDUINO_2_TIMEOUT = 60
ARDUINO_COMMAND_DATA_LENGTH = {"L1\n": 8, "L2\n": 8, "L3\n": 8, "L4\n": 8, "GD\n": 4, "RPL1P0\n": 2, "RPL1P1\n": 2,
                               "RPL1P2\n": 2, "RPL1P3\n": 2, "RPL1P4\n": 2, "RPL2P0\n": 2, "RPL2P1\n": 2, "RPL2P2\n": 2,
                               "RPL2P3\n": 2, "RPL2P4\n": 2, "RPL3P0\n": 2, "RPL3P1\n": 2, "RPL3P2\n": 2, "RPL3P3\n": 2,
                               "RPL3P4\n": 2, "RPL4P0\n": 2, "RPL4P1\n": 2, "RPL4P2\n": 2, "RPL4P3\n": 2, "RPL4P4\n": 2,
                               "RAL1\n": 1, "RAL2\n": 1, "RAL3\n": 1, "RAL4\n": 1, "RB\n": 1, "RE\n": 1}
data_subdirectory_creator = DataSubdirectoryCreator(NUMBER_OF_LOTS)

arduino_1_communicator = ArduinoCommunicator(arduino_port=ARDUINO_1_PORT, arduino_baud_rate=ARDUINO_1_BAUD_RATE,
                                             arduino_timeout=ARDUINO_1_TIMEOUT)

arduino_2_communicator = ArduinoCommunicator(arduino_port=ARDUINO_2_PORT, arduino_baud_rate=ARDUINO_2_BAUD_RATE,
                                             arduino_timeout=ARDUINO_2_TIMEOUT)

print("Arduino connections established.")
data_structurer = DataStructurer()
sleep(6)
command = "L1\n"
data_length = ARDUINO_COMMAND_DATA_LENGTH[command]
arduino_response = arduino_1_communicator.write_to_arduino(command=command, data_length=data_length)
print(arduino_response)
print()
