#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import docker
import logging
import argparse
import requests
import coloredlogs
import xml.etree.ElementTree as ET


NAME="pyogctest"
OGCCITE_WMS13="ogccite/ets-wms13"


def docker_pull(img):
    client = docker.from_env()
    client.images.pull(img)


def docker_run(img, port):
    # stop a previous container if necessary (should not happen)
    docker_stop()

    # run a new container
    client = docker.from_env()
    client.containers.run(img, detach=True, ports={8080: port}, name=NAME, remove=True)
    time.sleep(5)  # teamengine takes some time to start


def docker_stop():
    client = docker.from_env()

    try:
        cont = client.containers.get(NAME)
        cont.stop()
        time.sleep(5)
    except docker.errors.NotFound:
        pass


def ogc_tests_wms13(url, port):
    logging.debug("Pull last Docker image".format(OGCCITE_WMS13))
    docker_pull(OGCCITE_WMS13)

    logging.debug("Start Docker container")
    docker_run(OGCCITE_WMS13, port)

    getcapa = "{}?REQUEST=GetCapabilities%26VERSION=1.3.0%26SERVICE=WMS".format(url)
    teamengine = "http://localhost:{}/teamengine/rest/suites/wms13/run".format(port)

    request = ('{0}?queryable=queryable&basic=basic&recommended=recommended&'
               'capabilities-url={1}'
               .format(teamengine, getcapa))

    logging.debug("Run OGC CITE tests")
    r = requests.get(request, headers={'Accept': 'application/xml'})
    xml = r.text

    root = ET.fromstring(xml)
    # for child in root:
    #     print(child.text)

    logging.debug("Stop Docker container")
    docker_stop()


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

    # pull images
    ogc_tests_wms13(args.url, args.port)
