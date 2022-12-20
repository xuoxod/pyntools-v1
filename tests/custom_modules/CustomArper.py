#! /usr/bin/python3

from scapy.all import srp, Ether, ARP, conf
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms


def send_arp(destination_host=None, target_host=None):
    _dst = "ff:ff:ff:ff:ff:ff"
    _pdst = None
    conf.verb = 0
    cus = cms["custom"]

    if not destination_host == None:
        _dst = destination_host

    if not target_host == None:
        _pdst = target_host

    if not _pdst == None:
        try:
            ans, unans = srp(Ether(dst=_dst) / ARP(pdst=_pdst), timeout=2)

            print(r"\begin{tabular}{|l|l|}")
            print(r"\hline")
            print(r"MAC & IP\\")
            print(r"\hline")
            for snd, rcv in ans:
                print(rcv.sprintf(r"%Ether.src% & %ARP.psrc%\\"))
            print(r"\hline")
            print(r"\end{tabular}")
        except SystemExit as se:
            msg = "{}".format(se)
            cmsg = cus(255, 255, 255, msg)
            print("\t{}\n".format(cmsg))
            ans = None
            unans = None
            _pdst = None
        except KeyboardInterrupt as ki:
            msg = "{}".format(ki)
            cmsg = cus(255, 255, 255, msg)
            print("\t{}\n".format(cmsg))
            ans = None
            unans = None
            _pdst = None
