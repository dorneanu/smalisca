#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         core/smalisca_main.py
# Created:      2015-01-25
# Purpose:      Main application
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

"""Main smalisca application built on top of Cement"""

import signal
import sys
import smalisca.core.smalisca_config as config
from smalisca.core.smalisca_logging import log
from smalisca.controller.controller_base import BaseController

from cement.core import foundation


def smalisca_signal_handler(signum, frame):
    """A basic signal handler.

    This function will catch specific signals and trigger some actions.

    Args:
        signum (int): Signal number

    """
    if signum == signal.SIGTERM:
        log.warn("Caught SIGTERM! Exiting ...")
        sys.exit(1)

    elif signum == signal.SIGINT:
        log.warn("Caught SIGINT! Exiting...")
        sys.exit(1)


class SmaliscaApp(foundation.CementApp):
    """Main application class.

    Smalisca was build upon Cement due to its advanced CLI application
    framework capabilities. This class just initializes the application,
    sets logging and all the other pre-run initializations.

    """
    class Meta:
        label = config.PROJECT_NAME
        base_controller = BaseController
        log_handler = log

    def print_banner(self):
        """Prints main application banner"""
        print(config.HelpMessage.MAIN_BANNER)
