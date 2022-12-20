#! /usr/bin/python3

import argparse
import sys
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.BtDiscoverer import (
    enable_discovery_mode as edm,
    start_sniff as ss,
    collect_advertising_reports as car,
)

cus = cms["custom"]


def exit_prog(exit_code=0):
    sys.exit(exit_code)


def error_handler(*args):
    cus = cms["custom"]
    arg = args[0]
    cargs = cus(254, 60, 60, arg)
    print("{}".format(cargs))
    exit_prog()


desc = "This program scans for nearby bluetooth devices"
epil = "Discovery mode is enabled and disabled automatically"
vers = "%prog 0.1"

parser = argparse.ArgumentParser(description=desc, epilog=epil)

parser.error = error_handler

parser.version = vers

parser.add_argument(
    "-d",
    "--discover",
    action="store_true",
    help="Start bluetooth discovery mode and scan for bluetooth devices.",
)

args = parser.parse_args()

if args.discover:
    bt = edm()
    print(bt)

    adverts = ss(bt)
    print(adverts)

    dev_pkts, dvs = car(adverts)

    print("{}\n{}".format(dev_pkts, dvs))
