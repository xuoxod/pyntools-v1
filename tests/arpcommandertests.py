#! /usr/bin/python3

from custom_modules.ArgumentManager import filtered, filtered_count
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.ArpCommander import (
    get_network_interface_hardware_address as mac,
    get_network_interface_name as iface_name,
    get_routing_table as routing,
)

print("MAC:\t{}".format(mac()))

print("Iface:\t{}".format(iface_name()))

print("Route:")

print(*routing().items(), sep="\n")
