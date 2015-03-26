#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         analysis/analysis_shell.py
# Created:      2015-02-01
# Purpose:      Provide basic shell to interact with the results
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

import cmd
import argparse
import sys
import textwrap

import smalisca.core.smalisca_config as config
from smalisca.core.smalisca_logging import log
from smalisca.modules.module_graph import ClassGraph, CallGraph
from smalisca.analysis.analysis_sqlite import row2dict

from prettytable import PrettyTable
from argparse import RawTextHelpFormatter


# Own argparse types
def list_type(s):
    return s.split(',')


def extract_range(s):
    """ Extract range from string"""
    ranges = s.split(',')
    if len(ranges) > 1:
        return (int(ranges[0]), int(ranges[1]))
    else:
        return (int(ranges[0]), None)


class AnalyzerShell(cmd.Cmd):
    """Analyzer command interface"""
    intro = "\n-- Analyzer "
    intro += "%s" % "-"*(80-len(intro))
    intro += '\nWelcome to ' + config.PROJECT_NAME + ' analyzer shell. \n'
    intro += 'Type ? or help to list available commands.\n'
    intro += 'Type "<command> --help" for additional help.'
    intro += '\n'

    prompt = config.PROJECT_NAME + '>'
    ruler = '-'

    # Classes columns
    class_fields = [
        {'name': 'id'},
        {'name': 'class_name'},
        {'name': 'class_type'},
        {'name': 'class_package'},
        {'name': 'depth'},
        {'name': 'path'}
    ]

    # Call columns
    call_fields = [
        {'name': 'id'},
        {'name': 'from_class'},
        {'name': 'from_method'},
        {'name': 'local_args'},
        {'name': 'dst_class'},
        {'name': 'dst_method'},
        {'name': 'dst_args'},
        {'name': 'ret'}
    ]

    # Property columns
    property_fields = [
        {'name': 'id'},
        {'name': 'property_name'},
        {'name': 'property_type'},
        {'name': 'property_info'},
        {'name': 'property_class'}
    ]

    # Const strings fields
    const_string_fields = [
        {'name': 'id'},
        {'name': 'const_string_var'},
        {'name': 'const_string_value'},
        {'name': 'const_string_class'}
    ]

    # Method columns
    method_fields = [
        {'name': 'id'},
        {'name': 'method_name'},
        {'name': 'method_type'},
        {'name': 'method_args'},
        {'name': 'method_ret'},
        {'name': 'method_class'}
    ]

    def __init__(self, analysis):
        """Initializes a analysis shell

        Args:
            analysis (AnalsysBase): An implementation of :class:`smalisca.analysis.AnalysisBase`

        """
        self.analysis = analysis

        # - Parsers ----------------------------------------------------------
        # - global search
        self.s_parser = argparse.ArgumentParser(
            prog='s', add_help=True,
            description=textwrap.dedent(config.HelpMessage.ANALYZER_HELP_S),
            formatter_class=RawTextHelpFormatter)
        self.s_parser.add_argument(
            '-p', dest='search_pattern', help="Specify search pattern")
        self.s_parser.add_argument(
            '-t', dest='table', choices=('class', 'property', 'const', 'method'),
            help="Specify table to lookup in")

        # - search classes
        self.sc_parser = argparse.ArgumentParser(
            prog='sc', add_help=True,
            description=textwrap.dedent(config.HelpMessage.ANALYZER_HELP_SC),
            formatter_class=RawTextHelpFormatter)

        self.sc_parser.add_argument(
            '-c', dest='search_type', help="Specify column.\nType ? for list")
        self.sc_parser.add_argument(
            '-p', dest='search_pattern', help="Specify search pattern")
        self.sc_parser.add_argument(
            '-s', dest='sortby', help="Sort by column name")
        self.sc_parser.add_argument(
            '--reverse', action='store_true', dest='sortby_reverse',
            help="Reverse sort order")
        self.sc_parser.add_argument(
            '-r', dest='range', help="Specify output range by single integer or separated by ','")
        self.sc_parser.add_argument(
            '--max-width', dest='max_width', type=int, help="Global column max width")
        self.sc_parser.add_argument(
            '-x', dest='exclude_fields', help="Exclude table fields",
            type=list_type)

        # - draw classes
        self.dc_parser = argparse.ArgumentParser(
            prog='dc', add_help=True,
            description=textwrap.dedent(config.HelpMessage.ANALYZER_HELP_DC),
            formatter_class=RawTextHelpFormatter)

        self.dc_parser.add_argument(
            '-c', dest='search_type', help="Specify column.\nType ? for list")
        self.dc_parser.add_argument(
            '-p', dest='search_pattern', help="Specify search pattern")
        self.dc_parser.add_argument(
            '-f', dest='output_format', help="Output format\nDefault: dot",
            choices=('dot', 'xdot', 'png', 'pdf', 'jpg', 'svg'), default="dot")
        self.dc_parser.add_argument(
            '--prog', dest='output_prog', help="Graphviz layout method\nDefault: dot",
            choices=('dot', 'neato', 'circo', 'twopi', 'fdp', 'sfdp', 'nop'), default="dot")
        self.dc_parser.add_argument(
            '--args', dest='output_args', help="Additional graphviz arguments")
        self.dc_parser.add_argument(
            '-o', dest='output', help="Specify output file", required=True)

        # properties
        self.sp_parser = argparse.ArgumentParser(
            prog='sp', add_help=True,
            description=textwrap.dedent(config.HelpMessage.ANALYZER_HELP_SP),
            formatter_class=RawTextHelpFormatter)

        self.sp_parser.add_argument(
            '-c', dest='search_type', help="Specify column.\nType ? for list")
        self.sp_parser.add_argument(
            '-p', dest='search_pattern', help="Specify search pattern")
        self.sp_parser.add_argument(
            '-s', dest='sortby', help="Sort by column name")
        self.sp_parser.add_argument(
            '--reverse', action='store_true', dest='sortby_reverse',
            help="Reverse sort order")
        self.sp_parser.add_argument(
            '-r', dest='range', help="Specify output range by single integer or separated by ','")
        self.sp_parser.add_argument(
            '--max-width', dest='max_width', type=int, help="Global column max width")
        self.sp_parser.add_argument(
            '-x', dest='exclude_fields', help="Exclude table fields",
            type=list_type)

        # const strings
        self.scs_parser = argparse.ArgumentParser(
            prog='scs', add_help=True,
            description=textwrap.dedent(config.HelpMessage.ANALYZER_HELP_SCS),
            formatter_class=RawTextHelpFormatter)

        self.scs_parser.add_argument(
            '-c', dest='search_type', help="Specify column.\nType ? for list")
        self.scs_parser.add_argument(
            '-p', dest='search_pattern', help="Specify search pattern")
        self.scs_parser.add_argument(
            '-s', dest='sortby', help="Sort by column name")
        self.scs_parser.add_argument(
            '--reverse', action='store_true', dest='sortby_reverse',
            help="Reverse sort order")
        self.scs_parser.add_argument(
            '-r', dest='range', help="Specify output range by single integer or separated by ','")
        self.scs_parser.add_argument(
            '--max-width', dest='max_width', type=int, help="Global column max width")

        # methods
        self.sm_parser = argparse.ArgumentParser(
            prog='sm', add_help=True,
            description=textwrap.dedent(config.HelpMessage.ANALYZER_HELP_SM),
            formatter_class=RawTextHelpFormatter)

        self.sm_parser.add_argument(
            '-c', dest='search_type', help="Specify column.\nType ? for list")
        self.sm_parser.add_argument(
            '-p', dest='search_pattern', help="smecify search pattern")
        self.sm_parser.add_argument(
            '-s', dest='sortby', help="Sort by column name")
        self.sm_parser.add_argument(
            '--reverse', action='store_true', dest='sortby_reverse',
            help="Reverse sort order")
        self.sm_parser.add_argument(
            '-r', dest='range', help="smecify output range by single integer or separated by ','")
        self.sm_parser.add_argument(
            '--max-width', dest='max_width', type=int, help="Global column max width")
        self.sm_parser.add_argument(
            '-x', dest='exclude_fields', help="Exclude table fields",
            type=list_type)

        # - search calls
        self.scl_parser = argparse.ArgumentParser(
            prog='scl', add_help=True,
            description=textwrap.dedent(config.HelpMessage.ANALYZER_HELP_SCL),
            formatter_class=RawTextHelpFormatter)

        self.scl_parser.add_argument(
            '-fc', dest='from_class', help="Specify calling class (from)")
        self.scl_parser.add_argument(
            '-fm', dest='from_method', help="Specify calling method (from)")
        self.scl_parser.add_argument(
            '-tc', dest='to_class', help="Specify destination class (to)")
        self.scl_parser.add_argument(
            '-tm', dest='to_method', help="Specify destination method (to)")
        self.scl_parser.add_argument(
            '-fa', dest='local_args', help="Local arguments (from)")
        self.scl_parser.add_argument(
            '-ta', dest='dest_args', help="Destination arguments (to)")
        self.scl_parser.add_argument(
            '-s', dest='sortby', help="Sort by column name")
        self.scl_parser.add_argument(
            '--reverse', action='store_true', dest='sortby_reverse',
            help="Reverse sort order")
        self.scl_parser.add_argument(
            '-r', dest='range', help="smecify output range by single integer or separated by ','")
        self.scl_parser.add_argument(
            '--max-width', dest='max_width', type=int, help="Global column max width")
        self.scl_parser.add_argument(
            '-x', dest='exclude_fields', help="Exclude table fields",
            type=list_type)

        # - search cross calls
        self.sxcl_parser = argparse.ArgumentParser(
            prog='sxcl', add_help=True,
            description=textwrap.dedent(config.HelpMessage.ANALYZER_HELP_SXCL),
            formatter_class=RawTextHelpFormatter)

        self.sxcl_parser.add_argument(
            '-c', dest='class_name', help="Specify class name")
        self.sxcl_parser.add_argument(
            '-m', dest='method_name', help="Specify method name")
        self.sxcl_parser.add_argument(
            '-d', dest='direction', help="Cros-reference direction",
            choices=('to', 'from'), required=True)
        self.sxcl_parser.add_argument(
            '--max-depth', dest='xref_depth', help="Cross-References max depth\nDefault: 1",
            nargs='?', const=1, type=int)
        self.sxcl_parser.add_argument(
            '-s', dest='sortby', help="Sort by column name")
        self.sxcl_parser.add_argument(
            '--reverse', action='store_true', dest='sortby_reverse',
            help="Reverse sort order")
        self.sxcl_parser.add_argument(
            '-r', dest='range', help="smecify output range by single integer or separated by ','")
        self.sxcl_parser.add_argument(
            '--max-width', dest='max_width', type=int, help="Global column max width")
        self.sxcl_parser.add_argument(
            '-x', dest='exclude_fields', help="Exclude table fields",
            type=list_type)

        # - draw calls
        self.dcl_parser = argparse.ArgumentParser(
            prog='dcl', add_help=True,
            description=textwrap.dedent(config.HelpMessage.ANALYZER_HELP_DCL),
            formatter_class=RawTextHelpFormatter)

        self.dcl_parser.add_argument(
            '-fc', dest='from_class', help="Specify calling class (from)")
        self.dcl_parser.add_argument(
            '-fm', dest='from_method', help="Specify calling method (from)")
        self.dcl_parser.add_argument(
            '-tc', dest='to_class', help="Specify destination class (to)")
        self.dcl_parser.add_argument(
            '-tm', dest='to_method', help="Specify destination method (to)")
        self.dcl_parser.add_argument(
            '-fa', dest='local_args', help="Local arguments (from)")
        self.dcl_parser.add_argument(
            '-ta', dest='dest_args', help="Destination arguments (to)")
        self.dcl_parser.add_argument(
            '-f', dest='output_format', help="Output format\nDefault: dot",
            choices=('dot', 'xdot', 'png', 'pdf', 'jpg', 'svg'), default="dot")
        self.dcl_parser.add_argument(
            '--prog', dest='output_prog', help="Graphviz layout method\nDefault: dot",
            choices=('dot', 'neato', 'circo', 'twopi', 'fdp', 'sfdp', 'nop'), default="dot")
        self.dcl_parser.add_argument(
            '--args', dest='output_args', help="Additional graphviz arguments")
        self.dcl_parser.add_argument(
            '-o', dest='output', help="Specify output file", required=True)

        # - draw cross calls (cross references)
        self.dxcl_parser = argparse.ArgumentParser(
            prog='dcxl', add_help=True,
            description=textwrap.dedent(config.HelpMessage.ANALYZER_HELP_DXCL),
            formatter_class=RawTextHelpFormatter)

        self.dxcl_parser.add_argument(
            '-c', dest='class_name', help="Specify class name")
        self.dxcl_parser.add_argument(
            '-m', dest='method_name', help="Specify method name")
        self.dxcl_parser.add_argument(
            '-d', dest='direction', help="Cros-reference direction",
            choices=('to', 'from'), required=True)
        self.dxcl_parser.add_argument(
            '--max-depth', dest='xref_depth', help="Cross-References max depth\nDefault: 1",
            nargs='?', const=1, type=int)
        self.dxcl_parser.add_argument(
            '-f', dest='output_format', help="Output format\nDefault: dot",
            choices=('dot', 'xdot', 'png', 'pdf', 'jpg', 'svg'), default="dot")
        self.dxcl_parser.add_argument(
            '--prog', dest='output_prog', help="Graphviz layout method\nDefault: dot",
            choices=('dot', 'neato', 'circo', 'twopi', 'fdp', 'sfdp', 'nop'), default="dot")
        self.dxcl_parser.add_argument(
            '--args', dest='output_args', help="Additional graphviz arguments")
        self.dxcl_parser.add_argument(
            '-o', dest='output', help="Specify output file", required=True)

        # Parents constructor
        cmd.Cmd.__init__(self)

    def get_classes(self, args):
        """Returns classes specified by args

        Returns:
            list: Return list of classes if any, otherwise None

        """
        try:
            results = None

            if args.search_type:

                # Print available columns
                if args.search_type == '?':
                    print([c['name'] for c in self.class_fields])
                    return

                # Search
                if args.search_pattern:
                    if any(c['name'] == args.search_type for c in self.class_fields):
                        p = {
                            'type': args.search_type,
                            'pattern': args.search_pattern
                        }
                        results = self.analysis.search_class(p)
                    else:
                        log.error("No such column! Type '-c ?' for a list of available columns.")
                else:
                    log.error("No pattern (-p) specified")
            else:
                results = self.analysis.search_class()

            return results

        except SystemExit:
            pass

    def get_calls(self, args):
        """Return calls

        Returns:
            list: Return list of calls if any, otherwise None

        """
        try:
            results = None

            # Function arguments
            p = {}

            # from class
            if 'from_class' in args:
                p['from_class'] = args.from_class
            else:
                p['from_class'] = None

            # from method
            if 'from_method' in args:
                p['from_method'] = args.from_method
            else:
                p['from_method'] = None

            # destination class
            if 'to_class' in args:
                p['to_class'] = args.to_class
            else:
                p['to_class'] = None

            # destination method
            if 'to_method' in args:
                p['to_method'] = args.to_method
            else:
                p['to_method'] = None

            # Local arguments
            if 'local_args' in args:
                p['local_args'] = args.local_args
            else:
                p['local_args'] = None

            # Destination arguments
            if 'dest_args' in args:
                p['dest_args'] = args.dest_args
            else:
                p['dest_args'] = None

            # Search for calls
            results = self.analysis.search_call(p)

            return results

        except SystemExit:
            pass

    def print_prettytable(self, args, localfields, results):
        """Prints pretty tables

        Args:
            args (dict): Arguments
            localfields (dict): Table columns
            results (list): List of results to pretty print

        """
        # Return results
        if results:
            x = PrettyTable([f['name'] for f in localfields])
            x.align = "l"
            for r in results:
                r_dict = row2dict(r)
                x.add_row([r_dict[f['name']] for f in localfields])

            # Sort by column name
            if args.sortby:
                x.sortby = args.sortby

            # Reverse output
            if args.sortby_reverse:
                x.reversesort = True

            # Column width
            if args.max_width:
                x.max_width = args.max_width

            # Print results
            if args.range:
                ranges = extract_range(args.range)
                if ranges[1]:
                    print(x.get_string(start=ranges[0], end=ranges[1]))
                else:
                    print(x.get_string(start=0, end=ranges[0]))
            else:
                print(x.get_string())
        else:
            print("No results! :(")

    def print_global_search(self, results):
        # Print classes
        print("- Classes ---------------------------------------------------------------------")
        if len(results['classes']) > 0:
            classes = results['classes']
            log.info("Found %d results" % len(classes))

            for c in classes:
                print("%s\n" % c)
        else:
            log.warn("No found classes.\n")

        # Print properties
        print("- Properties ------------------------------------------------------------------")
        if len(results['properties']) > 0:
            properties = results['properties']
            log.info("Found %d results" % len(properties))

            for p in properties:
                print("%s\n" % p)
        else:
            log.warn("No found properties.\n")

        # Print const strings
        print("- Const strings ---------------------------------------------------------------")
        if len(results['consts']) > 0:
            const_strings = results['consts']
            log.info("Found %d results" % len(const_strings))

            for s in const_strings:
                print("%s\n" % s)
        else:
            log.warn("No found const strings.\n")

        # Print methods
        print("- Methods ---------------------------------------------------------------------")
        if len(results['methods']) > 0:
            methods = results['methods']
            log.info("Found %d results" % len(methods))

            for m in methods:
                print("%s\n" % m)
        else:
            log.warn("No found methods.\n")


    # - Search commands ------------------------------------------------------
    def do_s(self, params):
        """Global search function. Type 's --help' for help."""
        try:
            args = self.s_parser.parse_args(params.split())
            p = {}
            if args.search_pattern:
                p['pattern'] = args.search_pattern

                if args.table:
                    p['table'] = args.table

                # Get results
                results = self.analysis.search(p)
                self.print_global_search(results)
            else:
                log.warn("You have to specify a search pattern!")

        except SystemExit:
            pass

    def do_sc(self, params):
        """Search for classes. Type 'sc --help' for help."""
        local_fields = self.class_fields

        try:
            args = self.sc_parser.parse_args(params.split())
            results = self.get_classes(args)

            # Exclude fields
            if args.exclude_fields:
                local_fields = [d for d in local_fields
                            if d['name'] not in args.exclude_fields]

            # Print results
            self.print_prettytable(args, local_fields, results)

        except SystemExit:
            pass

    def do_sp(self, params):
        """Search for properties. Type 'sp --help' for help."""
        local_fields = self.property_fields

        try:
            results = None

            # Parse arguments
            args = self.sp_parser.parse_args(params.split())

            if args.search_type:
                # Print available columns
                if args.search_type == '?':
                    print([c['name'] for c in t_fields])
                    return

                # Search
                if args.search_pattern:
                    if any(c['name'] == args.search_type for c in property_fields):
                        p = {
                            'type': args.search_type,
                            'pattern': args.search_pattern
                        }
                        results = self.analysis.search_property(p)
                    else:
                        log.error("No such column! Type '-c ?' for a list of available columns.")
                else:
                    log.error("No pattern (-p) specified")
            else:
                results = self.analysis.search_property()

            # Exclude fields
            if args.exclude_fields:
                local_fields = [d for d in local_fields
                            if d['name'] not in args.exclude_fields]

            # Print results
            self.print_prettytable(args, local_fields, results)

        except SystemExit:
            pass

    def do_scs(self, params):
        """Search for const strings. Type 'scs --help' for help."""
        local_fields = self.const_string_fields

        try:
            results = None

            # Parse arguments
            args = self.scs_parser.parse_args(params.split())

            if args.search_type:
                # Print available columns
                if args.search_type == '?':
                    print([c['name'] for c in local_fields])
                    return

                # Search
                if args.search_pattern:
                    if any(c['name'] == args.search_type for c in local_fields):
                        p = {
                            'type': args.search_type,
                            'pattern': args.search_pattern
                        }
                        results = self.analysis.search_const_string(p)
                    else:
                        log.error("No such column! Type '-c ?' for a list of available columns.")
                else:
                    log.error("No pattern (-p) specified")
            else:
                results = self.analysis.search_const_string()

            # Print results
            self.print_prettytable(args, local_fields, results)

        except SystemExit:
            pass

    def do_sm(self, params):
        """Search for methods. Type 'sm --help' for help."""
        local_fields = self.method_fields

        try:
            results = None

            # Parse arguments
            args = self.sm_parser.parse_args(params.split())

            if args.search_type:
                # Print available columns
                if args.search_type == '?':
                    print([c['name'] for c in local_fields])
                    return

                # Search
                if args.search_pattern:
                    if any(c['name'] == args.search_type for c in local_fields):
                        p = {
                            'type': args.search_type,
                            'pattern': args.search_pattern
                        }
                        results = self.analysis.search_method(p)
                    else:
                        log.error("No such column! Type '-c ?' for a list of available columns.")
                else:
                    log.error("No pattern (-p) specified")
            else:
                results = self.analysis.search_method()

            # Exclude fields
            if args.exclude_fields:
                local_fields = [d for d in local_fields
                            if d['name'] not in args.exclude_fields]

            # Print results
            self.print_prettytable(args, local_fields, results)

        except SystemExit:
            pass

    def do_scl(self, params):
        """Search for calls. Type 'scl --help' for help."""
        local_fields = self.call_fields

        try:
            results = None

            # Parse arguments
            args = self.scl_parser.parse_args(params.split())

            # Search for calls
            results = self.get_calls(args)

            # Exclude fields
            if args.exclude_fields:
                local_fields = [d for d in self.call_fields
                            if d['name'] not in args.exclude_fields]

            # Print results
            self.print_prettytable(args, local_fields, results)

        except SystemExit:
            pass

    def do_sxcl(self, params):
        """Search for cross calls. Type 'sxcl --help' for help."""
        local_fields = self.call_fields

        try:
            results = None
            args = self.sxcl_parser.parse_args(params.split())
            calls_args = argparse.Namespace()

            # Collect arguments
            if args.class_name:
                if args.direction == 'to':
                    calls_args.to_class = args.class_name
                elif args.direction == 'from':
                    calls_args.from_class = args.class_name

            if args.method_name:
                if args.direction == 'to':
                    calls_args.to_method = args.method_name
                elif args.direction == 'from':
                    calls_args.from_method = args.method_name

            # Get calls
            temp_results = self.get_calls(calls_args)

            # Get cross-references
            results = self.analysis.xref_call(temp_results, args.direction, args.xref_depth)

            # Exclude fields
            if args.exclude_fields:
                local_fields = [d for d in self.call_fields
                            if d['name'] not in args.exclude_fields]

            # Print results
            self.print_prettytable(args, local_fields, results)

        except SystemExit:
            pass

    # - Drawing commands -----------------------------------------------------
    def do_dc(self, params):
        """Draw classes. Type '--help' for more information."""
        try:
            args = self.dc_parser.parse_args(params.split())
            results = self.get_classes(args)

            # Create new graph
            classes_graph = ClassGraph()
            for r in results:
                classes_graph.add_class(r)

            # Finalize graph
            classes_graph.finalize()

            # Write output
            if args.output:
                classes_graph.write(args.output_format, args.output, args.output_prog, args.output_args)
                log.info("Wrote results to %s" % args.output)

        except SystemExit:
            pass

    def do_dcl(self, params):
        """Draw calls. Type '--help' for more information."""
        try:
            args = self.dcl_parser.parse_args(params.split())
            results = self.get_calls(args)

            # Create new graph
            calls_graph = CallGraph()
            for r in results:
                calls_graph.add_call(r)

            # Finalize graph
            calls_graph.finalize()

            # Write output
            if args.output:
                if results:
                    calls_graph.write(
                        args.output_format, args.output,
                        args.output_prog, args.output_args)
                    log.info("Wrote results to %s" % args.output)
                else:
                    log.info("No results :(")

        except SystemExit:
            pass

    def do_dxcl(self, params):
        """Draw cross calls. Type '--help' for more information."""
        try:
            args = self.dxcl_parser.parse_args(params.split())
            calls_args = argparse.Namespace()

            if args.class_name:
                if args.direction == 'to':
                    calls_args.to_class = args.class_name
                elif args.direction == 'from':
                    calls_args.from_class = args.class_name

            if args.method_name:
                if args.direction == 'to':
                    calls_args.to_method = args.method_name
                elif args.direction == 'from':
                    calls_args.from_method = args.method_name

            log.info(calls_args)
            # Get calls
            results = self.get_calls(calls_args)

            # Get cross-references
            xresults = self.analysis.xref_call(results, args.direction, args.xref_depth)

            # Create new graph
            calls_graph = CallGraph()

            for r in xresults:
                calls_graph.add_call(r)

            # Finalize graph
            calls_graph.finalize()

            # Write output
            if args.output:
                calls_graph.write(args.output_format, args.output, args.output_prog, args.output_args)
                log.info("Wrote results to %s" % args.output)

        except SystemExit:
            pass

    def do_quit(self, params):
        """Exists"""
        sys.exit(0)

    def do_q(self, params):
        """Exists"""
        self.do_quit(params)
