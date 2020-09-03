# -*- coding: utf-8 -*-
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
