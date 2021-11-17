# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"

import os
import shutil
import datetime
import tempfile
import subprocess
import xml.etree.ElementTree as ET

from pyogctest.logger import Logger
from pyogctest.report.format import Format


class Test(object):
    def __init__(self):
        self.name = ""
        self.message = ""
        self.result = ""
        self.exception = ""
        self.method = ""


class ParserOGCAPIF(object):
    def __init__(self, xml, duration):
        self.xml = xml
        self.duration = duration
        self.error = 0

    def dump_prompt(self, verbose, regex):
        tests = self._parse()
        Logger.log("collected {} items".format(len(tests)), bold=True)
        Logger.log("")

        ok = "PASSED" if verbose else "."
        ko = "FAIL" if verbose else "F"

        for test in tests:
            if regex not in test.name and regex not in test.method:
                continue

            results = ""
            if test.result == "PASS":
                results = results + Logger.Symbol.OK + ok + Logger.Symbol.ENDC
            else:
                results = results + Logger.Symbol.FAIL + ko + Logger.Symbol.ENDC

            print("{} {}".format(f"{test.name}::{test.method}", results))

        self._print_summary(tests)

    def _print_summary(self, tests):
        failures = []
        successes = []
        for test in tests:
            if test.result == "PASS":
                successes.append(test)
            else:
                failures.append(test)

        failures = []

        Logger.log("")
        if not failures:
            msg = " {} passed in {} seconds ".format(len(successes), self.duration)
            Logger.log(msg, color=Logger.Symbol.OK, center=True, symbol="=")
        else:
            Logger.log(" FAILURES ", center=True, symbol="=")

            for failure in failures:
                name = f" {failure.name}::{failure.method} "
                Logger.log(name, color=Logger.Symbol.FAIL, center=True, symbol="_")
                Logger.log("")

                if failure.exception:
                    Logger.log("Error: {}".format(failure.exception))
                    Logger.log("")

                if failure.message:
                    msg = failure.message.strip().replace("\n", "")
                    Logger.log(f"Message: {msg}")
                    Logger.log("")

                if failure.method:
                    Logger.log("Method: {}".format(failure.method))
                    Logger.log("")

            msg = " {} passed, {} failed in {} seconds ".format(
                len(successes), len(failures), self.duration
            )
            self.error = 1
            Logger.log(msg, color=Logger.Symbol.WARNING, center=True, symbol="=")

    def _parse(self):
        root = ET.fromstring(self.xml)

        tests = []
        for test in root.find("suite").find("test"):
            for child in test:
                exception = ""
                message = ""
                for cc in child:
                    if "exception" in cc.tag:
                        exception = cc.attrib["class"]
                        for ccc in cc:
                            if "message" in ccc.tag:
                                message = ccc.text

                t = Test()
                t.name = "::".join(test.attrib["name"].split(".")[-2:])
                t.method = child.attrib["name"]
                t.result = child.attrib["status"]
                t.exception = exception
                t.message = message
                tests.append(t)

        return tests
