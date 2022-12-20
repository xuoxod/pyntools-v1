#! /usr/bin/python3

import argparse
import sys
from custom_modules.ArgumentManager import filtered as args, filtered_count as argsc
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.PatternConstants import valid_ipv4 as vip4, valid_mac as vma
from custom_modules.Pinger import ping

_dst = None
_tgt = None
cus = cms["custom"]

desc = "This program sends an ICMP to the given host"
epil = "Test that host is reachable on the network. Failure exit code: 121"
vers = "%prog 0.1"


def error_handler(*args):
    cus = cms["custom"]
    arg = args[0]
    cargs = cus(254, 64, 4, arg)
    print("{}".format(cargs))
    sys.exit(121)


parser = argparse.ArgumentParser(description=desc, epilog=epil)

parser.error = error_handler

parser.version = vers

# The target host to ping
parser.add_argument("-t", "--target", nargs=1, help="The target host to ping")

# The destination host to receive results
parser.add_argument(
    "-d",
    "--dest",
    nargs=1,
    help="The destination host to receive results. Defaults to the local machine.",
)

# parser arguments
args = parser.parse_args()

if args.target:
    if vip4(args.target[0]):
        _tgt = args.target[0]
    else:
        msg = cus(255, 255, 255, "Invalid IP address: {}".format(args.target))
        msg_head = cus(255, 22, 22, "Error:")
        e_msg = "{}\t{}\n".format(msg_head, msg)
        print("{}".format(e_msg))
        sys.exit(120)


if args.dest:
    if vma(args.dest[0]):
        _dst = args.dest[0]
    else:
        msg = cus(255, 255, 255, "Invalid MAC address: {}".format(args.dest))
        msg_head = cus(255, 22, 22, "Error:")
        e_msg = "{}\t{}\n".format(msg_head, msg)
        print("{}".format(e_msg))
        sys.exit(120)
