# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"

import os
import sys
import shutil
import zipfile
import requests
import fileinput

from pyogctest.teamengine import Teamengine


WMS130_ZIP = "data-wms-1.3.0.zip"
WMS130_PROJECT = "teamengine_wms_130.qgs"
WMS130_URL = "https://cite.opengeospatial.org/teamengine/about/wms13/1.3.0/site/"


class Data(object):
    def __init__(self, suite):
        self.suite = suite

    def download(self):
        if self.suite == Teamengine.TestSuite.WMS130:
            request = os.path.join(WMS130_URL, WMS130_ZIP)
            r = requests.get(request, verify=False)

            open(WMS130_ZIP, "wb").write(r.content)

            self.extract(WMS130_ZIP)
            os.remove(WMS130_ZIP)

    def extract(self, zipdata=None):

        dirname = os.path.dirname(os.path.realpath(__file__))

        if self.suite == Teamengine.TestSuite.WMS130:
            if zipdata is None:
                zipdata = os.path.join(dirname, WMS130_ZIP)

            with zipfile.ZipFile(zipdata, "r") as zip_ref:
                zip_ref.extractall("data")

            src = os.path.join(dirname, WMS130_PROJECT)
            dst = os.path.join("data", WMS130_PROJECT)
            shutil.copyfile(src, dst)

    def prepare(self, url):
        if not Data.exists():
            return

        dirname = os.path.dirname(os.path.realpath(__file__))
        src = os.path.join(dirname, WMS130_PROJECT)
        dst = os.path.join("data", WMS130_PROJECT)
        shutil.copyfile(src, dst)

        pattern = "http://nginx/wms13"
        replacement = url

        for line in fileinput.input(dst, inplace=True):
            line = line.replace(pattern, replacement)
            sys.stdout.write(line)

    @staticmethod
    def exists():
        return os.path.exists("data")
