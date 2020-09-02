#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import docker
import argparse
import requests

NAME="pyogctest"
OGCCITE_WMS13="ogccite/ets-wms13"


def docker_run(img, port):
    # pull the image
    client = docker.from_env()
    client.images.pull(img)

    # stop a previous container if necessary (should not happen)
    docker_stop()

    # run a new container
    client.containers.run(img, detach=True, ports={8080: port}, name=NAME, remove=True)


def docker_stop():
    client = docker.from_env()

    try:
        cont = client.containers.get(NAME)
        cont.stop()
    except docker.errors.NotFound:
        pass


def ogc_tests_wms13(url, port):
    docker_run(OGCCITE_WMS13, port)

    getcapa = "{}?SERVICE=GetCapabilities&VERSION=1.3.0&SERVICE=WMS".format(url)
    teamengine = "http://localhost:{}/teamengine/rest/suites/wms13/run".format(port)

    request = ('{0}?queryable=queryable&basic=basic&recommended=recommended&'
               'capabilities-url={1}'
               .format(teamengine, getcapa))

    time.sleep(5)  # teamengine takes some time to start
    r = requests.get(request, verify=False)

    print(r.text)

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

    args = parser.parse_args()

    # pull images
    ogc_tests_wms13(args.url, args.port)
