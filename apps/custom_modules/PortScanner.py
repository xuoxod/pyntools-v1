#! /usr/bin/python3

import socket
from ast import Param
from multiprocessing.pool import ThreadPool
from .ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms


def is_port_open(host, port, verbose=False, timeout=None):
    _timeout = 2.2

    if not timeout == None and not timeout <= 0:
        _timeout = timeout

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            if verbose:
                print("Connecting to host {} on port {}".format(host, port))

            s.settimeout(_timeout)
            s.connect((host, port))
            connected = s.connect_ex((host, port))

            return connected == 0
        except Exception as ex:
            if verbose:
                line = ""
                if "class" in str(type(ex)):
                    if len(ex.args) > 1:
                        line = "{}".format(ex.args[1])
                    elif len(ex.args) == 1:
                        line = "{}".format(ex.args[0])
                else:
                    line = "{}".format(ex)

                print(line)

            return False


def is_port_open_thread(host, port, verbose=None, timeout=None):
    pool = ThreadPool(processes=3)
    async_result = pool.apply_async(is_port_open, (host, port, verbose, timeout))
    return async_result.get()
