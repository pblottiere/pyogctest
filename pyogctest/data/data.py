# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"

import os
import zipfile
import requests

from pyogctest.teamengine import Teamengine


WMS130_ZIP="data-wms-1.3.0.zip"
WMS130_PROJECT="teamengine_wms_130.qgs"
WMS130_URL="http://cite.opengeospatial.org/teamengine/about/wms/1.3.0/site/"


class Data(object):

    def __init__(self, suite):
        self.suite = suite

    def project(self):
        dirname = os.path.dirname(os.path.realpath(__file__))

        if self.suite == Teamengine.TestSuite.WMS130:
            return os.path.join(dirname, PROJECT_WMS130)

    def download(self):
        if self.suite == Teamengine.TestSuite.WMS130:
            request = os.path.join(WMS130_URL, WMS130_ZIP)
            r = requests.get(request)
            open(WMS130_ZIP, 'wb').write(r.content)

            with zipfile.ZipFile(WMS130_ZIP, 'r') as zip_ref:
                zip_ref.extractall("data")

    @staticmethod
    def exists():
        return os.path.exists("data")

