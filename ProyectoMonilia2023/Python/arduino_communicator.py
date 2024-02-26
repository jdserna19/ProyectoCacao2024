from time import sleep
import serial


class ArduinoCommunicator:
    def __init__(self, arduino_port, arduino_baud_rate, arduino_timeout):
        self.arduino = serial.Serial(port=arduino_port, baudrate=arduino_baud_rate, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=arduino_timeout)
        sleep(0.1)
        self.arduino.flushOutput()
        # Waits for the first response coming from Arduino in order to verify the communication.
        self.arduino.readline().rstrip().decode()

    def write_to_arduino(self, command, data_length):
        """Sends a command to Arduino and returns its response."""
        arduino_response = list()
        self.arduino.write(command.encode())
        sleep(0.1)
        for i in range(data_length):
            arduino_response.append(self.arduino.readline().rstrip().decode())
        return arduino_response