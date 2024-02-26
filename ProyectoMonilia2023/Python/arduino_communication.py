from time import sleep
import serial


class ArduinoCommunication:
    ARDUINO_PORT = "/dev/ttyACM0"
    ARDUINO_BAUD_RATE = 115200
    ARDUINO_TIMEOUT = 60

    def __init__(self):
        self.arduino = None

    def establish_arduino_connection(self):
        """Establishes the connection between Arduino and Python."""
        self.arduino = serial.Serial(port=self.ARDUINO_PORT, baudrate=self.ARDUINO_BAUD_RATE, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,
                                     timeout=self.ARDUINO_TIMEOUT)
        self.arduino.readline()
        print("Arduino connection established.\n")

    def write_to_arduino(self, command, data_length):
        """Sends a command to Arduino and returns its response."""
        arduino_response = list()
        self.arduino.write(command.encode())
        sleep(0.1)
        for i in range(data_length):
            arduino_response.append(self.arduino.readline().rstrip().decode())
        return arduino_response
