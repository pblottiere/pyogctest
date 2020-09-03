#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    coloredlogs.install(fmt="%(asctime)s %(levelname)s %(message)s", level=level)
    logging.info("Run pyogctest for WMS 1.3.0")

    # run OGC tests with Teamengine
    # t = Teamengine(Teamengine.TestSuite.WMS130, args.port)

    # logging.debug("Pull docker image")
    # t.pull()

    # logging.debug("Start container")
    # t.start()

    # logging.debug("Run OGC tests")
    # xml = t.run(args.url)
    # t.stop()

    f = open("report.xml", "r")
    data = f.read()
    f.close()

    # parse xml report
    logging.debug("Parse XML report")
    r = Report(data)
    r.dump()
