# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"

from setuptools import setup

requirements = (
    'docker',
    'requests',
    'coloredlogs'
)

dev_requirements = (
    'black',
)


setup(
    name="pyogctest",
    version="0.1",
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    }
)
