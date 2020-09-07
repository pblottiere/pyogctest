# pyogctest

`pyogctest` is a Python tool to run OGC test suites from your terminal. This is
done by using the REST API provided by
[Teamengine](http://opengeospatial.github.io/teamengine/#). Then the resulting
XML report is parsed and displayed to be humanly readable "à la" `pytest` (as
much as possible).

`pyogctest` have been developed and tested with [QGIS
Server](https://docs.qgis.org/3.10/en/docs/server_manual/index.html) thanks to
[QGIS.org](https://www.qgis.org/en/site/). However, there's nothing specific to
QGIS Server itself (excepted for the HTML report CSS theme), so it should work
with other map servers too (while not tested).

For now, only the next test suites are supported:

- [WMS 1.3.0](http://cite.opengeospatial.org/teamengine/about/wms/1.3.0/site/wms-1_3_0-ats.html)


## Install

To install Python dependencies:

```` python
$ git clone https://github.com/pblottiere/pyogctest
$ cd pyogctest
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -e .
````

Some system dependencies are also necessary:

- `docker` because Teamengine is used through Docker images provided on
  [Dockerhub](https://hub.docker.com/u/ogccite).
- `xmlstarlet` to convert a XML document into a HTML report (useful when the
  `html` format option is activated)


## Usage

`pyogctest` allows to run OGC tests on a map server instance, so the first
thing you need is an URL pointing to the map server itself. In this
documentation, we're going to use an online instance of QGIS Server (the one
used for official certifications).

To run the WMS 1.3.0 test suites:

````
$ ./pyogctest.py -s wms130 http://qgis4.qgis.org:8080/certification_qgisserver_master
======================================== OGC test session starts =========================================
testsuite: WMS 1.3.0
collected 183 items

data-independent ...................................................................................................................................................................
data-preconditions .
basic ......
recommendations .........
queryable .........

======================================== 183 passed in 69 seconds ========================================
````


#### Verbose

If you want more details about tests, you can use the `-v` option when the
format is `prompt:

````
$ ./pyogctest.py -s wms130 -v http://qgis4.qgis.org:8080/certification_qgisserver_master
======================================== OGC test session starts =========================================
testsuite: WMS 1.3.0
collected 183 items

data-independent::basic_elements::param-rules::extra-GetMap-param PASSED
data-independent::basic_elements::param-rules::extra-GetFeatureInfo-param PASSED
data-independent::basic_elements::param-rules::extra-GetCapabilities-param PASSED
data-independent::basic_elements::version-negotiation::negotiate-no-version PASSED
...
````


#### Regex

We cannot control tests which are genuinely executed by Teamengine, but we can
filter the report. A `-r` option is available when the `prompt` format is
activated. It's not a "real" regular expression parameter, only a simple
pattern matching:

````
$ ./pyogctest.py -r transparent -s wms130 -v http://qgis4.qgis.org:8080/certification_qgisserver_master
======================================== OGC test session starts =========================================
testsuite: WMS 1.3.0
collected 183 items

data-independent::getmap::transparent::transparent-false PASSED
data-independent::getmap::transparent::transparent-default PASSED
data-independent::getmap::transparent::transparent-opaque-layer PASSED
basic::getmap::transparent::transparent-true PASSED

======================================== 183 passed in 74 seconds ========================================
````


#### HTML report

By default the output format is 'prompt' but you can also the the `-f html`
option to generate a HTML report. In this case, you can control the next
parameters:

- `-o` for the output directory with a QGIS CSS theme file
- `-b` for the branch name to use in the report
- `-c` for the commit number to use in the report


#### Docker binding port

The default binding port for the Docker container is `8081` but you may have an
error if this port is already in use on your system:

````
$ ./pyogctest.py -s wms130 http://qgis4.qgis.org:8080/certification_qgisserver_master
docker.errors.APIError: 500 Server Error: Internal Server Error ("driver failed programming external connectivity on endpoint pyogctest: Error starting userland proxy: listen tcp 0.0.0.0:8081: bind: address already in use")
````

In this case you have to use the `-p` option to use another port:

````
$ ./pyogctest.py -s wms130 -p 8088 http://qgis4.qgis.org:8080/certification_qgisserver_master
````


#### Help

To take a look at all available options, you can use the `-h` parameter:

````
$ ./pyogctest.py -h
usage: pyogctest.py [-h] [-p PORT] [-d] [-x] [-f {prompt,html}] [-s {wms130}] [-r REGEX] [-v] [-o OUTPUT] [-c COMMIT] [-b BRANCH] url

positional arguments:
  url                   URL

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Docker container binding port (default: '8081')
  -d, --debug           Debug mode
  -x, --xml             Save Teamengine XML report
  -f {prompt,html}, --format {prompt,html}
                        Output format (default: 'prompt')
  -s {wms130}, --suite {wms130}
                        Test suite (default: 'wms130')
  -r REGEX, --regex REGEX
                        Regular expression. Only the 'prompt' format is affected by this option
  -v, --verbose         Verbose mode. Only the 'prompt' format is affected by this option
  -o OUTPUT, --output OUTPUT
                        Output directory. Only the 'html' format is affected by this option (default: '/home/pblottiere/devel/perso/pyogctest/teamengine')
  -c COMMIT, --commit COMMIT
                        QGIS commit number. Only the 'html' format is affected by this option (default: None)
  -b BRANCH, --branch BRANCH
                        QGIS branch name. Only the 'html' format is affected by this option (default: 'master')
````
