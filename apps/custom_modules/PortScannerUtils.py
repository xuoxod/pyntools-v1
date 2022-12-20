import sys
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.TypeTester import arg_is_an_int as aiai, arg_is_none as ain
from custom_modules.PatternConstants import (
    valid_ipv4 as vip4,
    valid_network_range as vnr,
    has_char,
    is_a_number_or_float as ianof,
    is_a_number as ian,
    is_port_range as ipr,
)

cus = cms["custom"]
host_address_e_msg_header = cus(255, 90, 90, "IP Address Error:")
port_e_msg_header = cus(255, 90, 90, "Port Error:")
network_address_e_msg_header = cus(255, 90, 90, "Network Range Error:")

empty_host = "Expected a valid IP address but received nothing"
invalid_host = "Expected an IP address but received "
empty_port = "Expected either an integer or integer range. e.g. 13 or 44-200 but receiced nothing"
invalid_port = "Expected an integer but received ["
invalid_port_range_number = "Expected an integer or a range e.g. 1-33, but received"
invalid_port_range = "The end range must be larger than the start range"
empty_network = "Expected a network range but received nothing"
invalid_network = "Expected a network range - e.g. 10.1.10.1/8 but received "


def make_msg_body(words):
    return cus(255, 255, 255, words)


def exit_prog(exit_code=0):
    sys.exit(exit_code)


def test_port_arg(port):
    if "-" not in port and ain(port):
        e_msg_body = make_msg_body(empty_port)
        e_msg = "{}\t{}".format(port_e_msg_header, e_msg_body)
        print("{}".format(e_msg))
        exit_prog()
    elif "-" not in port:
        try:
            port = int(port)
        except ValueError:
            e_msg_body = make_msg_body("{}{}]".format(invalid_port, port))
            e_msg = "{}\t{}".format(port_e_msg_header, e_msg_body)
            print("{}".format(e_msg))
            exit_prog()

    elif "-" in port:
        port_split = port.split("-")
        sport = port_split[0]
        eport = port_split[1]

        try:
            sport = int(sport)
            eport = int(eport)

            if sport > eport:
                e_msg_body = make_msg_body(invalid_port_range)
                e_msg = "{}\t{}".format(port_e_msg_header, e_msg_body)
                print("{}".format(e_msg))
                exit_prog()

        except ValueError:
            e_msg_body = make_msg_body("{}{}".format(invalid_port_range_number, port))
            e_msg = "{} {}".format(port_e_msg_header, e_msg_body)
            print("{}".format(e_msg))
            exit_prog()
    return True


def test_network_address(network):
    if ain(network):
        e_msg_body = make_msg_body(empty_network)
        e_msg = "{}\t[{}".format(network_address_e_msg_header, e_msg_body)
        print("{}".format(e_msg))
        exit_prog()
    elif not vnr(network):
        e_msg_body = make_msg_body("{} {}".format(invalid_network, network))
        e_msg = "{}\t{}".format(network_address_e_msg_header, e_msg_body)
        print("{}".format(e_msg))
        exit_prog()

    return True


def test_host_address(host):
    if ain(host):
        e_msg_body = make_msg_body(empty_host)
        e_msg = "{}\t{}".format(host_address_e_msg_header, e_msg_body)
        print("{}".format(e_msg))
        exit_prog()
    elif not vip4(host):
        e_msg_body = make_msg_body("{} {}".format(invalid_host, host))
        e_msg = "{}\t{}".format(host_address_e_msg_header, e_msg_body)
        print("{}".format(e_msg))
        exit_prog()
    return True


def test_ipv4(address):
    if ain(address):
        e_msg_body = make_msg_body(empty_host)
        e_msg = "{}\t{}".format(host_address_e_msg_header, e_msg_body)
        print("{}".format(e_msg))
        exit_prog()
    elif not vip4(address):
        e_msg_body = make_msg_body("{}{}".format(invalid_host, address))
        e_msg = "{}\t{}".format(host_address_e_msg_header, e_msg_body)
        print("{}".format(e_msg))
        exit_prog()
    return True


def is_port_range(arg=None):
    if not arg == None:
        return ipr(arg)
    return False


def is_not_port_range(arg=None):
    if not arg == None:
        return "-" not in arg and ian(arg) and "," not in arg
    return False


def is_host_address(arg=None):
    if not arg == None:
        return vip4(arg)
    return False


def is_network_address(arg=None):
    if not arg == None:
        return vnr(arg)
    return False


def is_valid_timeout(arg=None):
    if not arg == None:
        return ianof(arg)
    return False


def make_range(arg=None):
    if not arg == None:
        if "-" in arg:
            arg_dash_split = arg.split("-")
            start = int(arg_dash_split[0])
            end = int(arg_dash_split[1])
            return {"status": True, "type": "range", "data": range(start, end, 1)}
        elif "," in arg:
            arg_comma_split = arg.split(",")
            return {"status": True, "type": "list", "data": arg_comma_split}
    return {"status": False, "reason": "Invalid argument"}
