import random


def random_mac():
    return [
        0x00,
        0x50,
        0x56,
        random.randint(0x00, 0x7F),
        random.randint(0x00, 0xFF),
        random.randint(0x00, 0xFF),
    ]


def mac_pretty_print(mac):
    return ":".join(map(lambda x: "%02x" % x, mac))


def make_pretty_random_mac():
    return mac_pretty_print(random_mac())
