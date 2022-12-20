#! /usr/bin/python3


from socket import timeout
from scapy.all import sr1, IP, ICMP
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms


def ping(host_address):
    cus = cms["custom"]
    try:
        p = sr1(IP(dst=host_address) / ICMP(timeout=3))
        # print("{}".format(p.show()))
        p.show()
        if p:
            if "IP" in p:
                ip = p["IP"]
                print("Hops: {}".format(ip.hops()))
                print("Source: {}".format(ip.src))
                print("Dest: {}".format(ip.dst))
                print("TTL: {}".format(ip.ttl))
                print("TOS: {}".format(ip.tos))
                print("Name: {}".format(ip.name))
                print("Sniffed On: {}".format(ip.sniffed_on))
                print("Seconds: {}".format(round((ip.time / 1000), 2)))

    except SystemExit as se:
        p = None
        cus = None
        msg = "{}".format(se)
        cmsg = cus(255, 255, 255, msg)
        print("\t{}\n".format(cmsg))
    except KeyboardInterrupt as ki:
        p = None
        cus = None
        msg = "{}".format(ki)
        cmsg = cus(255, 255, 255, msg)
        print("\t{}\n".format(cmsg))
