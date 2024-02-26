from time import time
import shutil
import glob
import os


class DataCopier:
    MULTISPECTRAL_IMAGES_FILE_EXTENSION = ".JPG"
    COPY_TIME = 3

    def __init__(self, rgn_camera_files_directory, re_camera_files_directory, rgn_image_filename, re_image_filename):
        self.rgn_camera_files_directory = rgn_camera_files_directory
        self.re_camera_files_directory = re_camera_files_directory
        self.rgn_image_filename = rgn_image_filename
        self.re_image_filename = re_image_filename

    def get_path_to_latest_image(self, directory):
        """Returns the path to the latest multispectral image inside the given directory."""
        list_of_images = glob.iglob("{}*{}".format(directory, self.MULTISPECTRAL_IMAGES_FILE_EXTENSION))
        try:
            latest_image = max(list_of_images, key=os.path.getctime)
        except:
            latest_image = None
            print("No image with the {} extension was found inside the given directory."
                  .format(self.MULTISPECTRAL_IMAGES_FILE_EXTENSION))
        return latest_image

    def copy_latest_multispectral_image_to_destination(self, destination_directory, multispectral_image_name):
        """Copies the latest multispectral image to the given destination using a simpler name."""
        try:
            if multispectral_image_name is self.rgn_image_filename:
                image_destination = "{}{}{}".format(destination_directory, self.rgn_image_filename,
                                                    self.MULTISPECTRAL_IMAGES_FILE_EXTENSION)
                shutil.copy2(self.get_path_to_latest_image(self.rgn_camera_files_directory), image_destination)
            else:
                image_destination = "{}{}{}".format(destination_directory, self.re_image_filename,
                                                    self.MULTISPECTRAL_IMAGES_FILE_EXTENSION)
                shutil.copy2(self.get_path_to_latest_image(self.re_camera_files_directory), image_destination)
            is_image_copied = True
        except:
            is_image_copied = False
            print("The multispectral image could not be copied to the given destination.")
        # Waits for the given time before finishing the copy process.
        initial_time = time()    
        while (time() - initial_time) < self.COPY_TIME:
            None
        return is_image_copied, image_destination
