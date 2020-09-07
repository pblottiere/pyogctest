# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"

from enum import Enum

from pyogctest.teamengine import Teamengine
from pyogctest.report.wms130 import ParserWMS130


class Report(object):
    def __init__(self, suite, xml, duration):
        self.parser = None
        if suite == Teamengine.TestSuite.WMS130:
            self.parser = ParserWMS130(xml, duration)

    def dump(self, verbose, regex, format):
        self.parser.dump(verbose, regex, format)
