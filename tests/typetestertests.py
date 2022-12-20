#! /usr/bin/python3

from custom_modules.TypeTester import arg_is_a_function as aiaf
from custom_modules.ArgumentManager import filtered as args, filtered_count as argsc

if argsc == 1:
    arg = args[0]
    print("{} is a function: {}".format(arg, aiaf(arg)))
