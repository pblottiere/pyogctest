# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

from pyogctest.logger import Logger


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
        self._parse()

    def dump(self, verbose):
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
                name, prefix, path, result, assertion, exception, url, method = self._info(e)
                names.append(name)

            name, prefix, path, result, assertion, exception, url, method = self._info(t[0])
            names.reverse()

            test = Test()
            test.assertion = assertion
            test.result = result
            test.exception = exception
            test.url = url
            test.method = method

            if "data-independent" in names:
                test.name = '.'.join(names[1:])
                data_independent.append(test)
            elif "basic" in names:
                test.name = '.'.join(names[1:])
                basic.append(test)
            elif "queryable" in names:
                test.name = '.'.join(names[1:])
                queryable.append(test)

            elif "recommendations" in names:
                test.name = '.'.join(names[1:])
                recommendations.append(test)
            elif "data-preconditions" in names:
                test.name = '.'.join(names[1:])
                data_preconditions.append(test)
            else:
                test.name = '.'.join(names)
                others.append(test)

        failures = []
        successes = []

        f, s = self._results(data_preconditions)
        failures += f
        successes += s

        f, s = self._results(data_independent)
        failures += f
        successes += s

        f, s = self._results(basic)
        failures += f
        successes += s

        f, s = self._results(recommendations)
        failures += f
        successes += s

        f, s = self._results(queryable)
        failures += f
        successes += s

        if others:
            f, s = self._results(others)
            failures += f
            successes += s

        if verbose:
            pass
        else:
            self._normal(data_independent, "data-independent")
            self._normal(data_preconditions, "data-preconditions")
            self._normal(basic, "basic")
            self._normal(recommendations, "recommendations")
            self._normal(recommendations, "queryable")
            if others:
                self._normal(others, "main")

        self._summary(failures, successes)

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

    def _normal(self, tests, name):
        results = ""
        for test in tests:
            if test.result == "1":
                results = results + Logger.Symbol.OK + "." + Logger.Symbol.ENDC
            else:
                results = results + Logger.Symbol.FAIL + "F" + Logger.Symbol.ENDC
        print("{} {}".format(name, results))

    # def _dump(self, tests, name):
    #     failures = []
    #     results = ""
    #     for test in tests:
    #         if test.result == "1":
    #             results = results + Logger.Symbol.OK + "." + Logger.Symbol.ENDC
    #         else:
    #             results = results + Logger.Symbol.FAIL + "F" + Logger.Symbol.ENDC
    #             failures.append(test)
    #     print("{} {}".format(name, results))

    #     return failures

    def _summary(self, failures, successes):
        Logger.log("")
        if not failures:
            msg = " {} passed in {} seconds ".format(len(successes), self.duration)
            Logger.log(msg, color=Logger.Symbol.OK, center=True, symbol="=")
        else:
            Logger.log(" FAILURES ", center=True, symbol="=")

            for failure in failures:
                name = " {} ".format(failure.name)
                Logger.log(name, color=Logger.Symbol.FAIL, center=True, symbol='_')
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
            return '/'.join(path.split("/")[:-1])
        return None

    def _has_child(self, node):
        for child in node:
            if child.tag == "testcall":
                return True
        return False

    def _info(self, node):
        name = ""
        prefix = ""
        path = ""
        result = ""
        exception = ""
        url = ""
        method = ""

        for child in node:
            if child.tag == "starttest":
                name = child.attrib["local-name"]
                prefix = child.attrib["prefix"]
                path = child.attrib["path"]

                for cc in child:
                    if cc.tag == "assertion":
                        assertion = cc.text

            if child.tag == "request":
                for cc in child:
                    if "request" in cc.tag:
                        for ccc in cc:
                            if "url" in ccc.tag:
                                url = ccc.text

                            if "param" in ccc.tag:
                                url = "{}{}={}&".format(url, ccc.attrib["name"], ccc.text)

                            if "method" in ccc.tag:
                                method = ccc.text

            if child.tag == "endtest":
                result = child.attrib["result"]

            if child.tag == "exception":
                exception = child.text
            if child.tag == "message":
                exception = child.text.replace("Error: ", "")

        return name, prefix, path, result, assertion, exception, url, method
