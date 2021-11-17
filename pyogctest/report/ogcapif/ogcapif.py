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
        self.assertion = ""
        self.result = ""
        self.exception = ""
        self.url = ""
        self.method = ""


class ParserOGCAPIF(object):
    def __init__(self, xml, duration):
        self.xml = xml
        self.duration = duration
        self.error = 0

    def dump_prompt(self, verbose, regex):
        print(self.xml)
