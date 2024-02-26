from image_transfer import ImageTransfer

FILE_TO_UPLOAD = "images/11062018170000/IMG_180509_203356_0000_RGB.JPG"
CURRENT_IMAGE_DIRECTORY = "11062018170000/"
FILENAME = "IMG_180509_203356_0000_RGB.JPG"

# Creates the image directory in the server and transfers one image to it.
image_transfer = ImageTransfer()
image_transfer.create_img_directory_in_server(CURRENT_IMAGE_DIRECTORY)
image_transfer.upload_img_to_server(file_to_upload=FILE_TO_UPLOAD,
                                    current_img_directory=CURRENT_IMAGE_DIRECTORY,
                                    filename=FILENAME)
