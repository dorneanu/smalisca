#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         controller/controller_base.py
# Created:      2015-01-17
# Purpose:      Base commandline arguments controller
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

"""Default (base) CLI controller"""

import textwrap
import smalisca.core.smalisca_config as config
from cement.core import controller


class BaseController(controller.CementBaseController):
    """Cements base controller"""

    class Meta:
        label = 'base'
        description = textwrap.dedent(config.HelpMessage.MAIN_HELP)

        config_defaults = dict(
            debug=False,
        )

        arguments = config.COMMON_ARGS + [
            (['-v', '--version'],
                dict(action='version', version=config.PROJECT_BANNER)),
        ]

    def help(self):
        """Prints help message"""
        print(textwrap.dedent(config.HelpMessage.MAIN_BANNER))

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        """Default command"""
        print("Type '--help' for additional info")
