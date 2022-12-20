#! /usr/bin/python3
# -*- coding: utf-8 -*-

import ftplib


def anon_login(hostname=None):
    if not hostname == None:
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login("anonymous", "Hello")

            print("FTP anonymous login succeeded")

            ftp.quit()
            return True
        except Exception as exc:
            print("FTP {} login failed".format(hostname))
            return False
