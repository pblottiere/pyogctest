# -*- coding: utf-8 -*-
from enum import Enum


class Format(Enum):

    PROMPT = "prompt"
    HTML = "html"

    def __str__(self):
        return self.value
