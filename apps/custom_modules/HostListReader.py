#! /usr/bin/python3

import os, sys
from custom_modules.TypeTester import arg_is_none as ain, arg_is_a_string as aias
from custom_modules.FileValidator import fileExists as fde, isFile as isaf
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms

cus = cms["custom"]
error_msg_header = cus(255, 88, 88, "Error:")
warning_msg_header = cus(255, 200, 1, "Warning:")
success_msg_header = cus(88, 255, 88, "Success:")


def msg_body_generator(msg=None):
    if not ain(msg):
        if aias(msg):
            return cus(255, 255, 255, msg)


def run_nmap_vuln_scan(file_path=None):
    if not ain(file_path):
        if fde(file_path):
            if isaf(file_path):
                with open(file_path) as f:
                    lines = f.readlines()

                    for line in lines:
                        line_split = line.split(",")
                        ip = line_split[0]
                        mac = line_split[1]

                        os.system("sudo nmap --script vuln {}".format(ip))
                        print("-" * 100)
                    print("\n\n")
            else:
                msg = msg_body_generator(
                    "File path [{}] is not a file".format(file_path)
                )
                warning_msg = "{}\t{}".format(warning_msg_header, msg)
                raise ValueError(warning_msg)
        else:
            msg = msg_body_generator("File path [{}] does not exist".format(file_path))
            warning_msg = "{}\t{}".format(warning_msg_header, msg)
            raise ValueError(warning_msg)
    else:
        msg = msg_body_generator(
            "Expecting a file path argument but received [{}]".format(file_path)
        )
        error_msg = "{}\t{}".format(error_msg_header, msg)
        raise ValueError(error_msg)
