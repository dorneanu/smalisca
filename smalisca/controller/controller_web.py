#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         controller/controller_web.py
# Created:      2015-06-01
# Purpose:      Controller for web related analysis
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

"""CLI controller for web related analysis"""

import smalisca.core.smalisca_config as config
from smalisca.core.smalisca_logging import log
from smalisca.modules.web import create_flask_app
from smalisca.modules.web.module_web import WebServer

from cement.core import controller
from cement.core.controller import CementBaseController


class WebController(CementBaseController):
    """ Web controller

        FIXME: Finish this text
    """

    class Meta:
        label = 'web'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = config.HelpMessage.WEB_HELP

        arguments = config.COMMON_ARGS + [
            (['-f', '--file'],
                dict(
                    dest="filename", help="Specify SQLite DB (required)",
                    required=True)),
            (['-H', '--host'],
                dict(
                    dest="host",
                    help="Specify hostname to listen on")),
            (['-p', '--port'],
                dict(
                    dest="port", type=int,
                    help="Specify port to listen on")),
        ]

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        """Default command"""
        host = None
        port = None

        # Check for hostname
        if self.app.pargs.host:
            host = self.app.pargs.host

        # Check for port
        if self.app.pargs.port:
            port = int(self.app.pargs.port)

        # Read SQLite data
        if self.app.pargs.filename:
            from smalisca.modules.module_sql_models import AppSQLModel

            # Read SQLite data
            appSQL = AppSQLModel(self.app.pargs.filename)
            log.info("Successfully opened SQLite DB")

            # Create API endpoints
            flask_app = create_flask_app()

            # Start web server
            log.info("Starting web application ...")
            web_server = WebServer(host, port, flask_app)
            web_server.create_blueprints(appSQL.get_session())
            web_server.run()
