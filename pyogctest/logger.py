# -*- coding: utf-8 -*-
import os
import logging
import coloredlogs


class Logger(object):
    class Symbol:
        OK = "\033[92m"
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        BOLD = "\033[1m"
        ENDC = "\033[0m"

    @staticmethod
    def init(debug):
        level = logging.INFO
        if debug:
            level = logging.DEBUG
        coloredlogs.install(level=level)

    @staticmethod
    def log(text, color=None, bold=False, center=False, symbol=""):
        rows, columns = os.popen("stty size", "r").read().split()

        if center:
            width = ":{}^{}".format(symbol, columns)
            msg = "{{{}}}".format(width)
            text = msg.format(text)

        if bold:
            text = "{}{}{}".format(Logger.Symbol.BOLD, text, Logger.Symbol.ENDC)

        if color:
            text = "{}{}{}".format(color, text, Logger.Symbol.ENDC)

        print(text)

    @staticmethod
    def debug(msg):
        logging.debug(msg)
