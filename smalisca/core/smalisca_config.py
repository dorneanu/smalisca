#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         core/smalisca_config.py
# Created:      2015-01-16
# Purpose:      Global configuration
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

"""Global configuration file for smalisca"""

import smalisca
import codecs
import configparser
import json
from pyfiglet import Figlet

# General project information
PROJECT_NAME = "smalisca"
PROJECT_DESC = "Static Code Analysis tool for Smali files"
PROJECT_AUTHOR = "Victor <Cyneox> Dorneanu"
PROJECT_VERSION = smalisca.__version__
PROJECT_BANNER = PROJECT_NAME + " " + PROJECT_VERSION + "-" + PROJECT_DESC
PROJECT_URL = "http://nullsecurity.net, http://{blog,www}.dornea.nu"
PROJECT_MAIL = "info AEEET dornea DOT nu"
PROJECT_CONF = "smalisca/data/config/config.conf"

# Common CLI arguments
COMMON_ARGS = [
    (['--log-level'],
        dict(
            action='store', dest='level',
            choices=('debug', 'info', 'warn', 'error', 'critical'),
            help='Change logging level (Default: info)'
        )),
]

# JSON settings
JSON_SETTINGS = {
    'indent': 4
}

# Input/Output formats
# [MaÑAt the moment you can export the results as json/sqlite
# but you can only analyze sqlite.
PARSER_OUTPUT_CHOICES = ('json', 'sqlite')
ANALYZER_INPUT_CHOICES = ('sqlite',)


class HelpMessage:
    """Static class for argparse help messages"""

    # - smalisca main --------------------------------------------------------
    f = Figlet(font='larry3d')
    MAIN_BANNER = "%s\n" % f.renderText(PROJECT_NAME)
    MAIN_BANNER += "%s" % '-'*80
    MAIN_BANNER += "\n:: Author:\t %s\n" % PROJECT_AUTHOR
    MAIN_BANNER += ":: Desc:\t %s\n" % PROJECT_DESC
    MAIN_BANNER += ":: URL:\t\t %s\n" % PROJECT_URL
    MAIN_BANNER += ":: Version:\t %s\n" % PROJECT_VERSION
    MAIN_BANNER += "%s" % '-'*80
    MAIN_BANNER += "\n"

    MAIN_HELP = """
    [--] Static Code Analysis (SCA) tool for Baskmali (Smali) files.
    """

    # - Parser ---------------------------------------------------------------
    PARSER_HELP = "[--] Parse files and extract data based on Smali syntax."

    # - Analyzer -------------------------------------------------------------
    ANALYZER_HELP = "[--] Analyze results using an interactive prompt or on the command line."

    # - Web ------------------------------------------------------------------
    WEB_HELP = "[--] Analyze results using web API."

    # s (global search)
    ANALYZER_HELP_S = """
    [--] Search for pattern

    Search available tables for a specific pattern (-p).
    """

    # sc (search classes)
    ANALYZER_HELP_SC = """
    [--] Search for classes

    Specify by '-c' in which column you'd like to search for a pattern (specified by '-p').
    Examples:

    a) List available columns
        sc -c ?

    b) Search for pattern "test" in column "class_name" (first 10 results)
        sc -c class_name -p test -r 10

    c) Search for pattern "test2" in column "class_type" (print only from index 10 to 20)
        sc -c class_type -p test2 -r 10,20

    You can also exclude table fields using '-x':

    a) Exclude only one column
        sc -c class_type -p test2 -x depth

    b) Exclude multiple columns:
        sc -c class_type -p test2 -x depth,id,class_name
    """

    # sp (search properties)
    ANALYZER_HELP_SP = """
    [--] Search for properties

    Sp[MaÑecify by '-c' in which column you'd like to search for a pattern (specified by '-p').
    Examples:

    a) Lis[MaÑt available columns
        sp -c ?

    b) Search for pattern "test" in column "property_name"
        sp -c property_name -p test

    c) Search for pattern "test2" in column "property_type"
        sp -c property_type -p test2

    You can also exclude table fields using '-x':

    a) Exclude only one column
        sp -c property_type -p test2 -x depth

    b) Exclude multiple columns:
        sp -c property_type -p test2 -x depth,id,class_name
    """

    # scs (search const strings)
    ANALYZER_HELP_SCS = """
    [--] Search for const strings

    Specify by '-c' in which column you'd like to search for a pattern (specified by '-p').
    Examples:

    a) List available columns
        scs -c ?

    b) Search for pattern "test" in column "const_string_var"
        scs -c const_string_var -p test
    """

    # sm (search methods)
    ANALYZER_HELP_SM = """
    >> Search for methods

    Specify by '-t' in which column you'd like to search for a pattern (specified by '-p').
    Examples:

    a) List available columns
        sm -c ?

    b) Search for pattern "test" in column "method_name"
        sm -c method_name -p test

    c) Search for pattern "test2" in column "method_type"
        sm -c method_type -p test2

    You can al[MaÑso exclude table fields using '-x':

    a) Exclude only one column
        sm -c method_type -p test2 -x depth

    b) Exclude multiple columns:
        sm -c method_type -p test2 -x depth,id,class_name
    """

    # scl (search calls)
    ANALYZER_HELP_SCL = """
    >> Search for calls

    You can apply filters by using the optional arguments.
    Without any arguments the whole 'calls' table will
    be printed.
    """

    # sxcl (search cross calls)
    ANALYZER_HELP_SXCL = """
    >> Search for calls

    You can apply filters by using the optional arguments.
    Without any arguments the whole 'calls' table will
    be printed.
    """

    # dc (draw classes)
    ANALYZER_HELP_DC = """
    >> Draw class graphs
    """

    # dcl (draw calls)
    ANALYZER_HELP_DCL = """
    >> Draw calls graphs
    """

    # dcl (draw calls)
    ANALYZER_HELP_DXCL = """
    >> Draw cross-calls graphs
    """


class Config(object):
    """ Configuration

        Maintains basic configuration like Graphviz options stuff.

        Attributes:
            sections: Available sections
            options: Parsed options
    """

    # Specify sections to be expected
    sections = {
        'graphviz': ['classes', 'calls']
    }

    def __init__(self):
        self.parser = configparser.SafeConfigParser(allow_no_value=True)
        self.options = {}

    def read(self, filename):
        """Read config from file"""
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            self.parser.readfp(f)
            f.close()

    def parse(self):
        """Create dicts from config variables"""
        # Run through sections and check for options
        opts = {}
        for s in self.sections:
            if self.parser.has_section(s):
                opts[s] = {}
                for o in self.sections[s]:
                    if self.parser.has_option(s, o):
                        # Create JSON from string
                        opts[s][o] = json.loads(self.parser[s][o])
        self.options = opts

# Global config options
smalisca_conf = Config()
