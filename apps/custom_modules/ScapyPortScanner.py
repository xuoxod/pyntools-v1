from scapy.all import *
from .ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from .PatternConstants import (
    valid_ipv4 as vip4,
    valid_network_range as vnr,
    is_port_range as isportrange,
    is_a_number as isanum,
)
from .TypeTester import arg_is_a_dict as isadict, arg_is_a_string, arg_is_an_int

import logging


logging.basicConfig(filemode="scapy-info-log", level=logging.INFO)
logging.basicConfig(filemode="scapy-warning-log", level=logging.WARNING)
logging.basicConfig(filemode="scapy-error-log", level=logging.ERROR)
logging.basicConfig(filemode="scapy-critical-log", level=logging.CRITICAL)

cus = cms["custom"]

""" Configure the port """


def config_port(port):
    if arg_is_an_int(port):
        port = str(port)

    if "," in port:
        ports = port.split(",")
        sport = ports[0]
        eport = ports[1]
        return {"type": "range", "sport": int(sport), "eport": int(eport)}
    elif "-" in port:
        ports = port.split("-")
        sport = ports[0]
        eport = ports[1]
        return {"type": "range", "sport": int(sport), "eport": int(eport)}
    else:
        return {"type": "integer", "port": int(port)}


""" Scan host  """


def scan_host(host, port):
    # ans,unans = sr(IP(dst="{}".format(ip))/TCP(flags="S",dport=(1,2048)))
    # ans.nsummary( lfilter=lambda (s,r): (r.haslayer(TCP) and (r.getlayer(TCP).flags & 2)) )

    ports = config_port(port)
    _type = ports["type"]

    if _type.strip() == "range":
        sport = ports["sport"]
        eport = ports["eport"]
        port_range = (
            sport,
            eport,
        )
        print(
            "Packet Data: \n\tHost: {}\n\tPort: {}".format(
                host,
                port_range,
            )
        )

        ans, unans = sr(IP(dst="{}".format(host)) / TCP(flags="S", dport=port_range))
        return ans, unans
    else:
        port = ports["port"]

        ans, unans = sr(IP(dst="{}".format(host)) / TCP(flags="S", dport=port))
        return ans, unans


""" Prepare TCP packet 
    @param host: The target host
    @param port: The target's port
"""


def prepare_packet(obj_data):
    validate_mandatory_parameters(obj_data)

    host = obj_data["host"]
    port = obj_data["port"]

    return scan_host(host, port)


def validate_mandatory_parameters(objData):
    if objData == None:
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(255, 255, 255, "Expecting a dict but received nothing")
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)

    if not isadict(objData):
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(
            255, 255, 255, "Expecting a dict but received [{}]".format(type(objData))
        )
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)

    if "host" not in objData or len(objData["host"]) == 0:
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(
            255,
            255,
            255,
            "Expected a host key in the dict parameter but received nothing",
        )
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)

    host = objData["host"]

    if not vip4(host) and not vnr(host):
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(
            255,
            255,
            255,
            "Expected a valid IPv4 host address or a network range address but received [{}]".format(
                host
            ),
        )
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)

    if "port" not in objData or len(str(objData["port"])) == 0:
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(
            255,
            255,
            255,
            "Expected a port key in the dict parameter but received nothing",
        )
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)

    port = objData["port"]

    if not isanum(port) and not isportrange(port):
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(
            255,
            255,
            255,
            "Expected a valid port number but received [{}]".format(port),
        )
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)
