#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         controller/controller_analyzer.py
# Created:      2015-01-29
# Purpose:      Controller for analyzing results
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

"""CLI controller for the analyzer"""

import smalisca.core.smalisca_config as config
from smalisca.core.smalisca_logging import log
from smalisca.core.smalisca_app import App
from smalisca.analysis.analysis_shell import AnalyzerShell

from cement.core import controller
from cement.core.controller import CementBaseController


class AnalyzerController(CementBaseController):
    """ Controller for analyzing previously parsed Smali files

    You can interact with the results in an interactive way or
    run commands in batch style. Several commands are provided
    which can:

        * search for data
        * draw data

    """

    class Meta:
        label = 'analyzer'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = config.HelpMessage.ANALYZER_HELP

        arguments = config.COMMON_ARGS + [
            (['-i', '--input'],
                dict(
                    dest="filename", help="Specify results file to read from",
                    required=True)),
            (['-f', '--format'],
                dict(
                    dest="fileformat", help="Files format",
                    choices=config.ANALYZER_INPUT_CHOICES,
                    required=True)),
            (['-c'],
                dict(
                    dest="commands_file",
                    help="Read commands from file instead of interactive prompt")),
        ]

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        """Default command"""

        if (self.app.pargs.filename) and (self.app.pargs.fileformat):
            # Create new app
            app = App(__name__)

            # Analysis obj
            analysis = None

            # Read SQLite data
            if self.app.pargs.fileformat == "sqlite":
                from smalisca.analysis.analysis_sqlite import AnalyzerSQLite
                from smalisca.modules.module_sql_models import AppSQLModel

                # Read SQLite data
                appSQL = AppSQLModel(self.app.pargs.filename)
                log.info("Successfully opened SQLite DB")

                # Create analysis framework
                log.info("Creating analyzer framework ...")
                analysis = AnalyzerSQLite(appSQL.get_session())

            # Where to read commands from?
            if self.app.pargs.commands_file:
                commands = open(self.app.pargs.commands_file, "rt")
                try:
                    log.info("Reading commands from %s" % self.app.pargs.commands_file)
                    cmd_shell = AnalyzerShell(analysis)
                    cmd_shell.use_rawinput = False
                    cmd_shell.stdin = commands
                    cmd_shell.prompt = ''
                    cmd_shell.cmdloop()
                finally:
                    commands.close()
            else:
                # Start new shell
                log.info("Starting new analysis shell")
                cmd_shell = AnalyzerShell(analysis)
                cmd_shell.cmdloop()
