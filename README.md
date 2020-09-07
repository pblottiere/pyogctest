# pyogctest

`pyogctest` is a Python tool to run OGC test suites from your terminal. This is
done by using the REST API provided by
[Teamengine](http://opengeospatial.github.io/teamengine/#). Then the resulting
XML report is parsed and displayed to be humanly readable "à la" `pytest` (as
much as possible).

`pyogctest` have been developed and tested with [QGIS
Server](https://docs.qgis.org/3.10/en/docs/server_manual/index.html) thanks to
[QGIS.org](https://www.qgis.org/en/site/). However, there's nothing specific to
QGIS Server itself, so it should work with other map servers too (while not
tested).


### Install

To install Python dependencies:

```` python
$ git clone https://github.com/pblottiere/pyogctest
$ cd pyogctest
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -e .
````

Moreover, `docker` is also necessary to run `pyogctests`. Indeed, Teamengine is
used through Docker images provided on
[Dockerhub](https://hub.docker.com/u/ogccite).
