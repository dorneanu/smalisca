#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         controller/controller_parser.py
# Created:      2015-01-17
# Purpose:      Controll commandline arguments for parsing files
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

"""CLI controller for parsing files"""

import smalisca.core.smalisca_config as config
from smalisca.core.smalisca_app import App
from smalisca.core.smalisca_logging import log
from smalisca.modules.module_sql_models import AppSQLModel
from smalisca.modules.module_smali_parser import SmaliParser

from cement.core import controller
from cement.core.controller import CementBaseController


class ParserController(CementBaseController):
    """CLI Controller for parsing Smali files

    Iterate through files and extract data from files:

        * classes (name, type)
        * class properties (name, type)
        * methods (name, type, arguments, return value)
        * calls (source, destination, arguments)

    After extracting the information, the controller will
    save the results either as **JSON** or **SQLite DB**.

    """

    class Meta:
        label = 'parser'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = config.HelpMessage.PARSER_HELP

        arguments = config.COMMON_ARGS + [
            (['-l', '--location'],
                dict(help="Set location (required)", required=True)),
            (['-s', '--suffix'],
                dict(help="Set file suffix (required)", required=True)),
            (['-f', '--format'],
                dict(dest="fileformat", help="Files format",
                     choices=config.PARSER_OUTPUT_CHOICES)),
            (['-o', '--output'],
                dict(help="Specify output file")),
        ]

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        """Default command"""

        if self.app.pargs.location and self.app.pargs.suffix:
            self.location = self.app.pargs.location
            self.suffix = self.app.pargs.suffix

            # Create new parser
            parser = SmaliParser(self.location, self.suffix)
            parser.run()

            # Output results
            if (self.app.pargs.output) and (self.app.pargs.fileformat):
                results = parser.get_results()
                app = App(__name__)

                # Add additional info
                app.add_location(self.location)
                app.add_parser("%s - %s" % (config.PROJECT_NAME, config.PROJECT_VERSION))

                # Append classes
                for c in results:
                    app.add_class_obj(c)

                # Write results to JSON
                if self.app.pargs.fileformat == 'json':
                    log.info("Exporting results to JSON")
                    app.write_json(self.app.pargs.output)
                    log.info("\tWrote results to %s" % self.app.pargs.output)

                # Write results to sqlite
                elif self.app.pargs.fileformat == 'sqlite':
                    appSQL = AppSQLModel(self.app.pargs.output)

                    try:
                        log.info("Exporting results to SQLite")
                        # Add classes
                        log.info("\tExtract classes ...")
                        for c in app.get_classes():
                            appSQL.add_class(c)

                        # Add properties
                        log.info("\tExtract class properties ...")
                        for p in app.get_properties():
                            appSQL.add_property(p)

                        # Add const-strings
                        log.info("\tExtract class const-strings ...")
                        for c in app.get_const_strings():
                            appSQL.add_const_string(c)

                        # Add methods
                        log.info("\tExtract class methods ...")
                        for m in app.get_methods():
                            appSQL.add_method(m)

                        # Add calls
                        log.info("\tExtract calls ...")
                        for c in app.get_calls():
                            appSQL.add_call(c)

                        # Commit changes
                        log.info("\tCommit changes to SQLite DB")
                        appSQL.commit()
                        log.info("\tWrote results to %s" % self.app.pargs.output)

                    finally:
                        log.info("Finished scanning")
