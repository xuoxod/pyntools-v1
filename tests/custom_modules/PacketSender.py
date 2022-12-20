#! /usr/bin/python

import logging
from scapy.all import *
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.Flags import FLAGS as flags
from custom_modules.PatternConstants import valid_ipv4 as vip4
from custom_modules.TypeTester import (
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


def send_pkt(host=None, port=None, flag=None, timeout=None):
    logging.info("Method send_pkt called\n")
    _host = None
    _port = None
    _flag = None
    _timeout = 10
    _src_port = RandShort()

    if not timeout == None and aiai(timeout):
        _timeout = timeout

    if not flag == None:
        try:
            _flag = flags[flag]
        except KeyError as ke:
            msg = "Key [{}] does not exist".format(ke)
            msg_header = cus(255, 88, 88, "Error:")
            c_msg = cus(255, 255, 255, msg)
            error_msg = "{}\t{}".format(msg_header, c_msg)

            raise ValueError(error_msg)

    if host == None:
        msg = "Expected a host address but received [{}]".format(host)
        msg_header = cus(255, 88, 88, "Error:")
        c_msg = cus(255, 255, 255, msg)
        error_msg = "{}\t{}".format(msg_header, c_msg)

        raise ValueError(("{}".format(error_msg)))

    if port == None:
        msg = "Expected a port number but received [{}]".format(port)
        msg_header = cus(255, 88, 88, "Error:")
        c_msg = cus(255, 255, 255, msg)
        error_msg = "{}\t{}".format(msg_header, c_msg)

        raise ValueError(("{}".format(error_msg)))

    if not vip4(host):
        msg = "Expected a IPv4 host address but received [{}]".format(host)
        msg_header = cus(255, 88, 88, "Error:")
        c_msg = cus(255, 255, 255, msg)
        error_msg = "{}\t{}".format(msg_header, c_msg)

        raise ValueError(("{}".format(error_msg)))

    if not aiai(port):
        msg = "Expected a valid integer port number but received [{}]".format(port)
        msg_header = cus(255, 88, 88, "Error:")
        c_msg = cus(255, 255, 255, msg)
        error_msg = "{}\t{}".format(msg_header, c_msg)

        raise ValueError(("{}".format(error_msg)))

    if _flag == None:
        _flag = flags["s"]

    _host = host
    _port = port

    tcp_connect_scan_resp = sr1(
        IP(dst=_host) / TCP(sport=_src_port, dport=_port, flags=_flag),
        timeout=_timeout,
    )

    if ain(tcp_connect_scan_resp):
        print("Closed")

    elif not ain(tcp_connect_scan_resp):
        print("\n\n{}\n\n".format(tcp_connect_scan_resp))

        # if tcp_connect_scan_resp.getlayer(IP):
        # print("IP Layer: {}".format(tcp_connect_scan_resp.getlayer(IP)))

        if tcp_connect_scan_resp.haslayer(TCP):
            # print("TCP Layer: {}".format(tcp_connect_scan_resp.getlayer(TCP)))

            if tcp_connect_scan_resp.getlayer(TCP).flags == 0x12:
                print("TCP Flags: {}".format(tcp_connect_scan_resp.getlayer(TCP).flags))

                send_rst = sr(
                    IP(dst=_host) / TCP(sport=_src_port, dport=_port, flags="AR"),
                    timeout=_timeout,
                )

                print(send_rst)

                print("Port {} is open".format(_port))
                return True
            elif tcp_connect_scan_resp.getlayer(TCP).flags == 0x14:
                print("Port {} is closed off".format(_port))
            else:
                print("Port {} is closed".format(_port))
    return False
