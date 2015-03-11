#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         core/smalisca_logging.py
# Created:      2015-01-25
# Purpose:      Global logging functionalities
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

"""Implements all logging related functionalities"""

import smalisca.core.smalisca_config as config
from cement.ext.ext_logging import LoggingLogHandler


class LoggingHandler(LoggingLogHandler):
    """Default Cement logging handler"""

    class Meta:
        """Default logging handler

        The logging handler is build upon Cement's LoggingLogHandler.

        Note:
            Also have a look at http://cement.readthedocs.org/en/stable-2.0.x/api/ext/ext_logging/.

        Attributes:
            console_format (str): Specifies how a log entry should look like
            debug_format (str): Specifies how a debug log entry should look like

        """
        console_format = ':: %(levelname)-10s %(message)s'
        debug_format = '%(asctime)s (%(levelname)s) %(namespace)s : %(message)s'

        config_section = 'log'
        label = config.PROJECT_NAME + ' logger'


#: Main logging object referenced in other classes
log = LoggingHandler()
