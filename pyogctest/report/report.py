# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"

from enum import Enum

from pyogctest.teamengine import Teamengine
from pyogctest.report.wms111.wms111 import ParserWMS111
from pyogctest.report.wms130.wms130 import ParserWMS130
from pyogctest.report.ogcapif.ogcapif import ParserOGCAPIF


class Report(object):
    def __init__(self, suite, xml, duration):
        self.parser = None
        if suite == Teamengine.TestSuite.WMS111:
            self.parser = ParserWMS111(xml, duration)
        elif suite == Teamengine.TestSuite.WMS130:
            self.parser = ParserWMS130(xml, duration)
        elif suite == Teamengine.TestSuite.OGCAPIF:
            self.parser = ParserOGCAPIF(xml, duration)

    def dump_prompt(self, verbose, regex):
        self.parser.dump_prompt(verbose, regex)

    def dump_html(self, outdir, commit, branch):
        self.parser.dump_html(outdir, commit, branch)
