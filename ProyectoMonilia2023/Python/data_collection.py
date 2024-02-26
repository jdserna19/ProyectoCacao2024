from data_subdirectory_creator import DataSubdirectoryCreator
from arduino_communicator import ArduinoCommunicator
from data_structurer import DataStructurer
from document_local_writer import DocumentLocalWriter
from thingworx_communicator import ThingworxCommunicator
from image_capturer import ImageCapturer
from pulse_generator import PulseGenerator
from data_copier import DataCopier
from mongodb_communicator import MongoDBCommunicator
from vpn_connector import VPNConnector
from data_uploader import DataUploader
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler as Scheduler
import datetime as dt
import schedule

NUMBER_OF_LOTS = 4
ARDUINO_1_PORT = "/dev/ttyACM0"  # "/dev/cu.usbmodem1411"
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
TWX_REQUEST_URL = "http://iot.dis.eafit.edu.co/Thingworx/Things/CoffeeCrop/Services/"
TWX_APP_KEY = "31cd5888-213d-4d61-b5d5-e3f748fa321c"
NUMBER_OF_PLANTS = 4
PLANT_NAMES = ["plant_1", "plant_2", "plant_3", "plant_4"]
RGN_CAMERA_PIN = 7
RE_CAMERA_PIN = 13
PWM_FREQUENCY = 400
MULTISPECTRAL_CAMERA_DO_NOTHING = 37.6
MULTISPECTRAL_CAMERA_ENTER_EXIT_USB_TRANSFER = 57.6
MULTISPECTRAL_CAMERA_CAPTURE_IMAGE = 77.6
RGN_CAMERA_PATH_INDICATOR = "/media/pi/VOLUME1/DCIM/Photo/rgn.txt"
RE_CAMERA_PATH_INDICATOR = "/media/pi/VOLUME1/DCIM/Photo/re.txt"
RGN_CAMERA_FILES_DIRECTORY = "/media/pi/VOLUME1/DCIM/Photo/"
RE_CAMERA_FILES_DIRECTORY = "/media/pi/VOLUME1/DCIM/Photo/"
MULTISPECTRAL_IMAGES_NAMES = ["rgn", "re"]
MONGODB_HOST = "mongodb://192.168.10.115"
MONGODB_PORT = 27017
DB_NAME = "coffee_leaf_rust_diagnosis"
DB_COLLECTION_LOT_DATA = "lot_data"
DB_COLLECTION_GENERAL_DATA = "general_data"
VPN_CONNECTION_FILE_LOCATION = "/home/pi/Documents/vpn/"
VPN_CONNECTION_FILE = "vpn_connection.exp"
SERVER_HOST = "192.168.10.115"
SERVER_USERNAME = "asanch41"
SERVER_PASSWORD = "Asd87Jkl."
PACKAGE_PARTIAL_NUMBER_OF_FILES = 5
PACKAGE_TOTAL_NUMBER_OF_FILES = 29
SERVER_DESTINATION_DIRECTORY = "/home/asanch41/Documents/coffee_leaf_rust_diagnosis/"
DATA_COLLECTION_SEQUENCE = ["L1\n", "L2\n", "L3\n", "L4\n", "GD\n"]
DATA_COLLECTION_SUBSEQUENCES = {"L1\n": ["RAL1\n", "L1\n", "RPL1P1\n", "RPL1P2\n", "RPL1P3\n", "RPL1P4\n", "RPL1P0\n"],
                                "L2\n": ["RAL2\n", "L2\n", "RPL2P1\n", "RPL2P2\n", "RPL2P3\n", "RPL2P4\n", "RPL2P0\n"],
                                "L3\n": ["RAL3\n", "L3\n", "RPL3P1\n", "RPL3P2\n", "RPL3P3\n", "RPL3P4\n", "RPL3P0\n"],
                                "L4\n": ["RAL4\n", "L4\n", "RPL4P1\n", "RPL4P2\n", "RPL4P3\n", "RPL4P4\n", "RPL4P0\n"]}
ROTARY_ARM_INITIAL_POSITION = "RAL1\n"
RAIN_COMMANDS = ["RB\n", "RE\n"]
SEPTEMBER_RAIN_DAYS = ["08", "09", "10", "12", "13", "14", "16", "17", "18", "19", "22", "24", "30"]
OCTOBER_RAIN_DAYS = ["02", "03", "05", "07", "08", "09", "10", "12", "13", "14", "17", "19", "20", "21", "22", "23",
                     "24", "26", "27", "28"]
NOVEMBER_RAIN_DAYS = ["01", "03", "05"]
RAIN_TIMES = [("00:20:00", "01:00:00"), ("04:00:00", "04:30:00"), ("14:20:00", "14:40:00"), ("17:00:00", "17:20:00"),
              ("19:00:00", "19:40:00"), ("22:40:00", "23:10:00")]

data_subdirectory_creator = DataSubdirectoryCreator(NUMBER_OF_LOTS)

arduino_1_communicator = ArduinoCommunicator(arduino_port=ARDUINO_1_PORT, arduino_baud_rate=ARDUINO_1_BAUD_RATE,
                                             arduino_timeout=ARDUINO_1_TIMEOUT)
arduino_2_communicator = ArduinoCommunicator(arduino_port=ARDUINO_2_PORT, arduino_baud_rate=ARDUINO_2_BAUD_RATE,
                                             arduino_timeout=ARDUINO_2_TIMEOUT)
print("Arduino connections established.")
data_structurer = DataStructurer()
document_local_writer = DocumentLocalWriter()
thingworx_communicator = ThingworxCommunicator(request_url=TWX_REQUEST_URL, app_key=TWX_APP_KEY)
image_capturer = ImageCapturer()
pulse_generator = PulseGenerator(rgn_camera_pin=RGN_CAMERA_PIN, re_camera_pin=RE_CAMERA_PIN,
                                 pwm_frequency=PWM_FREQUENCY, do_nothing_dc=MULTISPECTRAL_CAMERA_DO_NOTHING,
                                 enter_exit_usb_transfer_dc=MULTISPECTRAL_CAMERA_ENTER_EXIT_USB_TRANSFER,
                                 capture_image_dc=MULTISPECTRAL_CAMERA_CAPTURE_IMAGE, 
                                 rgn_camera_path_indicator=RGN_CAMERA_PATH_INDICATOR,
                                 re_camera_path_indicator=RE_CAMERA_PATH_INDICATOR)
pulse_generator.start_pwm()
data_copier = DataCopier(rgn_camera_files_directory=RGN_CAMERA_FILES_DIRECTORY,
                         re_camera_files_directory=RE_CAMERA_FILES_DIRECTORY,
                         rgn_image_filename=MULTISPECTRAL_IMAGES_NAMES[0],
                         re_image_filename=MULTISPECTRAL_IMAGES_NAMES[1])
mongodb_communicator = MongoDBCommunicator(mongodb_host=MONGODB_HOST, mongodb_port=MONGODB_PORT)
vpn_connector = VPNConnector(server_host=SERVER_HOST, vpn_connection_file_location=VPN_CONNECTION_FILE_LOCATION,
                             vpn_connection_file=VPN_CONNECTION_FILE)
connected_to_vpn, connecting_to_vpn_msg = vpn_connector.maybe_connect_to_vpn()
print(connecting_to_vpn_msg)
data_uploader = DataUploader(server_host=SERVER_HOST, server_username=SERVER_USERNAME, server_password=SERVER_PASSWORD)
# It is a flag for coordinating data visualization and rain system processes.
is_visualization_channel_busy = False


def collect_data_for_visualization():
    """Collects data from field sensors and sends it to Thingworx for real-time visualization."""
    global is_visualization_channel_busy
    is_visualization_channel_busy = True
    for command in DATA_COLLECTION_SEQUENCE:
        data_length = ARDUINO_COMMAND_DATA_LENGTH[command]
        if command is not DATA_COLLECTION_SEQUENCE[NUMBER_OF_LOTS]:
            arduino_response = arduino_1_communicator.write_to_arduino(command=command, data_length=data_length)
        else:
            arduino_response = arduino_2_communicator.write_to_arduino(command=command, data_length=data_length)
        data_dictionary = data_structurer.structure_data(command=command, data=arduino_response)
        if vpn_connector.is_host_active(vpn_connector.GOOGLE_HOST):
            thingworx_communicator.structure_and_post_data(command=command, data=data_dictionary)
    is_visualization_channel_busy = False


def collect_partial_data_for_storage():
    """Collects data from field sensors, stores it locally and saves it remotely."""
    current_timestamp = dt.datetime.utcnow()
    current_timestamp_as_string = data_subdirectory_creator.timestamp_to_string(current_timestamp)
    main_data_subdir, data_subdirs = data_subdirectory_creator.create_data_subdirectories(current_timestamp)
    lot_data_document_list = list()
    for index in range(len(DATA_COLLECTION_SEQUENCE)):
        command = DATA_COLLECTION_SEQUENCE[index]
        data_length = ARDUINO_COMMAND_DATA_LENGTH[command]
        if command is not DATA_COLLECTION_SEQUENCE[NUMBER_OF_LOTS]:
            arduino_response = arduino_1_communicator.write_to_arduino(command=command, data_length=data_length)
            data_dictionary = data_structurer.structure_data(command=command, data=arduino_response)
            lot_data_document_list.append(data_dictionary)
            document_local_writer.write_document_to_file(document_path=data_subdirs[index], command=command,
                                                         document=data_dictionary,
                                                         timestamp=current_timestamp_as_string)
        else:
            arduino_response = arduino_2_communicator.write_to_arduino(command=command, data_length=data_length)
            data_dictionary = data_structurer.structure_data(command=command, data=arduino_response)
            general_data_document = data_dictionary
            document_local_writer.write_document_to_file(document_path=data_subdirs[NUMBER_OF_LOTS], command=command,
                                                         document=data_dictionary,
                                                         timestamp=current_timestamp_as_string)
        if vpn_connector.is_host_active(vpn_connector.GOOGLE_HOST):
            thingworx_communicator.structure_and_post_data(command=command, data=data_dictionary)
    if vpn_connector.check_vpn_connection():
        mongodb_communicator.insert_document_list(db_name=DB_NAME, collection=DB_COLLECTION_LOT_DATA,
                                                  document_list=lot_data_document_list, timestamp=current_timestamp)
        mongodb_communicator.insert_document(db_name=DB_NAME, collection=DB_COLLECTION_GENERAL_DATA,
                                             document=general_data_document, timestamp=current_timestamp)
        data_uploader.save_data_remotely(local_path=main_data_subdir,
                                         total_number_of_files=PACKAGE_PARTIAL_NUMBER_OF_FILES,
                                         destination_directory=SERVER_DESTINATION_DIRECTORY)
    else:
        print("Data could not be saved remotely.")


def collect_total_data_for_storage():
    """
    Collects data from field sensors and captures RGB and multispectral images, stores all data locally and saves it 
    remotely.
    """
    current_timestamp = dt.datetime.utcnow()
    current_timestamp_as_string = data_subdirectory_creator.timestamp_to_string(current_timestamp)
    main_data_subdir, data_subdirs = data_subdirectory_creator.create_data_subdirectories(current_timestamp)
    lot_data_document_list = list()
    for index in range(len(DATA_COLLECTION_SEQUENCE)):
        command = DATA_COLLECTION_SEQUENCE[index]
        if command is not DATA_COLLECTION_SEQUENCE[NUMBER_OF_LOTS]:
            subsequence = DATA_COLLECTION_SUBSEQUENCES[command]
            subsequence_command = subsequence[0]
            data_length = ARDUINO_COMMAND_DATA_LENGTH[subsequence_command]
            arduino_response = arduino_2_communicator.write_to_arduino(command=subsequence_command,
                                                                       data_length=data_length)
            data_dictionary = data_structurer.structure_data(command=subsequence_command, data=arduino_response)
            if vpn_connector.is_host_active(vpn_connector.GOOGLE_HOST):
                thingworx_communicator.structure_and_post_data(command=subsequence_command, data=data_dictionary)
            total_data_subsequence_command = subsequence[1]
            data_length = ARDUINO_COMMAND_DATA_LENGTH[total_data_subsequence_command]
            arduino_response = arduino_1_communicator.write_to_arduino(command=total_data_subsequence_command,
                                                                       data_length=data_length)
            total_data_dictionary = data_structurer.structure_data(command=total_data_subsequence_command,
                                                                   data=arduino_response)
            if vpn_connector.is_host_active(vpn_connector.GOOGLE_HOST):
                thingworx_communicator.structure_and_post_data(command=total_data_subsequence_command,
                                                               data=total_data_dictionary)
            for plant_index in range(NUMBER_OF_PLANTS):
                subsequence_command = subsequence[plant_index + 2]
                data_length = ARDUINO_COMMAND_DATA_LENGTH[subsequence_command]
                arduino_response = arduino_1_communicator.write_to_arduino(command=subsequence_command,
                                                                           data_length=data_length)
                data_dictionary = data_structurer.structure_data(command=subsequence_command, data=arduino_response)
                plant_name = PLANT_NAMES[plant_index]
                _, image_path = image_capturer.try_rgb_image_capture(command=command,
                                                                     image_directory=data_subdirs[index],
                                                                     image_name=plant_name)
                total_data_dictionary[plant_name] = image_path
                if vpn_connector.is_host_active(vpn_connector.GOOGLE_HOST):
                    thingworx_communicator.structure_and_post_data(command=subsequence_command, data=data_dictionary)
            subsequence_command = subsequence[plant_index + 2]
            data_length = ARDUINO_COMMAND_DATA_LENGTH[subsequence_command]
            arduino_response = arduino_1_communicator.write_to_arduino(command=subsequence_command,
                                                                       data_length=data_length)
            data_dictionary = data_structurer.structure_data(command=subsequence_command, data=arduino_response)
            if vpn_connector.is_host_active(vpn_connector.GOOGLE_HOST):
                thingworx_communicator.structure_and_post_data(command=subsequence_command, data=data_dictionary)
            pulse_generator.put_multispectral_cameras_in_capture_mode()
            pulse_generator.capture_image(RGN_CAMERA_PIN)
            pulse_generator.capture_image(RE_CAMERA_PIN)
            pulse_generator.enter_exit_usb_transfer(RGN_CAMERA_PIN)
            multispectral_image_name = MULTISPECTRAL_IMAGES_NAMES[0]
            _, multispectral_image_path = data_copier \
                .copy_latest_multispectral_image_to_destination(destination_directory=data_subdirs[index],
                                                                multispectral_image_name=multispectral_image_name)
            total_data_dictionary[multispectral_image_name] = multispectral_image_path
            pulse_generator.enter_exit_usb_transfer(RGN_CAMERA_PIN)
            pulse_generator.put_multispectral_cameras_in_capture_mode()
            pulse_generator.enter_exit_usb_transfer(RE_CAMERA_PIN)
            multispectral_image_name = MULTISPECTRAL_IMAGES_NAMES[1]
            _, multispectral_image_path = data_copier \
                .copy_latest_multispectral_image_to_destination(destination_directory=data_subdirs[index],
                                                                multispectral_image_name=multispectral_image_name)
            total_data_dictionary[multispectral_image_name] = multispectral_image_path
            pulse_generator.enter_exit_usb_transfer(RE_CAMERA_PIN)
            lot_data_document_list.append(total_data_dictionary)
            document_local_writer.write_document_to_file(document_path=data_subdirs[index],
                                                         command=total_data_subsequence_command,
                                                         document=total_data_dictionary,
                                                         timestamp=current_timestamp_as_string)
        else:
            data_length = ARDUINO_COMMAND_DATA_LENGTH[command]
            arduino_response = arduino_2_communicator.write_to_arduino(command=command, data_length=data_length)
            data_dictionary = data_structurer.structure_data(command=command, data=arduino_response)
            general_data_document = data_dictionary
            document_local_writer.write_document_to_file(document_path=data_subdirs[NUMBER_OF_LOTS], command=command,
                                                         document=data_dictionary,
                                                         timestamp=current_timestamp_as_string)
            if vpn_connector.is_host_active(vpn_connector.GOOGLE_HOST):
                thingworx_communicator.structure_and_post_data(command=command, data=data_dictionary)
    data_length = ARDUINO_COMMAND_DATA_LENGTH[ROTARY_ARM_INITIAL_POSITION]
    arduino_response = arduino_2_communicator.write_to_arduino(command=ROTARY_ARM_INITIAL_POSITION,
                                                               data_length=data_length)
    data_dictionary = data_structurer.structure_data(command=ROTARY_ARM_INITIAL_POSITION, data=arduino_response)
    if vpn_connector.is_host_active(vpn_connector.GOOGLE_HOST):
        thingworx_communicator.structure_and_post_data(command=ROTARY_ARM_INITIAL_POSITION, data=data_dictionary)
    if vpn_connector.check_vpn_connection():
        mongodb_communicator.insert_document_list(db_name=DB_NAME, collection=DB_COLLECTION_LOT_DATA,
                                                  document_list=lot_data_document_list, timestamp=current_timestamp)
        mongodb_communicator.insert_document(db_name=DB_NAME, collection=DB_COLLECTION_GENERAL_DATA,
                                             document=general_data_document, timestamp=current_timestamp)
        data_uploader.save_data_remotely(local_path=main_data_subdir,
                                         total_number_of_files=PACKAGE_TOTAL_NUMBER_OF_FILES,
                                         destination_directory=SERVER_DESTINATION_DIRECTORY)
    else:
        print("Data could not be saved remotely.")


def begin_rain():
    """Starts the rain on the lots."""
    global is_visualization_channel_busy
    while is_visualization_channel_busy:
        # Waits until the visualization channel is not busy before executing the begin_rain process.
        None
    is_visualization_channel_busy = True
    command = RAIN_COMMANDS[0]
    data_length = ARDUINO_COMMAND_DATA_LENGTH[command]
    arduino_response = arduino_2_communicator.write_to_arduino(command=command, data_length=data_length)
    data_dictionary = data_structurer.structure_data(command=command, data=arduino_response)
    if vpn_connector.is_host_active(vpn_connector.GOOGLE_HOST):
        thingworx_communicator.structure_and_post_data(command=command, data=data_dictionary)
    is_visualization_channel_busy = False


def end_rain():
    """Ends the rain on the lots."""
    global is_visualization_channel_busy
    while is_visualization_channel_busy:
        # Waits until the visualization channel is not busy before executing the end_rain process.
        None
    is_visualization_channel_busy = True
    command = RAIN_COMMANDS[1]
    data_length = ARDUINO_COMMAND_DATA_LENGTH[command]
    arduino_response = arduino_2_communicator.write_to_arduino(command=command, data_length=data_length)
    data_dictionary = data_structurer.structure_data(command=command, data=arduino_response)
    if vpn_connector.is_host_active(vpn_connector.GOOGLE_HOST):
        thingworx_communicator.structure_and_post_data(command=command, data=data_dictionary)
    is_visualization_channel_busy = False


# Data collection calendar.
schedule.every().day.at("00:00").do(collect_partial_data_for_storage)
schedule.every().day.at("03:00").do(collect_partial_data_for_storage)
schedule.every().day.at("06:30").do(collect_total_data_for_storage)
schedule.every().day.at("09:00").do(collect_total_data_for_storage)
schedule.every().day.at("12:00").do(collect_total_data_for_storage)
schedule.every().day.at("15:00").do(collect_total_data_for_storage)
schedule.every().day.at("17:30").do(collect_total_data_for_storage)
schedule.every().day.at("21:00").do(collect_partial_data_for_storage)
# Rain calendar.
rain_scheduler = Scheduler()
for rain_day in SEPTEMBER_RAIN_DAYS:
    for rain_time_begin, rain_time_end in RAIN_TIMES:
        run_date_begin = "2018-09-{} {}".format(rain_day, rain_time_begin)
        run_date_end = "2018-09-{} {}".format(rain_day, rain_time_end)
        rain_scheduler.add_job(func=begin_rain, trigger="date", run_date=run_date_begin)
        rain_scheduler.add_job(func=end_rain, trigger="date", run_date=run_date_end)
for rain_day in OCTOBER_RAIN_DAYS:
    for rain_time_begin, rain_time_end in RAIN_TIMES:
        run_date_begin = "2018-10-{} {}".format(rain_day, rain_time_begin)
        run_date_end = "2018-10-{} {}".format(rain_day, rain_time_end)
        rain_scheduler.add_job(func=begin_rain, trigger="date", run_date=run_date_begin)
        rain_scheduler.add_job(func=end_rain, trigger="date", run_date=run_date_end)
for rain_day in NOVEMBER_RAIN_DAYS:
    for rain_time_begin, rain_time_end in RAIN_TIMES:
        run_date_begin = "2018-11-{} {}".format(rain_day, rain_time_begin)
        run_date_end = "2018-11-{} {}".format(rain_day, rain_time_end)
        rain_scheduler.add_job(func=begin_rain, trigger="date", run_date=run_date_begin)
        rain_scheduler.add_job(func=end_rain, trigger="date", run_date=run_date_end)
rain_scheduler.start()

while True:
    schedule.run_pending()
    if not is_visualization_channel_busy:
        collect_data_for_visualization()
    sleep(1)
