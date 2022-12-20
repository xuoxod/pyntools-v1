#! /usr/bin/python3

from custom_modules.ArgumentManager import filtered as args, filtered_count as argsc
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.PatternConstants import (
    valid_ipv4 as vip,
    valid_mac as vma,
    valid_network_range as vnr,
)

if argsc == 1:
    arg = args[0]
    print("{} is a valid IPv4 address? {}".format(arg, vip(arg)))
    print("{} is a valid MAC address? {}".format(arg, vma(arg)))
    print("{} is a valid Network range? {}".format(arg, vnr(arg)))
elif argsc > 1:
    for a in args:
        print("{} is a valid IPv4 address? {}".format(a, vip(a)))
        print("{} is a valid MAC address? {}".format(a, vma(a)))
        print("{} is a valid Network range? {}".format(a, vnr(a)))
else:
    msg = cms["custom"](255, 255, 255, "Good Bye!")
    print("\n" + " " * 55 + "{}\n\n".format(msg))
