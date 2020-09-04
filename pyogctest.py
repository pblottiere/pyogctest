#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import argparse

from pyogctest.logger import Logger
from pyogctest.report.report import Report
from pyogctest.teamengine import Teamengine


if __name__ == "__main__":
    # aprse args
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url",
        type=str,
        help="URL",
    )

    parser.add_argument("-p", "--port", type=int, help="Binding port", default=8081)

    parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")

    parser.add_argument("-v", "--verbose", help="Verbose mode", action="store_true")

    parser.add_argument("-s", "--suite", help="Test suite", type=Teamengine.TestSuite, choices=list(Teamengine.TestSuite), default=Teamengine.TestSuite.WMS130)

    args = parser.parse_args()

    # init logging
    Logger.init(args.debug)
    Logger.log(" OGC test session starts ", center=True, symbol="=")
    Logger.log("testsuite: WMS 1.3.0")

    # run OGC tests with Teamengine
    start = datetime.datetime.now()
    t = Teamengine(args.suite, args.port)

    Logger.debug("Pull docker image")
    t.pull()

    Logger.debug("Start container")
    t.start()

    Logger.debug("Run OGC tests")
    xml = t.run(args.url)
    t.stop()
    end = datetime.datetime.now()

    # f = open("report.xml", "r")
    # f.write(xml)
    # xml = f.read()
    # f.close()

    # parse xml report
    Logger.debug("Parse XML report")
    r = Report(args.suite, xml, (end - start).seconds)
    r.dump(args.verbose)
