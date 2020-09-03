# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET


class Node(object):

    def __init__(self):
        self.name = ""
        self.assertion = ""
        self.prefix = ""
        self.path = ""
        self.result = None
        self.nodes = []
        self.leafs = []


class Leaf(object):

    def __init__(self):
        self.name = ""
        self.prefix = ""
        self.assertion = ""
        self.path = ""
        self.result = None


class Report(object):

    def __init__(self, xml):
        self.xml = xml
        self._parse()

    def dump(self):
        for t in self.tree:
            names = []
            for e in t:
                name, prefix, path, result = self._info(e)
                names.append(name)
            name, prefix, path, result = self._info(t[0])
            names.reverse()
            names = '.'.join(names[1:])
            print("{}: {}".format(names, result))

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

            if child.tag == "endtest":
                result = child.attrib["result"]

        return name, prefix, path, result
