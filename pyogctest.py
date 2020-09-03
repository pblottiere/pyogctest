#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime
import logging
import argparse
import coloredlogs

from pyogctest.report import Report
from pyogctest.teamengine import Teamengine


if __name__ == "__main__":
    # aprse args
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url", type=str, help="URL",
    )

    parser.add_argument(
       "-p", "--port", type=int, help="Binding port", default=8081
    )

    parser.add_argument(
       "-d", "--debug", help="Debug mode", action="store_true"
    )

    args = parser.parse_args()

    # init logging
    rows, columns = os.popen('stty size', 'r').read().split()
    width = ":=^{}".format(columns)
    msg = "\033[1m{{{}}}\033[0m".format(width)
    print(msg.format(' OGC test session starts '))
    print("testsuite: WMS 1.3.0")

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    coloredlogs.install(level=level)

    # run OGC tests with Teamengine
    start = datetime.datetime.now()
    t = Teamengine(Teamengine.TestSuite.WMS130, args.port)

    logging.debug("Pull docker image")
    t.pull()

    logging.debug("Start container")
    t.start()

    logging.debug("Run OGC tests")
    xml = t.run(args.url)
    t.stop()
    end = datetime.datetime.now()

    # f = open("report.xml", "r")
    # xml = f.read()
    # f.close()

    # parse xml report
    logging.debug("Parse XML report")
    r = Report(xml, (end-start).seconds)
    r.dump()
