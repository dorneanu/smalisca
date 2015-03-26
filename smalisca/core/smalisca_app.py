#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         core/smalisca_app.py
# Created:      2015-01-17
# Purpose:      Defines how an application is built.
#               Provides information about classes, methods and properties.
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

"""Defines the inner structures of an application"""

import json
from smalisca.core.smalisca_config import JSON_SETTINGS
from smalisca.core.smalisca_logging import log


class App:
    """Provides information about an application

    An application basically consists of several packages,
    classes, methods and so on. This class is meant to reflect
    the inner structure of an analyzed APK.

    You can add classes, methods and properties. In order to
    be able to analyze your results, you'll have to always
    have an instance of this class.

    In order to simplify data analysis an instance of class App
    can be easily exported as JSON.

    Attributes:
        name: Name of the application
        location: Location where the APK was dumped
        parser: Parser information

    """

    def __init__(self, name):
        self.name = name
        self.location = None
        self.parser = None
        self.classes = {}

    def add_location(self, location):
        """Adds application location

        Args:
            location (str): Path where the APK was dumped

        """
        self.location = location

    def add_parser(self, parser):
        """Adds parser information

        Args:
            parser (str): Parser information

        """
        self.parser = parser

    def add_class_obj(self, class_obj):
        """Adds a previsously created class object

        Args:
            class_obj (dict): A dictionary containing info about class

        """
        self.classes[class_obj['name']] = class_obj

    def add_class(self, class_obj):
        """Adds a class to the application

        Args:
            class_obj (dict): A dictionary containing info about class

        """
        classname = class_obj['name']
        self.classes[classname] = {}
        self.classes[classname]['type'] = class_obj['type']
        self.classes[classname]['parent'] = class_obj['parent']
        self.classes[classname]['path'] = class_obj['path']

        if class_obj['methods']:
            self.classes[classname]['methods'] = class_obj['methods']
        else:
            self.classes[classname]['methods'] = []

        if class_obj['properties']:
            self.classes[classname]['properties'] = class_obj['properties']
        else:
            self.classes[classname]['properties'] = []

        if class_obj['const-strings']:
            self.classes[classname]['const-strings'] = class_obj['const-strings']
        else:
            self.classes[classname]['const-strings'] = []

    def add_property(self, classname, prop):
        """Adds a property to the application

        Args:
            classname (str): The class name the property belongs to
            prop (dict): A dict containing property info

        """
        if classname in self.classes:
            self.classes[classname]['properties'].append(prop)

    def add_const_string(self, classname, const_string):
        """Adds a const-string to the application

        Args:
            classname (str): The class name the property belongs to
            const-string (dict): A dict containing const-string info

        """
        if classname in self.classes:
            self.classes[classname]['const-strings'].append(const_string)

    def add_method(self, classname, method):
        """Adds a method to the application

        Args:
            classname (str): The class name the property belongs to
            method (dict): A dict containing method info

        """
        if classname in self.classes:
            self.classes[classname]['methods'].append(method)

    def get_classes(self):
        """Return classes

        Returns:
            list: List of classes, otherwise None

        """
        data = []
        for k in self.classes.keys():
            c = self.classes[k]
            data.append({
                'name': c['name'],
                'type': c['type'],
                'package': c['package'],
                'parent': c['parent'],
                'path': c['path'],
                'depth': c['depth']
            })

        return data

    def get_properties(self):
        """Return properties

        Returns:
            list: List of properties, otherwise None

        """
        data = []
        for c in self.classes.keys():
            properties = self.classes[c]['properties']

            for p in properties:
                data.append({
                    'name': p['name'],
                    'type': p['type'],
                    'info': p['info'],
                    'class': c
                })

        return data

    def get_const_strings(self):
        """Return const strings

        Returns:
            list: List of const strings, otherwise None

        """
        data = []
        for c in self.classes.keys():
            const_strings = self.classes[c]['const-strings']

            for cs in const_strings:
                data.append({
                    'name': cs['name'],
                    'value': cs['value'],
                    'class': c
                })

        return data

    def get_methods(self):
        """Return methods

        Returns:
            list: List of methods, otherwise None

        """
        data = []
        for c in self.classes.keys():
            methods = self.classes[c]['methods']
            for m in methods:
                data.append({
                    'name': m['name'],
                    'type': m['type'],
                    'args': m['args'],
                    'return': m['return'],
                    'class': c
                })

        return data

    def get_calls(self):
        """Return calls"""
        data = []
        for c in self.classes.keys():
            methods = self.classes[c]['methods']
            for m in methods:
                for invoke in m['calls']:
                    data.append({
                        'from_class': c,
                        'from_method': m['name'],
                        'local_args': invoke['local_args'],
                        'to_class': invoke['to_class'],
                        'to_method': invoke['to_method'],
                        'dst_args': invoke['dst_args'],
                        'return': invoke['return'],
                        'class': c
                    })

        return data

    def get_all(self):
        """Returns classes, properties, methods and calls as a dict"""
        data = {
            'classes': self.get_classes(),
            'properties': self.get_properties(),
            'methods': self.get_methods(),
            'calls': self.get_calls()
        }

        return data

    def to_json(self):
        """Return app object as JSON"""
        json_data = {
            'parser': self.parser,
            'location': self.location,
            'classes': self.classes
        }
        return json.dumps(json_data, indent=JSON_SETTINGS['indent'])

    def write_json(self, filename):
        """Write app object as JSON to file"""
        try:
            with open(filename, 'w+') as f:
                json.dump(self.to_json(), f, indent=JSON_SETTINGS['indent'])

        except IOError:
            log.error("Couldn't save data to %s" % filename)

    def read_json(self, filename):
        """Create class structure from json file"""
        try:
            with open(filename, 'r') as f:
                data = json.loads(json.load(f))

                # Set classes
                if 'classes' in data:
                    self.classes = data['classes']

        except IOError:
            log.error("Couldn't read from %s" % filename)

    def __str__(self):
        """ Return app als string"""
        return self.to_json()
