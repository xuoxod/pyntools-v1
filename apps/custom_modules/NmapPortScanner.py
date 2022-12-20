import nmap
from multiprocessing.pool import ThreadPool
from .ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from .TypeTester import arg_is_a_string, arg_is_an_int as aiai

custom = cms["custom"]

""" 
    Connects to given host at the given port to deteremine whether the host is up and state of the port.
    @Param host String: IP address or range 
    @Param port Striing: The connection port or port range
"""


def is_port_open(host, port):
    print("Scanning target: {}:{}".format(host, port))
    nm_scanner = nmap.PortScanner()
    nm_scanner.scan(str(host), str(port))
    return nm_scanner


def scan_network(network, port=None):
    print("Normal Scan\nScanning target: {} port(s): {}".format(network, port))
    nm = nmap.PortScanner()

    if not port == None:
        a = nm.scan(network, str(port), arguments="sn")
    else:
        a = nm.scan(network, arguments="sn")
    return nm


def custom_scan_network(network, port, scan_mode):
    return_list = []
    nm = nmap.PortScanner()
    a = nm.scan(hosts=network, ports=str(port), arguments="{}".format(scan_mode))
    for k, v in a["scan"].items():
        if str(v["status"]["state"]) == "up":
            try:
                return_list.append(
                    "{},{},{}".format(
                        str(v["status"]["state"]),
                        str(v["addresses"]["ipv4"]),
                        str(v["addresses"]["mac"]),
                    )
                )
            except Exception:
                pass
    if len(return_list) > 0:
        return {"status": True, "data": return_list, "source": a}
    else:
        return {"status": False, "reason": "Failed to detect any hosts"}


def is_port_open_thread(host, port, num_proc=None):
    _processes = 3
    if aiai(num_proc):
        _processes = num_proc
    pool = ThreadPool(processes=_processes)
    async_result = pool.apply_async(is_port_open, (host, port))
    return async_result.get()


def scan_network_thread(network, port):
    pool = ThreadPool(processes=1)
    async_results = pool.apply_async(scan_network, (network, port))
    return async_results.get()


def custom_scan_network_thread(network, port, scan_mode):
    pool = ThreadPool(processes=3)
    async_results = pool.apply_async(custom_scan_network, (network, port, scan_mode))
    return async_results.get()
