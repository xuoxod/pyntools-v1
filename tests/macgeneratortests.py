#! /usr/bin/python3

from custom_modules.MacGenerator import (
    mac_pretty_print as mpp,
    random_mac as rm,
    make_pretty_random_mac as mprm,
)
from custom_modules.ArgumentManager import filtered as args, filtered_count as argsc
from custom_modules.PatternConstants import valid_mac as vm

if argsc == 1:
    arg = args[0]
    if vm(arg):
        mac = rm()
        pretty_mac = mpp(mac)
        random_pretty_mac = mprm()

        print("Random MAC:\t\t{}".format(mac))
        print("Pretty MAC:\t\t{}".format(pretty_mac))
        print("PAuto MAC:\t\t{}".format(random_pretty_mac))
