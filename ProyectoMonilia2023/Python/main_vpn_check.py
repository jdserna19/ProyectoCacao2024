from vpn_check import VPNCheck

# Connects to the VPN if it's possible and necessary.
vpn_check = VPNCheck()
connect_to_vpn, connecting_to_vpn_msg = vpn_check.can_connect_to_vpn()
print(connecting_to_vpn_msg)
if connect_to_vpn:
    vpn_check.connect_to_vpn()
