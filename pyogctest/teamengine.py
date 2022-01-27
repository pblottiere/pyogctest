# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"

import time
import docker
import requests
from enum import Enum


NAME = "pyogctest"
OGCCITE_WMS111 = "ogccite/ets-wms11"
OGCCITE_WMS130 = "ogccite/ets-wms13"
OGCCITE_OGCAPIF = "ogccite/ets-ogcapi-features10:1.0-teamengine-5.4"


class Teamengine(object):
    class TestSuite(Enum):

        WMS130 = "wms130"
        WMS111 = "wms111"
        OGCAPIF = "ogcapif"

        def __str__(self):
            return self.value

    def __init__(self, suite, port, network):
        self.suite = suite
        self.port = port
        self.network = network

        if self.suite == Teamengine.TestSuite.WMS111:
            self.image = OGCCITE_WMS111
        elif self.suite == Teamengine.TestSuite.WMS130:
            self.image = OGCCITE_WMS130
        elif self.suite == Teamengine.TestSuite.OGCAPIF:
            self.image = OGCCITE_OGCAPIF

    def pull(self):
        client = docker.from_env()
        client.images.pull(self.image)

    def start(self):
        self.stop()

        client = docker.from_env()
        if self.network:
            client.containers.run(
                self.image,
                detach=True,
                ports={8080: self.port},
                name=NAME,
                remove=True,
                network=self.network,
            )
        else:
            client.containers.run(
                self.image, detach=True, ports={8080: self.port}, name=NAME, remove=True
            )
        time.sleep(5)  # teamengine takes some time to start

    def stop(self):
        client = docker.from_env()

        try:
            cont = client.containers.get(NAME)
            cont.stop()
            time.sleep(5)
        except docker.errors.NotFound:
            pass

    def run(self, url):
        request = None

        if self.suite == Teamengine.TestSuite.WMS111:
            getcapa = "{}?REQUEST=GetCapabilities%26VERSION=1.1.1%26SERVICE=WMS".format(
                url
            )
            teamengine = "http://localhost:{}/teamengine/rest/suites/wms11/run".format(
                self.port
            )

            request = (
                "{0}?profile=queryable&recommended=recommended&"
                "capabilities-url={1}".format(teamengine, getcapa)
            )
        elif self.suite == Teamengine.TestSuite.WMS130:
            getcapa = "{}?REQUEST=GetCapabilities%26VERSION=1.3.0%26SERVICE=WMS".format(
                url
            )
            teamengine = "http://localhost:{}/teamengine/rest/suites/wms13/run".format(
                self.port
            )

            request = (
                "{0}?queryable=queryable&basic=basic&recommended=recommended&"
                "capabilities-url={1}".format(teamengine, getcapa)
            )
        elif self.suite == Teamengine.TestSuite.OGCAPIF:
            entrypoint = "{}/wfs3".format(url)
            teamengine = "http://localhost:{}/teamengine/rest/suites/ogcapi-features-1.0/run".format(
                self.port
            )

            request = "{0}?iut={1}".format(teamengine, entrypoint)

        if request:
            r = requests.get(request, headers={"Accept": "application/xml"})
            return r.text

        return None
