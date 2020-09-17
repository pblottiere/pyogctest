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


class ParserWMS130(object):
    def __init__(self, xml, duration):
        self.xml = xml
        self.duration = duration
        self.error = 0

    def dump_html(self, outdir, commit, branch):
        out = None
        err = None
        moddir = os.path.dirname(os.path.realpath(__file__))

        with tempfile.NamedTemporaryFile() as f:
            f.write(self.xml.encode())

            xsl = os.path.join(moddir, "tohtml.xsl")
            cmd = ["xmlstarlet", "tr", xsl, f.name]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            out = out.decode("utf-8")

        report_out = ""

        for line in out.splitlines(keepends=True):
            # clear line
            line = line.replace("&quot;", '"')
            line = line.replace("&amp;", "&")

            # date
            date_tag = "{{TEMPLATE_DATE}}"
            if date_tag in line:
                format = "%Y-%m-%d %H:%M:%S"
                date = datetime.datetime.now().strftime(format)
                line = date

            # version
            version_tag = "{{TEMPLATE_VERSION}}"
            if version_tag in line:
                line = line.replace(version_tag, branch)

            # commit
            commit_tag = "{{TEMPLATE_COMMIT}}"
            if commit_tag in line:
                commit_link = "https://github.com/qgis/QGIS/commit/{}".format(commit)
                commit_link_tag = "%7BTEMPLATE_COMMIT_LINK%7D"
                line = line.replace(commit_link_tag, commit_link)
                line = line.replace(commit_tag, commit)

            report_out += line

        if not os.path.isdir(outdir):
            os.makedirs(outdir)

        f = open(os.path.join(outdir, "teamengine.html"), "w")
        f.write(report_out)
        f.close()

        style = os.path.join(moddir, "style.css")
        shutil.copy(style, outdir)

        logo = os.path.join(moddir, "logo.png")
        shutil.copy(logo, outdir)

    def dump_prompt(self, verbose, regex):
        self._parse()
        Logger.log("collected {} items".format(len(self.tree)), bold=True)
        Logger.log("")

        others = []
        data_independent = []
        basic = []
        queryable = []
        recommendations = []
        data_preconditions = []

        for t in self.tree:
            names = []
            for e in t:
                test = self._test(e)
                names.append(test.name)
            names.reverse()

            test = self._test(t[0])

            if "data-independent" in names:
                test.name = "::".join(names[1:])
                data_independent.append(test)
            elif "basic" in names:
                test.name = "::".join(names[1:])
                basic.append(test)
            elif "queryable" in names:
                test.name = "::".join(names[1:])
                queryable.append(test)
            elif "recommendations" in names:
                test.name = "::".join(names[1:])
                recommendations.append(test)
            elif "data-preconditions" in names:
                test.name = "::".join(names[1:])
                data_preconditions.append(test)
            else:
                test.name = "::".join(names)
                others.append(test)

        if verbose:
            self._print_verbose(data_independent, "data-independent", regex)
            self._print_verbose(data_preconditions, "data-preconditions", regex)
            self._print_verbose(basic, "basic", regex)
            self._print_verbose(recommendations, "recommendations", regex)
            self._print_verbose(queryable, "queryable", regex)
            if others:
                self._print_verbose(others, "main", regex)
        else:
            self._print_normal(data_independent, "data-independent")
            self._print_normal(data_preconditions, "data-preconditions")
            self._print_normal(basic, "basic")
            self._print_normal(recommendations, "recommendations")
            self._print_normal(recommendations, "queryable")
            if others:
                self._print_normal(others, "main")

        results = [
            data_preconditions,
            data_independent,
            basic,
            recommendations,
            queryable,
            others,
        ]

        self._print_summary(results)

    def _results(self, tests):
        failures = []
        successes = []
        results = ""
        for test in tests:
            if test.result == "1":
                successes.append(test)
            else:
                failures.append(test)

        return failures, successes

    def _print_verbose(self, tests, name, regex):
        for test in tests:
            if regex not in test.name:
                continue

            result = ""
            if test.result == "1":
                result = test.name + Logger.Symbol.OK + " PASSED" + Logger.Symbol.ENDC
            else:
                result = test.name + Logger.Symbol.FAIL + " FAIL" + Logger.Symbol.ENDC
            Logger.log(result)

    def _print_normal(self, tests, name):
        results = ""
        for test in tests:
            if test.result == "1":
                results = results + Logger.Symbol.OK + "." + Logger.Symbol.ENDC
            else:
                results = results + Logger.Symbol.FAIL + "F" + Logger.Symbol.ENDC
        print("{} {}".format(name, results))

    def _print_summary(self, results):
        failures = []
        successes = []
        for result in results:
            f, s = self._results(result)
            failures += f
            successes += s

        Logger.log("")
        if not failures:
            msg = " {} passed in {} seconds ".format(len(successes), self.duration)
            Logger.log(msg, color=Logger.Symbol.OK, center=True, symbol="=")
        else:
            Logger.log(" FAILURES ", center=True, symbol="=")

            for failure in failures:
                name = " {} ".format(failure.name)
                Logger.log(name, color=Logger.Symbol.FAIL, center=True, symbol="_")
                Logger.log("")

                Logger.log("Assertion: {}".format(failure.assertion))
                Logger.log("")

                if failure.exception:
                    Logger.log("Error: {}".format(failure.exception))
                    Logger.log("")

                if failure.url:
                    Logger.log("URL: {}".format(failure.url))
                    Logger.log("")

                if failure.method:
                    Logger.log("Method: {}".format(failure.method))
                    Logger.log("")

            msg = " {} passed, {} failed in {} seconds ".format(
                len(successes), len(failures), self.duration
            )
            self.error = 1
            Logger.log(msg, color=Logger.Symbol.WARNING, center=True, symbol="=")

    def _parse(self):

        root = ET.fromstring(self.xml)

        tree = []
        for child in root:
            if not self._has_child(child):
                tree.append(self._fathers(root, child, [child]))

        self.tree = tree

    def _fathers(self, root, node, fathers):
        father = self._father(root, node)

        if father:
            fathers.append(father)
            fathers = self._fathers(root, father, fathers)

        return fathers

    def _path(self, node):
        path = None
        for child in node:
            if child.tag == "starttest":
                path = child.attrib["path"]
        return path

    def _father(self, root, node):
        path = self._father_path(node)
        for child in root:
            if self._path(child) == path:
                return child
        return None

    def _father_path(self, node):
        path = self._path(node)
        if path:
            return "/".join(path.split("/")[:-1])
        return None

    def _has_child(self, node):
        for child in node:
            if child.tag == "testcall":
                return True
        return False

    def _test(self, node):
        t = Test()

        for child in node:
            if child.tag == "starttest":
                t.name = child.attrib["local-name"]
                prefix = child.attrib["prefix"]
                t.path = child.attrib["path"]

                for cc in child:
                    if cc.tag == "assertion":
                        t.assertion = cc.text

            if child.tag == "request":
                for cc in child:
                    if "request" in cc.tag:
                        for ccc in cc:
                            if "url" in ccc.tag:
                                t.url = ccc.text

                            if "param" in ccc.tag:
                                t.url = "{}{}={}&".format(
                                    t.url, ccc.attrib["name"], ccc.text
                                )

                            if "method" in ccc.tag:
                                t.method = ccc.text

            if child.tag == "endtest":
                t.result = child.attrib["result"]

            if child.tag == "exception":
                t.exception = child.text
            if child.tag == "message":
                t.exception = child.text.replace("Error: ", "")

        return t
