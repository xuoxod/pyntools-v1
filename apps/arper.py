#! /usr/bin/python3

import argparse
from ast import arguments
from logging.config import valid_ident
import re
import os
import sys
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.PatternConstants import (
    valid_ipv4 as vip4,
    valid_network_range as vnr,
    valid_mac as vma,
    has_ext,
)
from custom_modules.PrivilegeChecker import is_user_root as iur
from custom_modules.TypeTester import arg_is_an_int as aiai
from custom_modules.PlatformConstants import (
    SEP as psep,
    CUR_DIR as cdir,
    LINE_SEP as lsep,
)
from custom_modules.FileOperator import (
    write_to_file as wtf,
    append_list_to_file as altf,
)
from custom_modules.ArpCommander import (
    print_routing_table as prt,
    get_routing_table as grt,
    print_network_interface_name as pnin,
    get_network_interface_name as gnin,
    get_network_interface_hardware_address as gniha,
    _arp_who_has as awh,
)
from custom_modules.Utils import numbered_date_time_stamp as ndts

_verbose = None
_timeout = None
_target = None
_destination = None
_save = None
_list = None
cus = cms["custom"]
timestamp = ndts().replace("/", "-").replace(",", "-").replace(":", "-")
file_path = "{}{}arper-results-{}.txt".format(cdir, psep, timestamp)


def error_handler(*args):
    cus = cms["custom"]

    for a in args:
        cargs = cus(254, 64, 74, a)
        print("{}\n".format(cargs))

    sys.exit(os.EX_USAGE)


def warning_handler(*args):
    cus = cms["custom"]
    arg = args[0]
    cargs = cus(254, 224, 224, arg)
    print("{}".format(cargs))
    sys.exit(os.EX_USAGE)


def exit_prog(exit_code=0):
    sys.exit(exit_code)


desc = "A tool that displays and can print reports about the hosts connected to the network."
epil = "This program needs adminstrative access to perform many, if not, all of it's tasks."


parser = argparse.ArgumentParser(description=desc, epilog=epil)

parser.error = error_handler

""" group optional arguments """

group = parser.add_mutually_exclusive_group()

group.add_argument(
    "-v", "--verbose", help="Increases verbosity output", action="store_true"
)

""" positional arguments """

# Set timeout period in seconds
parser.add_argument(
    "-t",
    "--timeout",
    type=int,
    nargs=1,
    help="Time out periods in seconds before giving up",
)

# Set the response destination
parser.add_argument(
    "-d",
    "--destination",
    nargs=1,
    help="Set the response destination. Works with the arp command",
)

# Set the target IP or IP range
parser.add_argument(
    "--target", nargs=1, help="Sets the target IP or IP range. Works with arp command."
)

# Saves output to file in the user's home dir
parser.add_argument("-s", "--save", help="Save output to file", action="store_true")

# Print info to the console
parser.add_argument("-r", "--route", help="Print routing info", action="store_true")

# Prints the local network interface name
parser.add_argument(
    "-n",
    "--name",
    help="Prints the name of local network interface",
    action="store_true",
)

# Prints the local network interface hardware address
parser.add_argument(
    "-m",
    "--mac",
    help="Prints the local network interface hardware address[] MAC]",
    action="store_true",
)

# Prints output in a list
parser.add_argument("-a", "--arp", help="Make ARP request", action="store_true")


args = parser.parse_args()

if args.save:
    _save = True


if args.verbose:
    _verbose = True

if args.timeout:
    if aiai(args.timeout) and args.timeout > 0:
        _timeout = args.timeout

if args.destination:
    valid_dest = vma(str(args.destination[0]).strip())

    if valid_dest:
        _destination = args.destination[0]
    else:
        msg = cus(
            255,
            255,
            255,
            "Destination argument {} must be a valid MAC address. e.g. ##:##:##:##:##:##".format(
                args.destination
            ),
        )
        msg_head = cus(255, 101, 101, "Error:")
        err_msg = "{} {}".format(msg_head, msg)
        raise ValueError(err_msg)
        exit_prog()

if args.target:
    if vip4(args.target[0].strip()) or vnr(args.target[0].strip()):
        _target = args.target[0]
    else:
        msg = cus(
            255,
            255,
            255,
            "Target argument {} must be a valid IP address or IP range. e.g. 10.1.10.1, 192.168.1.1/24".format(
                args.target
            ),
        )
        msg_head = cus(255, 101, 101, "Error:")
        err_msg = "{} {}".format(msg_head, msg)
        raise ValueError(err_msg)
        exit_prog()

# Make sure program is ran with root privilege
if not iur():
    e_msg_header = cus(255, 155, 155, "Error:")
    e_msg_body = cus(255, 255, 255, "Must run this script with root privilege.")
    e_msg = "{} {}".format(e_msg_header, e_msg_body)
    print("{}\n".format(e_msg))
    exit_prog()

if args.route:
    data = grt()
    file_path = "{}{}{}".format(cdir, psep, "routing-results.txt")
    _title = "Local Routing Information"
    c_title = cus(255, 255, 255, _title)
    print(" {}\n".format(c_title))

    prt()

    if _save:
        output_saved = wtf(file_path, data)

        if _verbose:
            # Save output to file
            _action = "... Saving to file"
            c_action = cus(255, 255, 255, _action)
            print("\t\t{}\n".format(c_action))

            if output_saved:
                _action_success = "Info saved to file"
                c_action_success = cus(90, 255, 90, _action_success)
                print("\t\t{}\n".format(c_action_success))
            else:
                _action_failure = "Error saving to file"
                c_action_failure = cus(255, 90, 90, _action_failure)
                print("\t\t{}\n".format(c_action_failure))
        else:
            if not output_saved:
                _action_failure = "Error saving to file"
                c_action_failure = cus(255, 90, 90, _action_failure)
                print("\n\t\t{}\n".format(c_action_failure))

elif args.name:
    data_frame = gnin()

    if _verbose:
        _title = "Network Interface Name"
        c_title = cus(255, 255, 255, _title)

        print("\t\t{}\n".format(c_title))
        print("{}\n".format(data_frame))

        if args.save:
            print("... Saving info to file\n")

            output_saved = wtf(file_path, data_frame)

        if output_saved:
            _action_success = "Successfully saved info the file"
            c_action_success = cus(88, 255, 88, _action_success)
            print("{}\n".format(c_action_success))
        else:
            _action_failure = "Error saving to file"
            c_action_failure = cus(255, 90, 90, _action_failure)
            print("\n\t\t{}\n".format(c_action_failure))
    else:
        c_data = cus(255, 255, 255, data_frame)
        print("{}\n".format(c_data))

        if args.save:
            output_saved = wtf(file_path, data_frame)

            if not output_saved:
                _action_failure = "Error saving to file"
                c_action_failure = cus(255, 90, 90, _action_failure)
                print("\n\t\t{}\n".format(c_action_failure))

elif args.mac:
    mac = gniha()
    print("{}".format(mac))

elif args.arp:
    if _verbose:
        _verbose = 0

    if _timeout:
        _timeout = 0

    items = []
    results = awh(_destination, _target, _verbose, _timeout)
    status = results["status"]

    if status:
        clients = results["clients"]

        if len(clients) > 0:
            for i, c in enumerate(clients, start=1):
                client = c

                print("{}.\tIP: {}\tMAC: {}".format(i, client["ip"], client["mac"]))
            if _save:
                for c in clients:
                    client = c
                    line = "{},{}{}".format(client["ip"], client["mac"], lsep)
                    items.append(line)
                altf(file_path, items)
    else:
        print("{}\n".format(results["reason"]))

else:
    print("\n" + " " * 55 + "Done!\n\n")
