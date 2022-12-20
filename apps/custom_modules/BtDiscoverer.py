from socket import BTPROTO_RFCOMM
import sys, os
from scapy.all import *
from itertools import chain


def verify_bt():
    results = os.system("hcitool dev")
    return results == 0


def send_receive():
    bt = None
    ans = None
    unans = None

    if verify_bt():
        try:
            print("Discovering bluetooth devices")
            bt = BluetoothHCISocket(0)

            ans, unans = bt.sr(
                HCI_Hdr() / HCI_Command_Hdr() / HCI_Cmd_LE_Set_Scan_Parameters(type=1)
            )
            return ans, unans, bt
        except KeyboardInterrupt as ki:
            print("{}\n".format(ki))
            disable_discovery_mode(bt)
            return ans, unans, bt
        finally:
            disable_discovery_mode(bt)
            return ans, unans, bt


def send_receive2(bt):
    ans, unans = bt.sr(
        HCI_Hdr()
        / HCI_Command_Hdr()
        / HCI_Cmd_LE_Set_Scan_Enable(enable=True, filter_dups=False)
    )
    return ans, unans


def start_sniff(bt):
    adverts = None
    try:
        print("Sniffing packets ...")
        adverts = bt.sniff(lfilter=lambda p: HCI_LE_Meta_Advertising_Reports in p)
        # print(adverts)
    except KeyboardInterrupt as ki:
        disable_discovery_mode(bt)
        return adverts
    finally:
        disable_discovery_mode(bt)
        return adverts


def disable_discovery_mode(bt):
    bt.sr(HCI_Hdr() / HCI_Command_Hdr() / HCI_Cmd_LE_Set_Scan_Enable(enable=False))
    return bt


def collect_advertising_reports(adverts):
    reports = chain.from_iterable(
        p[HCI_LE_Meta_Advertising_Reports].reports for p in adverts
    )

    # Group reports by MAC address (consumes the reports generator)
    devices = {}
    for report in reports:
        device = devices.setdefault(report.addr, [])
        device.append(report)

    # Packet counters
    devices_pkts = dict((k, len(v)) for k, v in devices.items())
    print(devices_pkts)

    return devices_pkts, devices, reports
