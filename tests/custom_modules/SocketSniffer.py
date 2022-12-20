#! /usr/bin/python3

import socket
import os


def sniff(host_address=None):
    if not host_address == None:
        if os.name == "nt":
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host_address, 0))

        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == "nt":
            sniffer.loctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        print("{}".format(sniffer.recvfrom(65565)))

        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
