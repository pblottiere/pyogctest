# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"

from enum import Enum


class Format(Enum):

    PROMPT = "prompt"
    HTML = "html"

    def __str__(self):
        return self.value
