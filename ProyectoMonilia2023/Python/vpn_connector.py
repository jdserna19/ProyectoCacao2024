import os
import subprocess
from time import sleep


class VPNConnector:
    GOOGLE_HOST = "www.google.com"
    HOST_ACTIVE_STATUS = 0
    ATTEMPTS_TIMEOUT = 60
    INTERVAL_BTW_ATTEMPTS = 5

    def __init__(self, server_host, vpn_connection_file_location, vpn_connection_file):
        self.server_host = server_host
        self.vpn_connection_file_location = vpn_connection_file_location
        self.vpn_connection_file = vpn_connection_file

    def maybe_connect_to_vpn(self):
        """Tries to connect to the VPN."""
        if self.is_host_active(self.GOOGLE_HOST):
            if self.is_host_active(self.server_host):
                # The connection to the VPN was already established.
                connected_to_vpn = True
                connecting_to_vpn_msg = "Connected to the VPN."
            else:
                # It is possible and necessary to connect to the VPN.
                self.connect_to_vpn()
                connected_to_vpn = True
                connecting_to_vpn_msg = "Connected to the VPN."
        else:
            # It is not possible to connect to the VPN.
            connected_to_vpn = False
            connecting_to_vpn_msg = "Connecting to the VPN is not possible."
        return connected_to_vpn, connecting_to_vpn_msg

    def check_vpn_connection(self):
        """
        Checks whether the VPN connection is already established and attempts to establish it several times if not.
        """
        number_of_attempts = int(self.ATTEMPTS_TIMEOUT / self.INTERVAL_BTW_ATTEMPTS)
        for _ in range(number_of_attempts):
            connected_to_vpn, connecting_to_vpn_msg = self.maybe_connect_to_vpn()
            print(connecting_to_vpn_msg)
            if connected_to_vpn:
                break
            sleep(self.INTERVAL_BTW_ATTEMPTS)
        if not connected_to_vpn:
            print("After several attempts, it was not possible to connect to the VPN.")
        return connected_to_vpn

    def is_host_active(self, host):
        """Checks whether the given host is reachable or not."""
        ping_result = os.system("ping -c 1 {}".format(host))
        if ping_result is self.HOST_ACTIVE_STATUS:
            host_active = True
        else:
            host_active = False
        return host_active

    def connect_to_vpn(self):
        """Executes the script to connect to the VPN as a subprocess."""
        except_cmd = "./{}".format(self.vpn_connection_file)
        # 'cwd' specifies the current working directory.
        subprocess.Popen(args=[except_cmd], cwd=self.vpn_connection_file_location)
