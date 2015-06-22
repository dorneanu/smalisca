#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         modules/module_web.py
# Created:      2015-05-29
# Purpose:      Implement web specific tasks: API, Web-GUI etc.
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

"""Implements web specific tasks like web API, web gui etc."""

# Smalisca stuff
from smalisca.core.smalisca_logging import log

# Flask stuff
from flask.ext.restless import APIManager
from werkzeug.serving import run_simple

# Import SQLAlchemy models
from smalisca.modules.module_sql_models import SmaliClass, SmaliProperty, SmaliMethod
from smalisca.modules.module_sql_models import SmaliConstString, SmaliCall


class WebServer(object):

    """TODO: Add here description """

    def __init__(self, hostname, port, app):
        self.hostname = hostname
        self.port = port
        self.app = app
        self.apimanager = APIManager()

    def create_blueprints(self, session):
        # Initialize APIManager with Flask object
        self.apimanager.init_app(self.app, session=session)

        # Create API endpoints

        # SmaliClass
        self.apimanager.create_api(
            SmaliClass, app=self.app, methods=['GET', 'POST']
        )

        # SmaliProperty
        self.apimanager.create_api(
            SmaliProperty, app=self.app, methods=['GET', 'POST']
        )

        # SmaliMethod
        self.apimanager.create_api(
            SmaliMethod, app=self.app, methods=['GET', 'POST']
        )

        # SmaliConstString
        self.apimanager.create_api(
            SmaliConstString, app=self.app, methods=['GET', 'POST']
        )

        # SmaliCall
        self.apimanager.create_api(
            SmaliCall, app=self.app, methods=['GET', 'POST']
        )

    def run(self):
        """Runs the server"""
        run_simple(self.hostname, self.port, self.app)
