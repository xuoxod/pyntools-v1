#! /usr/bin/python

import logging
from scapy.all import *
from .ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from .Flags import FLAGS as _flags
from .PatternConstants import (
    valid_ipv4 as vip4,
    is_a_number as isnum,
    is_port_range as isportrange,
    is_a_number_or_float as isnumorfloat,
)
from .TypeTester import (
    arg_is_an_int as aiai,
    arg_is_none as ain,
    arg_is_a_dict as aiad,
    arg_is_a_tuple as aiat,
    arg_is_a_list as aial,
)


logging.basicConfig(filemode="scapy-info-log", level=logging.INFO)
logging.basicConfig(filemode="scapy-warning-log", level=logging.WARNING)
logging.basicConfig(filemode="scapy-error-log", level=logging.ERROR)
logging.basicConfig(filemode="scapy-critical-log", level=logging.CRITICAL)

cus = cms["custom"]

""" Send TCP packet 
    @param obj_packet: A Scapy packet
"""


def send_tcp_packet(obj_packet):
    _dst = obj_packet["_dst"]
    _sport = obj_packet["_src_port"]
    _dport = obj_packet["_dst_port"]
    _flag = obj_packet["_flag"]
    _timeout = obj_packet["_timeout"]

    results = sr(
        IP(dst=_dst) / TCP(sport=int(_sport), dport=int(_dport)),
        timeout=int(_timeout),
    )

    print(results)
    # sr1(IP(dst="192.168.1.1")/TCP(sport=5000,dport=6000,flags="A"),timeout=4)


""" Prepare TCP packet 
    @param host: The target host
    @param port: The target's port
    @param flag: The packet flag
    @param timeout: The number of seconds before giving up
"""


def stage_sender(obj_data=None):
    logging.info("Method stage_send invoked\n")
    _host = None
    _port = None
    _flag = None
    _timeout = None
    _src_port = RandShort()

    """ Validate parameters """

    validate_mandatory_parameters(obj_data)

    _timeout = validate_optional_parameters(obj_data) or 10
    _host = obj_data["host"]
    _port = obj_data["port"]
    _flag = _flags[obj_data["flag"]]
    packet = {
        "_dst": _host,
        "_src_port": _src_port,
        "_dst_port": _port,
        "_flag": _flag,
        "_timeout": _timeout,
    }

    if "verbose" in obj_data and obj_data["verbose"]:
        print(
            "Packet parameters:\n\tHost: {}\n\tPort: {}\n\tFlag: {}\n\tTimeout: {}\n".format(
                _host, _port, _flag, _timeout
            )
        )

    send_tcp_packet(packet)


def validate_optional_parameters(obj_data):
    if "timeout" in obj_data:
        timeout = obj_data["timeout"]
        if isnumorfloat(timeout):
            return timeout
    return None


def validate_mandatory_parameters(objData):
    if objData == None:
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(255, 255, 255, "Expecting a dict but received nothing")
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)

    if "host" not in objData:
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

    if not vip4(host):
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(
            255,
            255,
            255,
            "Expected a valid IPv4 host address but received [{}]".format(host),
        )
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)

    if "port" not in objData:
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

    if not isnum(port):
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(
            255,
            255,
            255,
            "Expected a valid port number but received [{}]".format(port),
        )
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)

    if "flag" not in objData:
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(
            255,
            255,
            255,
            "Expected a flag key in the dict parameter but received nothing",
        )
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)

    flag = objData["flag"]

    if flag not in _flags:
        e_msg_header = cus(255, 112, 112, "Error")
        e_msg_body = cus(
            255,
            255,
            255,
            "Expected a valid flag but [{}] is not available".format(flag),
        )
        e_msg = "{} {}".format(e_msg_header, e_msg_body)
        raise ValueError(e_msg)
