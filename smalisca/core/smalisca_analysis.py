#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         core/smalisca_analysis.py
# Created:      2015-01-30
# Purpose:      Defines classes aimed at analysing parsed results
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

"""Basic abstract class for analysis functionalities"""

import abc


class AnalysisBase(metaclass=abc.ABCMeta):
    """Basic analysis class

    Provides abstract methods how to interact with the results.
    Every inheriting class has to implement these methods.

    """

    # Search functionalities

    @abc.abstractmethod
    def search_class(self, args):
        """Search for class"""
        pass

    @abc.abstractmethod
    def search_property(self, args):
        """Search for property"""
        pass

    @abc.abstractmethod
    def search_method(self, args):
        """Search for method"""
        pass

    @abc.abstractmethod
    def search_call(self, args):
        """Search for call"""
        pass

    # Cross-References (xref)

    @abc.abstractmethod
    def xref_class(self, args):
        """Find xref to class"""
        pass

    @abc.abstractmethod
    def xref_method(self, args):
        """Find xref to method"""
        pass
