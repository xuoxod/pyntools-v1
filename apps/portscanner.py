#! /usr/bin/python3

import argparse
import os
import sys
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.NmapPortcannerHelpers import (
    handle_results as handler,
    print_nmap_report as pnr,
    nmap_scan_results_handler as nsrh,
)
from custom_modules.PlatformConstants import LINE_SEP as lsep
from custom_modules.PortScannerUtils import (
    test_network_address as tna,
    test_port_arg as tpa,
    test_host_address as tha,
    test_ipv4 as ti4,
    exit_prog as exp,
    is_host_address as iha,
    is_network_address as ina,
    is_not_port_range as inpr,
    is_port_range as ipr,
    is_valid_timeout as ivt,
    make_range as mr,
)
from custom_modules.PortScannerHelpers import scan_port_range, scan_port
from custom_modules.PortScanner import is_port_open_thread as ipot
from custom_modules.NmapPortScanner import is_port_open_thread as nmap, scan_network
from custom_modules.ArpCommander import get_routing_table as return_route


def exit_prog(exit_code=0):
    sys.exit(exit_code)


def range_verbosely(address, ports, verbose, timeout):
    mode = cus(100, 255, 100, "Scan Mode")
    print("{}".format(mode))
    msg = cus(
        255,
        255,
        255,
        "Scan parameters: Host: {} Port(s): {} Verbose? {} Timeout: {}".format(
            address, ports, verbose, timeout
        ),
    )
    print("{}".format(msg))
    normal = cus(255, 235, 100, lsep)
    print("{}".format(normal))

    for port in ports:
        print("Scanning port {}".format(port))
        open = ipot(address, port, verbose, timeout)

        if open:
            msg = cus(100, 255, 100, "Port {} is open".format(port))
            print("{}".format(msg))
            normal = cus(255, 235, 100, lsep)
            print("{}".format(normal))
        else:
            msg = cus(100, 100, 100, "Port {} is closed".format(port))
            print("{}".format(msg))
            normal = cus(255, 235, 100, lsep)
            print("{}".format(normal))


def range_silently(address, ports, verbose, timeout):
    for port in ports:
        open = ipot(address, port, verbose, timeout)

        if open:
            msg = cus(100, 255, 100, "Port {} is open".format(port))
            print("{}".format(msg))
            normal = cus(255, 235, 100, lsep)
            print("{}".format(normal))


def run_verbosely(address, ports, verbose, timeout):
    mode = cus(100, 255, 100, "Scan Mode")
    print("{}".format(mode))
    msg = cus(
        255,
        255,
        255,
        "Scan parameters: Host: {} Port(s): {} Verbose? {} Timeout: {}".format(
            address, ports, verbose, timeout
        ),
    )
    print("{}".format(msg))
    normal = cus(255, 235, 100, lsep)
    print("{}".format(normal))

    open = ipot(address, int(ports), verbose, timeout)

    if open:
        msg = cus(100, 255, 100, "Port {} is open".format(ports))
        print("{}{}".format(msg, lsep))
        normal = cus(255, 235, 100, lsep)
        print("{}".format(normal))
    else:
        msg = cus(100, 100, 100, "Port {} is closed".format(ports))
        print("{}{}".format(msg, lsep))
        normal = cus(255, 235, 100, lsep)
        print("{}".format(normal))


def run_silently(address, ports, verbose, timeout):
    open = ipot(address, int(ports), verbose, timeout)

    if open:
        msg = cus(100, 255, 100, "Port {} is open".format(ports))
        print("{}{}".format(msg, lsep))
        normal = cus(255, 235, 100, lsep)
        print("{}".format(normal))


cus = cms["custom"]
route_data = return_route()
netface_name = route_data["interface"]
local_ipv4_addr = route_data["address"]
gateway = route_data["gateway"]


desc = "This program scans the given port(s) of the given host"
epil = "Scan a port or range of ports. E.g. portscanner < [--scan <address> <[--ports <[n|n,n,n|n-n]>]> [--timeout <seconds>] |--nmap <[scan choice]> < --addr <[network|host]> >  [--ports <[n|n,n,n|n-n]>.] ] > [--report]"
vers = "%prog 0.1"


def error_handler(*args):
    cus = cms["custom"]
    arg = args[0]
    cargs = cus(254, 60, 60, arg)
    print("{}".format(cargs))
    exit_prog()


parser = argparse.ArgumentParser(description=desc, epilog=epil)

parser.error = error_handler

parser.version = vers

group = parser.add_mutually_exclusive_group()

""" group arguments """

# verbosity level
group.add_argument(
    "-v",
    "--verbose",
    help="Increase output verbosity. Does not work with the -n option.",
    action="store_true",
)

""" positional arguments """

# start program
parser.add_argument(
    "-s",
    "--scan",
    nargs=1,
    help="Scan host/network. Expects a host or network address, e.g. --scan <[10.1.10.1|10.1.10.1/8]>.",
)

# connection timeout
parser.add_argument(
    "-t",
    "--timeout",
    nargs=1,
    help="Expects a integer or float, e.g. --timeout <[3|0.8]>. Defaults to 10.",
)

# print results to file
parser.add_argument(
    "-r", "--report", help="Prints scan results to file.", action="store_true"
)

# address to scan
parser.add_argument(
    "-a",
    "--addr",
    help="Expects a host or network address. This argument works with the Nmap option.",
    nargs=1,
)

# port or port range
parser.add_argument(
    "-p",
    "--ports",
    nargs=1,
    help="Expects a number, comma separated list or a range: e.g. --port <[22|53,80,631,250|1-1024]>.",
)

# use nmap port scanning
parser.add_argument(
    "-n",
    "--nmap",
    action="store_true",
    help="Nmap scan, works with the --addr parameter.",
)


def run_scan_mode():
    verbose = False
    timeout = None

    address = args.scan[0]

    if ina(address) or iha(address):
        if args.ports:
            ports = args.ports[0]

            if ipr(ports):
                _port_range = mr(ports)
                status = _port_range["status"]

                if status:
                    ports = _port_range["data"]
                    type = _port_range["type"]

                    if args.verbose:
                        verbose = True

                    if args.timeout:
                        timeout = args.timeout[0]

                    if verbose:
                        range_verbosely(address, ports, verbose, timeout)
                    else:
                        range_silently(address, ports, verbose, timeout)

                else:
                    e_msg_header = cus(255, 100, 100, "Error: ")
                    e_msg_body = cus(255, 255, 255, _port_range["reason"])
                    e_msg = "{}{}".format(e_msg_header, e_msg_body)
                    print("{}".format(e_msg))
            else:
                if args.verbose:
                    verbose = True

                if args.timeout:
                    timeout = args.timeout[0]

                if verbose:
                    run_verbosely(address, ports, verbose, timeout)
                else:
                    run_silently(address, ports, verbose, timeout)

        else:
            e_msg_header = cus(255, 100, 100, "Error: ")
            e_msg_body = cus(255, 255, 255, "Missing port(s) option")
            e_msg = "{}{}".format(e_msg_header, e_msg_body)
            print("{}".format(e_msg))
    else:
        if len(args.scan[0].strip()) == 0:
            _err = "Expected a valid network or host address but received nothing."
        else:
            _err = "Expected a valid network or host address but received [{}]".format(
                address
            )
        e_msg_header = cus(255, 100, 100, "Error: ")
        e_msg_body = cus(
            255,
            255,
            255,
            _err,
        )
        e_msg = "{}{}".format(e_msg_header, e_msg_body)
        print("{}".format(e_msg))

    exit_prog()


def run_nmap_mode(args=None):
    mode = cus(100, 255, 100, "Nmap Mode")
    print("{}".format(mode))
    normal = cus(255, 235, 100, " ")
    print("{}".format(normal))

    ports = None

    if args.addr:
        address = args.addr[0]

        if iha(address) or ina(address):
            if args.ports:
                if tpa(args.ports[0]):
                    ports = args.ports[0]

                results = nmap(address, ports)
                handler(results)

                if args.report:
                    pnr(results)
        else:
            e_msg_header = cus(255, 110, 110, "Error: ")
            e_msg_body = cus(
                255,
                255,
                255,
                "Expected a valid IP address or range but received [{}]. E.g. 10.1.10.1, 192.168.1.1/24.".format(
                    address
                ),
            )
            e_msg = "{}{}".format(e_msg_header, e_msg_body)
            print("{}{}".format(e_msg, lsep))

    exit_prog()


# parse arguments
args = parser.parse_args()

if args.scan:
    run_scan_mode()
elif args.nmap:
    run_nmap_mode(args)
else:
    exit_prog()
