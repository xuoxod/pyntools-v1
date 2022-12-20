import socket
import re
import sys
from multiprocessing.pool import ThreadPool
from custom_modules.TypeTester import arg_is_an_int


def connect(username=None, password=None, address=None, port=None):
    if (
        not username == None
        and not password == None
        and not address == None
        and not port == None
    ):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Trying {} and {}".format(username, password))

        s.connect((address, str(port)))

        data = s.recv(1024)

        s.send("USER {}\r\n".format(username))

        data = s.recv(1024)

        s.send("PASS {}\r\n".format(password))

        data = s.recv(1024)

        s.send("QUIT\r\n")

        s.close()

        if str(data).strip() == "230":
            return {"status": True, "password": password}
        return {"status": False, "data": data}


def connect_thread(username, password, address, port, pr=3):
    _processes = 3

    if arg_is_an_int(pr) and pr > 0:
        _processes = pr

    pool = ThreadPool(processes=_processes)
    async_result = pool.apply_async(connect, (username, password, address, port))
    return async_result.get()
