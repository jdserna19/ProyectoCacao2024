import os
import paramiko
from time import sleep


class DataUploader:
    ATTEMPTS_TIMEOUT = 60
    INTERVAL_BTW_ATTEMPTS = 5
    SSH_CONNECTION_TIMEOUT = 5

    def __init__(self, server_host, server_username, server_password):
        self.host = server_host
        self.username = server_username
        self.password = server_password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))

    def open_sftp_session(self):
        """Connects to the server via SSH, opens a SFTP session and returns it."""
        try:
            self.ssh.connect(hostname=self.host, username=self.username, password=self.password,
                             timeout=self.SSH_CONNECTION_TIMEOUT, banner_timeout=self.SSH_CONNECTION_TIMEOUT,
                             auth_timeout=self.SSH_CONNECTION_TIMEOUT)
            # Tries to execute a simple command on the SSH connection to verify whether it is alive or not before
            # opening the SFTP session.
            self.ssh.exec_command(command='ls', timeout=self.SSH_CONNECTION_TIMEOUT)
            sftp = self.ssh.open_sftp()
            # Sets a timeout for SFTP operations.
            sftp.get_channel().settimeout(self.SSH_CONNECTION_TIMEOUT)
        except:
            # The SFTP session could not be opened.
            sftp = None
            print("Error opening SFTP session on the server.")
        return sftp

    def close_sftp_session(self, sftp):
        """Closes the SFTP session including the SSH connection."""
        self.ssh.close()
        if sftp is not None:
            sftp.close()

    def save_data_remotely(self, local_path, total_number_of_files, destination_directory):
        """
        Uploads every directory and file in the given local path to the server via SFTP in order to store the data
        remotely.
        """
        number_of_attempts = int(self.ATTEMPTS_TIMEOUT / self.INTERVAL_BTW_ATTEMPTS)
        number_of_uploaded_files = 0
        created_directories = list()
        uploaded_files = list()
        is_total_number_of_files_uploaded = False
        for _ in range(number_of_attempts):
            if number_of_uploaded_files == total_number_of_files:
                # The whole data has been uploaded successfully.
                is_total_number_of_files_uploaded = True
                break
            else:
                for subdir, dirs, files in os.walk(local_path):
                    if subdir not in created_directories:
                        sftp = self.open_sftp_session()
                        try:
                            sftp.mkdir("{}{}".format(destination_directory, subdir))
                            '''
                            The directory was successfully created in the server and it is added to the created
                            directories.
                            '''
                            created_directories.append(subdir)
                            self.close_sftp_session(sftp)
                        except:
                            # The directory could not be created in the server.
                            self.close_sftp_session(sftp)
                            print("The directory {} could not be created in the server.".format(subdir))
                    for file in files:
                        # Iterates over every file inside the current subdirectory.
                        file_path = os.path.join(subdir, file)
                        if file_path not in uploaded_files:
                            sftp = self.open_sftp_session()
                            try:
                                sftp.put(localpath=file_path,
                                         remotepath="{}{}".format(destination_directory, file_path))
                                '''
                                The file was successfully uploaded to the server and it is added to the uploaded
                                files.
                                '''
                                uploaded_files.append(file_path)
                                self.close_sftp_session(sftp)
                            except:
                                # The file could not be uploaded to the server.
                                self.close_sftp_session(sftp)
                                print("The file {} could not be uploaded to the server.".format(file_path))
            number_of_uploaded_files = len(uploaded_files)
            # Waits for an interval before executing the next attempt.
            sleep(self.INTERVAL_BTW_ATTEMPTS)
        '''
        This verification is necessary because the whole data could have been successfully uploaded at the last
        attempt.
        '''
        if number_of_uploaded_files == total_number_of_files:
            # The whole data has been uploaded successfully.
            is_total_number_of_files_uploaded = True
        else:
            # Some files could not be uploaded to the server.
            print("{}/{} files were successfully uploaded to the server.".format(number_of_uploaded_files,
                                                                                 total_number_of_files))
        return is_total_number_of_files_uploaded
