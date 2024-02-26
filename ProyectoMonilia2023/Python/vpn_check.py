import os


class VPNCheck:
    GOOGLE_HOST = "www.google.com"
    HOSTNAME = "192.168.10.115"
    HOST_ACTIVE_STATUS = 0
    VPN_CONNECTION_FILE_LOCATION = "/home/pi/Documents/vpn"
    VPN_CONNECTION_FILE = "vpn_connection.exp"

    def __init__(self):
        None

    def can_connect_to_vpn(self):
        """Checks whether it is possible and necessary to connect to the VPN."""
        if self.is_host_active(self.GOOGLE_HOST):
            if self.is_host_active(self.HOSTNAME):
                # The connection to the VPN was already established.
                connect_to_vpn = False
                connecting_to_vpn_msg = "Connecting to the VPN is not necessary."
            else:
                # It is possible and necessary to connect to the VPN.
                connect_to_vpn = True
                connecting_to_vpn_msg = "Connecting to the VPN..."
        else:
            # It is not possible to connect to the VPN.
            connect_to_vpn = False
            connecting_to_vpn_msg = "Connecting to the VPN is not possible."
        return connect_to_vpn, connecting_to_vpn_msg

    def is_host_active(self, host):
        """Checks wheter the given host is reachable or not."""
        ping_result = os.system("ping -c 1 " + host)
        if ping_result is self.HOST_ACTIVE_STATUS:
            host_active = True
        else:
            host_active = False
        return host_active

    def connect_to_vpn(self):
        """Executes the script to connect to the VPN."""
        cd_cmd = "cd " + self.VPN_CONNECTION_FILE_LOCATION
        except_cmd = "./" + self.VPN_CONNECTION_FILE
        os.system(cd_cmd + " && " + except_cmd)
