import os
import paramiko


class ImageTransfer:
    IMAGES_ROOT_DIRECTORY = "images/"
    HOSTNAME = "192.168.10.115"
    USERNAME = "asanch41"
    PASSWORD = ""
    # PRIVATE_KEY = paramiko.RSAKey.from_private_key_file("/home/pi/.ssh/id_rsa")
    HOST_DIRECTORY = "/home/asanch41/Documents/coffee_leaf_rust_diagnosis/"
    HOST_IMAGES_DIRECTORY = HOST_DIRECTORY + IMAGES_ROOT_DIRECTORY

    def __init__(self):
        self.remote_img_dir_created = False

    def get_ssh_connection(self):
        """Connects with the server via SSH and returns the SSH connection."""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        try:
            ssh.connect(hostname=self.HOSTNAME, username=self.USERNAME, password=self.PASSWORD)
            print("SSH connection with the server successfully established.")
        except:
            ssh = None
            print("Error establishing SSH connection with the server.")
        return ssh

    def close_ssh_connection(self, ssh):
        """Closes the SSH connection."""
        if ssh is not None:
            ssh.close()

    def close_sftp_connection(self, sftp):
        """Closes the SFTP connection."""
        if sftp is not None:
            sftp.close()

    def create_img_directory_in_server(self, current_img_directory):
        """Creates the given directory in the server to allow the captured images uploading."""
        if not self.remote_img_dir_created:
            ssh = self.get_ssh_connection()
            sftp = None
            try:
                sftp = ssh.open_sftp()
                sftp.mkdir(self.HOST_IMAGES_DIRECTORY + current_img_directory)
                # The image directory was successfully created in the remote server.
                self.remote_img_dir_created = True
                print("The image directory was successfully created in the remote server.")
                self.close_sftp_connection(sftp)
                self.close_ssh_connection(ssh)
            except:
                self.close_sftp_connection(sftp)
                self.close_ssh_connection(ssh)
                print("The image directory couldn't be created in the remote server.")

    def upload_img_to_server(self, file_to_upload, current_img_directory, filename):
        """Uploads the captured image to the server via SFTP for posterior processing."""
        ssh = self.get_ssh_connection()
        sftp = None
        try:
            sftp = ssh.open_sftp()
            sftp.put(localpath=file_to_upload, remotepath=self.HOST_IMAGES_DIRECTORY + current_img_directory + filename)
            # The image was successfully sent to the remote server.
            print(filename + " saved remotely.")
            self.close_sftp_connection(sftp)
            self.close_ssh_connection(ssh)
        except:
            self.close_sftp_connection(sftp)
            self.close_ssh_connection(ssh)
            print("The image \"" + filename + "\" couldn't be sent to the remote server.")
