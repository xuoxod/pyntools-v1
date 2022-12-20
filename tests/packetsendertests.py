#! /usr/bin/python3

from custom_modules.ArgumentManager import filtered, filtered_count
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.PacketSender import send_pkt as spk

if filtered_count == 2:
    try:
        host = filtered[0]
        port = int(filtered[1])
        spk(host, port)
    except Exception as exc:
        print("{}\n".format(exc))
elif filtered_count == 3:
    try:
        host = filtered[0]
        port = int(filtered[1])
        flag = filtered[2]
        spk(host, port, flag)
    # except KeyError as ke:
    #     print("{}\n".format(ke))
    except Exception as exc:
        print("{}\n".format(exc))
