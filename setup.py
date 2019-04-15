#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
from distutils.command.clean import clean

from setuptools import setup

PACKAGE = 'permission_resolver'
__version__ = '1.0.0'

classes = """
    Development Status :: 5 - Production/Stable
    Programming Language :: Python
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: OS Independent
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

setup(
    name=PACKAGE,
    version=__version__,
    description='Read/write folders permissions resolver',
    author='Ivan Bondarenko',
    author_email='bondarenko.ivan.v@gmail.com',
    packages=[PACKAGE],
    include_package_data=True,
    classifiers=classifiers
)
