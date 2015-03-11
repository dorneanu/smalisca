#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         analysis/analysis_json.py
# Created:      2015-02-01
# Purpose:      Analysis functionalities based on JSON files
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

"""Implement analysis interface for JSON"""

from smalisca.analysis.analysis_base import AnalysisBase


class AnalyzerJSON(AnalysisBase):
    """Implement analysis interface for JSON

    Not available at the moment.

    """

    def __init__(self, db_session):
        """Initiate class"""
        self.db = db_session

    def search_class(self, args):
        pass

    def search_property(self, args):
        pass

    def search_method(self, args):
        pass

    def search_call(self, args):
        pass

    def xref_class(self, args):
        pass

    def xref_method(self, args):
        pass
