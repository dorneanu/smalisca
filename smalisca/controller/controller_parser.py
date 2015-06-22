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

import multiprocessing
import os
from cement.core import controller
from cement.core.controller import CementBaseController


class SmaliParserProcess(multiprocessing.Process):
    """Implements a multiprocessing.Process

    Attributes:
        dirs (list): List of directory paths
        files (list): List of file paths
    """

    def __init__(self, dirs, suffix, result_queue):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue
        self.dirs = dirs
        self.suffix = suffix

    def run(self):
        """Runs the process"""
        c = 0
        for d in self.dirs:
            log.info("%s %d/%d Parsing %s ... " % (self.name, c, len(self.dirs), d))

            # Parse directory
            parser = SmaliParser(d, self.suffix)
            parser.run()

            # Get and save results
            res = parser.get_results()
            self.result_queue.put(res)
            c += 1


class ConcurrentParser():
    """Implements concurrency features

    Attributes:
        processes (list): List of processes/workers
        location (str): Path location
        suffix (str): File suffix
        jobs (int): Number of max allowed workers
        depth (int): Recursion level for directories depth
        result_queue (Queue): Proxy to some thread-safe queue
    """

    # Use a manager to proxy access to the real queue
    multimanager = multiprocessing.Manager()
    result_queue = multimanager.Queue()

    processes = []

    def __init__(self, location, suffix, jobs, depth=3):
        self.location = location
        self.suffix = suffix
        self.jobs = jobs
        self.depth = depth - 1

    def walk_location(self):
        """Walk through location and return lists of files and directories

        Args:
            location (str): Location path where to lookup for files and dirs

        Returns:
            tuple: (<list of dirs>, <list of files>)

        """
        file_list = []
        dirs_list = []

        startinglevel = self.location.count(os.sep)

        # "Walk" through location
        for root, dirs, files in os.walk(self.location):
            depth = root.count(os.sep) - startinglevel

            # Collect dirs
            for d in dirs:
                dirpath = os.path.join(root, d)

                if (os.path.isdir(dirpath)) and (depth == self.depth):
                        log.info("Adding %s to list" % dirpath)
                        dirs_list.append(dirpath)

            # Collect files
            for filename in files:
                filepath = os.path.join(root, filename)

                if os.path.isfile(filepath):
                    file_list.append(filepath)

        # Save results
        self.dirs = dirs_list
        self.files = file_list

    def run(self):
        """Parallelize parsing

        Split input list into sublists according to the number of
        specified jobs. Create new processes/workers and let them
        do the parsing job.
        """
        # Create sub-lists
        for i in range(0, self.jobs):
            sub_list = [self.dirs[j] for j in range(0, len(self.dirs))
                        if j % self.jobs == i]

            # Create new process
            if len(sub_list) > 0:
                p = SmaliParserProcess(sub_list, self.suffix, self.result_queue)
                self.processes.append(p)

        # Start processes
        for p in self.processes:
            p.start()

        # Exit the completed processes
        for p in self.processes:
            p.join()

        # Get results

    def get_results(self):
        """Merges results"""
        results = []
        queue_elements = [self.result_queue.get() for p in self.processes]
        for e in queue_elements:
            for r in e:
                results.append(r)

        return results


class ParserController(CementBaseController):
    """CLI Controller for parsing Smali files

    Iterate through files and extract data from files:

        * classes (name, type)
        * class properties (name, type)
        * methods (name, type, arguments, return value)
        * calls (source, destination, arguments)

    After extracting the information, the controller will
    save the results either as **JSON** or **SQLite DB**.

    Attributes:
        location (str): Path where to lookup for files and dirs
        suffix (str): File name suffix to lookup
        jobs (int): Number of jobs to be created (default: 1)
    """

    class Meta:
        label = 'parser'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = config.HelpMessage.PARSER_HELP

        arguments = config.COMMON_ARGS + [
            (['-j', '--jobs'],
                dict(help="Number of jobs/processes to be used", type=int)),
            (['-l', '--location'],
                dict(help="Set location (required)", required=True)),
            (['-d', '--depth'],
                dict(help="Path location depth", type=int)),
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

            # How many jobs (workers)?
            if self.app.pargs.jobs and self.app.pargs.jobs > 0:
                self.jobs = self.app.pargs.jobs
            else:
                self.jobs = multiprocessing.cpu_count()

            # Walk location to which depth?
            if self.app.pargs.depth and self.app.pargs.depth > 0:
                self.depth = self.app.pargs.depth
            else:
                self.depth = 1

            # Create new concurrent parser instance
            concurrent_parser = ConcurrentParser(
                self.location, self.suffix,
                self.jobs, self.depth)
            concurrent_parser.walk_location()
            concurrent_parser.run()

            # Output results
            if (self.app.pargs.output) and (self.app.pargs.fileformat):
                results = concurrent_parser.get_results()
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
