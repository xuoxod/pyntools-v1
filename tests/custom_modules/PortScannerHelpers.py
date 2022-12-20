import sys
from custom_modules.PortScanner import is_port_open_thread as ipot
from custom_modules.PlatformConstants import (
    LINE_SEP as lsep,
    CUR_DIR as cdir,
    SEP as sep,
)
from custom_modules.FileOperator import append_file as af


def scan_port_range(address, ports, timeout, report, verbose):
    data = []
    file_path = "{}{}portscanner-results.txt".format(cdir, sep)

    data.append("Scanning host {} port(s) {}{}".format(address, ports, lsep))

    for p in ports:
        if verbose:
            print("Scanning host {} port(s) {}".format(address, ports))

        port_open = ipot(address, p, verbose, timeout)

        data.append("Port {} open? {}{}".format(p, port_open, lsep))

        if verbose:
            print("Port {} open? {}{}".format(p, port_open, lsep))
        else:
            if port_open:
                print("Port {} is open{}".format(p, lsep))

    if report:
        if verbose:
            print("{}Saving {} to file".format(lsep, data))
        af(file_path, data)


def scan_port(address, port, timeout, report, verbose):
    data = []
    file_path = "{}{}portscanner-results.txt".format(cdir, sep)

    data.append("Scanning host {} port(s) {}{}".format(address, port, lsep))

    if verbose:
        print("Scanning {} port {}".format(address, port))

        port_open = ipot(address, port, verbose, timeout)

        print("Port {} open? {}{}".format(port, port_open, lsep))
    else:
        port_open = ipot(address, port, verbose, timeout)

        if port_open:
            print("Port {} is open{}".format(port, lsep))

    data.append("Port {} open? {}{}".format(port, port_open, lsep))

    if report:
        if verbose:
            print("{}Saving {} to file".format(lsep, data))
        af(file_path, data)
