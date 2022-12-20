from distutils.sysconfig import customize_compiler
from scapy.all import sniff
import os
import sys
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms

global cus

cus = cms["custom"]


def bring_up_iw(iface):
    x = os.system("sudo iwconfig {} up".format(iface))
    if x == 0:
        x = os.system("iwconfig {}".format(iface))
        s_msg_header = cus(100, 255, 100, "Successfully ")
        s_msg_body = cus(255, 255, 255, "Brought up {}".format(iface))
        s_msg = "{}{}".format(s_msg_header, s_msg_body)
        print("{}".format(s_msg))
    else:
        f_msg_header = cus(255, 100, 100, "Failed ")
        f_msg_body = cus(255, 255, 255, "to bring up {}".format(iface))
        f_msg = "{}{}".format(f_msg_header, f_msg_body)
        print("{}".format(f_msg))


def bring_down_iw(iface):
    x = os.system("sudo iwconfig {} down".format(iface))
    if x == 0:
        x = os.system("iwconfig {}".format(iface))
        s_msg_header = cus(100, 255, 100, "Successfully ")
        s_msg_body = cus(255, 255, 255, "Brought down {}".format(iface))
        s_msg = "{}{}".format(s_msg_header, s_msg_body)
        print("{}".format(s_msg))
    else:
        f_msg_header = cus(255, 100, 100, "Failed ")
        f_msg_body = cus(255, 255, 255, "to bring down {}".format(iface))
        f_msg = "{}{}".format(f_msg_header, f_msg_body)
        print("{}".format(f_msg))


def bring_up_if(iface):
    x = os.system("sudo ifconfig {} up".format(iface))
    if x == 0:
        x = os.system("ifconfig {}".format(iface))
        s_msg_header = cus(100, 255, 100, "Successfully ")
        s_msg_body = cus(255, 255, 255, "Brought up {}".format(iface))
        s_msg = "{}{}".format(s_msg_header, s_msg_body)
        print("{}".format(s_msg))
    else:
        f_msg_header = cus(255, 100, 100, "Failed ")
        f_msg_body = cus(255, 255, 255, "to bring up {}".format(iface))
        f_msg = "{}{}".format(f_msg_header, f_msg_body)
        print("{}".format(f_msg))


def bring_down_if(iface):
    x = os.system("sudo ifconfig {} down".format(iface))
    if x == 0:
        x = os.system("ifconfig {}".format(iface))
        s_msg_header = cus(100, 255, 100, "Successfully ")
        s_msg_body = cus(255, 255, 255, "Brought down {}".format(iface))
        s_msg = "{}{}".format(s_msg_header, s_msg_body)
        print("{}".format(s_msg))
    else:
        f_msg_header = cus(255, 100, 100, "Failed ")
        f_msg_body = cus(255, 255, 255, "to bring down {}".format(iface))
        f_msg = "{}{}".format(f_msg_header, f_msg_body)
        print("{}".format(f_msg))


def check_iface_exist(iface):
    x = os.system("sudo ifconfig {}".format(iface))

    if x == 0:
        return True
    return False


def check_iwface_exist(iface):
    x = os.system("sudo iwconfig {}".format(iface))

    if x == 0:
        return True
    return False


uod = {
    "ifup": bring_up_if,
    "ifdown": bring_down_if,
    "iwup": bring_up_iw,
    "iwdown": bring_down_iw,
    "iface": check_iface_exist,
}


def mon_mode(iface=None):
    x = os.system("ifconfig {}".format(iface))

    if x == 0:
        msg = "{} is in Monitor Mode\n".format(iface)
        s_msg = cus(190, 255, 190, msg)
        print("{}".format(s_msg))

    sys.exit(0)


def man_mode(iface=None):
    x = os.system("ifconfig {}".format(iface))

    if x == 0:
        msg = "{} is in Manage Mode".format(iface)
        s_msg = cus(190, 255, 190, msg)
        print(s_msg)

    sys.exit(0)


def pro_mode(iface=None):
    x = os.system("ifconfig {}".format(iface))

    if x == 0:
        msg = "{} is in Promiscuous Mode".format(iface)
        s_msg = cus(190, 255, 190, msg)
        print(s_msg)

    sys.exit(0)


modes = {
    "mon": mon_mode,
    "man": man_mode,
    "pro": pro_mode,
    "monitor": mon_mode,
    "manage": man_mode,
    "promiscuous": pro_mode,
    "prom": pro_mode,
}


def set_mode(iface=None, mode=None):
    if not iface == None:
        try:
            if not mode == None:
                mode = mode.strip()
                _mode = modes[mode]
                _mode(iface)
            else:
                msg = cus(255, 255, 255, "Expected mode name but received nothing")
                e_msg_header = cus(255, 100, 100, "Error:")
                e_msg = "{}\t{}".format(e_msg_header, msg)
                print("{}".format(e_msg))
        except KeyError as ie:
            msg = ""
            if len(mode) == 0:
                msg = cus(255, 255, 255, "Expected mode name but received nothing")
            else:
                msg = cus(255, 255, 255, "[{}] mode is not available".format(mode))
            e_msg_header = cus(255, 100, 100, "Error:")
            e_msg = "{}\t{}".format(e_msg_header, msg)
            print("{}".format(e_msg))
        except Exception as ex:
            msg = cus(255, 255, 255, ex)
            e_msg_header = cus(255, 100, 100, "Error:")
            e_msg = "{}\t{}".format(e_msg_header, msg)
            print("{}".format(e_msg))
    else:
        msg = cus(
            255,
            255,
            255,
            "Expected network interface name but received [{}]".format(iface),
        )
        e_msg_header = cus("Error:")
        e_msg = "{}\t{}".format(e_msg_header, msg)
        print("{}".format(e_msg))
    sys.exit(0)
