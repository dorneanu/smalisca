#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         setup.py
# Created:      2015-03-05
# Purpose:      Setup file for smalisca
#
# Copyright
# -----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2015 Victor Dorneanu <info AAET dornea DOT nu>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import io
import os
from setuptools import setup, find_packages

# Local directory
here = os.path.dirname(os.path.abspath(__file__))

# Version
version_file = open(os.path.join(here, 'smalisca', 'VERSION'))
version = version_file.read().strip()

# GitHub download url
github_url = "https://github.com/dorneanu/smalisca/archive/{0}.tar.gz".format(version)


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(os.path.join(here, filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

# Get long description
long_description = read('README.rst', 'CHANGELOG.rst')

setup(
    name='smalisca',
    version=version,
    description='Static code analysis tool for Smali files',
    long_description=long_description,
    url='http://github.com/dorneanu/smalisca',
    download_url=github_url,
    author='Victor Dorneanu',
    author_email='info@dornea.nu',
    keywords='cli smali sca',
    license='MIT',
    packages=find_packages(exclude="bin"),
    install_requires=[
        'graphviz',
        'cement',
        'sqlalchemy',
        'pyfiglet',
        'prettytable'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Java Libraries',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ],
    scripts=['bin/smalisca'],
)
