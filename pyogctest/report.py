# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Report(object):

    def __init__(self, xml, duration):
        self.xml = xml
        self.duration = duration
        self._parse()

    def dump(self, mode=""):
        print("\033[1mcollected {} items\033[0m".format(len(self.tree)))
        print("")

        data_independent = []
        basic = []
        queryable = []
        recommendations = []
        data_preconditions = []

        for t in self.tree:
            names = []
            for e in t:
                name, prefix, path, result, assertion = self._info(e)
                names.append(name)

            name, prefix, path, result, assertion = self._info(t[0])
            names.reverse()
            names = names[1:]

            if "data-independent" in names:
                data_independent.append([result, '.'.join(names), assertion])

            if "basic" in names:
                basic.append([result, '.'.join(names), assertion])

            if "queryable" in names:
                queryable.append([result, '.'.join(names), assertion])

            if "recommendations" in names:
                recommendations.append([result, '.'.join(names), assertion])

            if "data-preconditions" in names:
                data_preconditions.append([result, '.'.join(names), assertion])

        failures = []
        failures += self._dump(data_preconditions, "data-preconditions")
        failures += self._dump(data_independent, "data-independent")
        failures += self._dump(basic, "basic")
        failures += self._dump(recommendations, "recommendations")
        failures += self._dump(queryable, "queryable")

        print("")
        rows, columns = os.popen('stty size', 'r').read().split()

        if not failures:
            width = ":=^{}".format(columns)
            msg = bcolors.OKGREEN + "{{{}}}".format(width) + bcolors.ENDC
            text = ' {} passed in {} seconds '.format(len(self.tree), self.duration)
            print(msg.format(text))
        else:
            width = ":_^{}".format(columns)
            msg = "{{{}}}".format(width)
            print(msg.format(" FAILURES "))

            for failure in failures:
                msg = bcolors.FAIL + "{{{}}}".format(width) + bcolors.ENDC
                text = " {} ".format(failure[1])
                print(msg.format( text ))
                print()
                print("Assertion: {}".format(failure[2]))
                print()

    def _dump(self, tests, name):
        failures = []
        results = ""
        for test in tests:
            result = test[0]
            if result == "1":
                results = results + bcolors.OKGREEN + "." + bcolors.ENDC
            else:
                results = results + bcolors.FAIL + "F" + bcolors.ENDC
                failures.append(test)
        print("{} {}".format(name, results))
        return failures

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

        for child in node:
            if child.tag == "starttest":
                name = child.attrib["local-name"]
                prefix = child.attrib["prefix"]
                path = child.attrib["path"]

                for cc in child:
                    if cc.tag == "assertion":
                        assertion = cc.text

            if child.tag == "endtest":
                result = child.attrib["result"]

        return name, prefix, path, result, assertion
