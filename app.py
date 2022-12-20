#! /usr/bin/env python3

import sys
from scapy.all import *
from apps.custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from apps.custom_modules.ScapyPortScanner import prepare_packet as pp

cus = cms["custom"]


def exit_prog(exit_code=0):
    sys.exit(exit_code)


try:
    ans, unans = pp({"host": "192.168.1.22", "port": "22,445"})

    print(ans.nsummary(lfilter=lambda x, y: x.haslayer(TCP) and x.getlayer(TCP)))
    print(ans.show())
except ValueError as ve:
    print(ve)
