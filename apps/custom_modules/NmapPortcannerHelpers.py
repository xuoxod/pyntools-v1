#! /usr/bin/python3


# from Threading import Thread
from .NmapPortScanner import is_port_open as ipo
from .TypeTester import arg_is_a_string as aias, arg_is_a_list as aial
from .FileOperator import append_file as af
from .PlatformConstants import LINE_SEP as lsep


def handle_results(results):
    print("Handling results {}".format(results))
    protocols = None
    command = None
    scan_info = None
    dict_tcp_keys = None
    csv = None
    tcp = None
    state = None
    product = None
    reason = None
    name = None
    version = None
    extra = None
    conf = None

    # results = ipo(hosts, ports, verbose, timeout, report)

    """if results[host].state:
        state = results[host].state()

    if results[host].all_protocols:
        protocols = results[host].all_protocols()

    if results.command_line:
        command = results.command_line()

    if results.scaninfo:
        scan_info = results.scaninfo()

    if "tcp" in results[host]:
        dict_tcp_keys = results[host]["tcp"].keys()

    if results.csv:
        csv = results.csv"""

    all_hosts = results.all_hosts()

    print("All hosts {}".format(all_hosts))

    for _host in all_hosts:

        if results[_host].state:
            state = results[_host].state()

        if results[_host].all_protocols:
            protocols = results[_host].all_protocols()

        if results.command_line:
            command = results.command_line()

        if results.scaninfo:
            scan_info = results.scaninfo()

        if "tcp" in results[_host]:
            dict_tcp_keys = results[_host]["tcp"].keys()

        if results.csv:
            csv = results.csv()

        print("-" * 100 + "\n")

        print("Host:\t{}".format(_host))

        print("State:\t{}".format(state))

        # print("Command:\t{}".format(command))

        # print("Scann Info:\t{}".format(scan_info))

        # print("CSV:\t{}".format(csv))

        # print("-" * 100 + "\n\n")

        if protocols:

            for protocol in protocols:
                info = scan_info[protocol]

                print("Protocol:\t{}".format(protocol))

                print(
                    "Scan Info =\t\tAction: {}\tPorts: {}".format(
                        info["method"], info["services"]
                    )
                )

                if protocol == "tcp":

                    dict_tcp_keys = results[_host][protocol].keys()

                    print("Open Ports")

                    print(*dict_tcp_keys, sep="\t")

                    print("\n")

                    for tcp_key in dict_tcp_keys:
                        key = results[_host][protocol][tcp_key]

                        # print("TCP Key:\t{}".format(key))

                        state = key["state"]
                        reason = key["reason"]
                        product = key["product"]
                        name = key["name"]
                        version = key["version"]
                        extra = key["extrainfo"]
                        conf = key["conf"]
                        cpe = key["cpe"]

                        print("Port:\t\t{}".format(tcp_key))

                        print("State:\t\t{}".format(state))

                        print("Reason:\t\t{}".format(reason))

                        print("Name:\t\t{}".format(name))

                        print("Product:\t\t{}".format(product))

                        print("Version:\t\t{}".format(version))

                        print("Extra:\t\t{}".format(extra))

                        print("Conf:\t\t{}".format(conf))

                        print("CPE:\t\t{}\n".format(cpe))


# Print results to file
def print_nmap_report(results):
    protocols = None
    scan_info = None
    dict_tcp_keys = None
    state = None
    product = None
    reason = None
    name = None
    version = None
    extra = None
    conf = None
    data = []
    line = ""

    all_hosts = results.all_hosts()

    for _host in all_hosts:

        if results[_host].state:
            state = results[_host].state()

        if results[_host].all_protocols:
            protocols = results[_host].all_protocols()

        if results.command_line:
            command = results.command_line()

        if results.scaninfo:
            scan_info = results.scaninfo()

        if "tcp" in results[_host]:
            dict_tcp_keys = results[_host]["tcp"].keys()

        if results.csv:
            csv = results.csv()

        line = "-" * 100 + "{}".format(lsep)

        data.append(line)

        data.append("Host:\t{}{}".format(_host, lsep))

        data.append("State:\t{}{}".format(state, lsep))

        if protocols:

            for protocol in protocols:
                info = scan_info[protocol]

                data.append("Protocol:\t{}{}".format(protocol, lsep))

                data.append(
                    "Scan Info =\t\tAction: {}\tPorts: {}{}".format(
                        info["method"], info["services"], lsep
                    )
                )

                if protocol == "tcp":

                    dict_tcp_keys = results[_host][protocol].keys()

                    data.append("Open Ports{}".format(lsep))

                    line = ""

                    for dtk in dict_tcp_keys:
                        line += "{}\t".format(dtk)

                    data.append(line)

                    data.append("{}{}".format(lsep, lsep))

                    for tcp_key in dict_tcp_keys:
                        key = results[_host][protocol][tcp_key]

                        state = key["state"]
                        reason = key["reason"]
                        product = key["product"]
                        name = key["name"]
                        version = key["version"]
                        extra = key["extrainfo"]
                        conf = key["conf"]
                        cpe = key["cpe"]

                        data.append("Port:\t\t{}{}".format(tcp_key, lsep))

                        data.append("State:\t\t{}{}".format(state, lsep))

                        data.append("Reason:\t\t{}{}".format(reason, lsep))

                        data.append("Name:\t\t{}{}".format(name, lsep))

                        data.append("Product:\t\t{}{}".format(product, lsep))

                        data.append("Version:\t\t{}{}".format(version, lsep))

                        data.append("Extra:\t\t{}{}".format(extra, lsep))

                        data.append("Conf:\t\t{}{}".format(conf, lsep))

                        data.append("CPE:\t\t{}{}{}".format(cpe, lsep, lsep))
    results = af("nmap-port-scanner-results.txt", data)
    return results


def print_report(data):
    if not data == None:
        if aial(data):
            collection = []
            for d in data:
                collection.append(d + "{}".format(lsep))
            if len(collection) > 0:
                report = af("port-scanner-results.txt", collection)
                return report
    return None


def nmap_scan_results_handler(arg):
    if not arg == None:
        if "scan" in arg:
            scan = arg["scan"]
            _list = []

            for key in scan.keys():
                item = scan[key]

                hostnames = item["hostnames"]
                addresses = item["addresses"]
                vendor = item["vendor"]
                status = item["status"]

                print("Host {}".format(key))
                _list.append("Host {}".format(key))

                try:
                    print(
                        "Hostname: {}\tType: {}".format(
                            hostnames[0]["name"], hostnames[0]["type"]
                        )
                    )

                    # print(hostnames)

                    print("IP: {}\tMAC: {}".format(addresses["ipv4"], addresses["mac"]))
                    _list.append(
                        "IP: {}\tMAC: {}{}".format(
                            addresses["ipv4"], addresses["mac"], lsep
                        ),
                    )

                    # print(addresses)

                    print("Vendor: {}".format(vendor["{}".format(addresses["mac"])]))
                    _list.append(
                        "Vendor: {}{}".format(
                            vendor["{}".format(addresses["mac"])], lsep
                        ),
                    )

                    # print(vendor)

                    print(
                        "Status: {}\tReason: {}".format(
                            status["state"], status["reason"]
                        )
                    )
                    _list.append(
                        "Status: {}\tReason: {}{}".format(
                            status["state"], status["reason"], lsep
                        )
                    )
                except KeyError:
                    pass
                # print(status)

                if "tcp" in item:
                    tcp = item["tcp"]

                    for tcp_key in tcp.keys():
                        tcp_item = tcp[tcp_key]

                        state = tcp_item["state"]
                        reason = tcp_item["reason"]
                        name = tcp_item["name"]
                        product = tcp_item["product"]
                        version = tcp_item["version"]
                        extrainfo = tcp_item["extrainfo"]
                        conf = tcp_item["conf"]
                        cpe = tcp_item["cpe"]

                        print("State: {}".format(state))
                        _list.append("State: {}{}".format(state, lsep))

                        print("Reason: {}".format(reason))
                        _list.append("Reason: {}{}".format(reason, lsep))

                        print("Name: {}".format(name))
                        _list.append("Name: {}{}".format(name, lsep))

                        print("Product: {}".format(product))
                        _list.append("Product: {}{}".format(product, lsep))

                        print("Version: {}".format(version))
                        _list.append("Version: {}{}".format(version, lsep))

                        print("Extra Info: {}".format(extrainfo))
                        _list.append("Extra Info: {}{}".format(extrainfo, lsep))

                        print("Conf: {}".format(conf))
                        _list.append("Conf: {}{}".format(conf, lsep))

                        print("CPE: {}".format(cpe))
                        _list.append("CPE: {}{}".format(cpe, lsep))

                print("\n")
                _list.append("{}".format(lsep))
            return {"status": True, "data": _list}

    return {"status": False}
