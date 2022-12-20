#! /usr/bin/python3

from scapy.all import *
from .PlatformConstants import LINE_SEP as lsep, SEP as sep
from .ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from .TypeTester import (
    arg_is_a_dict as aiad,
    arg_is_a_list as aial,
    arg_is_a_tuple as aiat,
    arg_is_a_function as aiaf,
)
from .Utils import aiad, aial, clear_screen as clear
from .PatternConstants import valid_ipv4 as vip, valid_mac as vma

cus = cms["custom"]


""" Gets the local network interface's route. 
    List: Network Interface Name, it's address and the gateway.
    Returns: DataFrame
"""


def get_routing_table():
    route_info = conf.route.route()
    interface = route_info[0]
    address = route_info[1]
    gateway = route_info[2]

    data = {"interface": interface, "address": address, "gateway": gateway}

    return data


""" Prints the local network interface's route.
    Prints DataFrame
"""


def print_routing_table():
    route_info = conf.route.route()
    interface = route_info[0]
    address = route_info[1]
    gateway = route_info[2]

    data = {"Interface": interface, "Address": address, "Gateway": gateway}

    if aiad(data):
        pdv(data)


""" Returns the network interface's name
    Returns: string
"""


def get_network_interface_name():
    return conf.iface


""" Prints the network interface's name """


def print_network_interface_name():
    print("\n{}".format(conf.iface))


""" Prints the network interface's hardware address """


def print_network_interface_hardware_address():
    print("{}".format(get_if_hwaddr(conf.iface)))


""" Returns the network interface's hardware address
    Returns: str
"""


def get_network_interface_hardware_address():
    return get_if_hwaddr(conf.iface)


""" Prints arp who-has response
    @Param destination: response destination
    @Param target: IP or range
    @Param verbose: Increase verbosity output
    @Param timeout: Time in seconds to scan
"""


def _arp_who_has(destination=None, target=None, verbose=None, timeout=None):
    _dst = "ff:ff:ff:ff:ff:ff"
    _tgt = "192.168.1.1/24"
    _verbose = 0
    _timeout = 2
    results = None
    clients = []

    if not destination == None:
        _dst = destination

    if not target == None:
        _tgt = target

    if not verbose == None:
        _verbose = verbose

    if not timeout == None:
        _timeout = timeout

    if verbose == 0:
        v_msg_header = cus(255, 255, 255, "ARPing")
        v_msg_body = cus(245, 245, 255, "Target: {} Destination: {}".format(_tgt, _dst))
        v_msg = "{} {}".format(v_msg_header, v_msg_body)
        print("{}\n".format(v_msg))

    packet = Ether(dst=_dst) / ARP(pdst=_tgt)

    results = srp(packet, timeout=_timeout, verbose=_verbose)[0]

    if not results == None:
        for sent, recv in results:
            clients.append({"ip": str(recv.psrc), "mac": str(recv.hwsrc)})

    if len(clients) > 0:
        return {
            "status": True,
            "clients": clients,
            "msg": "Found {} devices on the network".format(len(clients)),
        }

    return {"status": False, "reason": "Could not detect any devices on the network"}
