from scapy.all import *
import sys
import signal
import os


def setup_monitor_mode(interface=None):
    if not interface == None:
        print("Setting up to sniff ....")
        os.system("ifconfig {} down".format(interface))
        try:
            os.system("ifconfig {} up".format(interface))
            print("Interface set UP")
            os.system("airmon-ng start {}".format(interface))
            print("Interface is set in monitor mode")
        except:
            print("Failed to set up monitor mode")
        return interface
