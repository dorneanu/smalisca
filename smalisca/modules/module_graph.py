#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         modules/module_graph.py
# Created:      2015-02-07
# Purpose:      Create graphs from generated results
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

"""Graph module for visualizing results"""

import graphviz as gv

from smalisca.core.smalisca_config import GraphConfig
from smalisca.core.smalisca_logging import log


# Useful functions found on http://matthiaseisen.com/articles/graphviz/
def add_nodes(graph, nodes):
    """ Add node(s) to graph

    Args:
        graph (Graph): Graph to add node(s) to
        nodes (list): List of nodes

    Returns:
        Graph: Return the modified graph

    """
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph


def add_edges(graph, edges):
    """Add edge(s) to graph

    Args:
        graph (Graph): Graph to add edge(s) to
        edges (list): List of edges

    Returns:
        Graph: Return the modified graph

    """
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph


def apply_styles(graph, styles):
    """ Apply styles to graph

    Note:
        Also have a look at :class:`smalisca.core.GraphConfig`

    Args:
        graph (Graph): Graph to apply styles to
        styles (dict): List of styles

    Returns:
        Graph: Return modified Graph

    Examples:

        # Define styles
        graph_styles = {
            'graph': {
                'rankdir': 'LR',
                'splines': 'ortho',
                'bgcolor': 'black'
            },
            'nodes': {
                'shape': 'record',
                'color': 'orange',
                'fontcolor': 'orange',
                'style': 'filled',
                'fillcolor': '#1c1c1c'
            },
            'edges': {
                'color': 'orange'
            }
        }

        # Apply styles
        apply_styles(myGraph, graph_styles)

    """
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )


class GraphBase(object):
    """Base graph interface"""

    def set_engine(self, engine):
        """Sets graphviz engine

        Args:
            engine (str): neato, dot, fdp, etc.

        """
        self.G._engine = engine

    def set_format(self, output_format):
        """Sets graphviz output format

        Args:
            output_format (str): png, pdf, dot, svg, etc.

        """
        self.G._format = output_format

    def write(self, output_format, filename, prog='dot', args=''):
        """Write graph to specified filename"

        Note:
            Due to the implementation of the python graphviz module, the graphviz code
            AND the rendered image will be saved as well.

            For example if you call:
                write(output_format='png', filename='/tmp/new')

            You'll get:
                * /tmp/new - Containing the graphviz code
                * /tmp/new.png - Containing the rendered graphviz code

        Args:
            output_format (str): The output format to save the graph in (pdf, png, jpg, etc.)
            filename (str): File path where to store results
            prog (str): Specify graphviz engine to use (dot, neato, etc.)
            args (str): Additional args to the grapviz engine

        """
        import os

        if output_format == 'dot':
            self.G.save(filename=filename)
        else:
            output_dir, output_filename = os.path.split(filename)
            output_filename = os.path.splitext(os.path.basename(output_filename))[0]
            output_path = output_dir + "/" + output_filename

            self.set_format(output_format)
            self.set_engine(prog)

            # Render graphviz source code
            self.G.render(filename=output_path)


class ClassGraph(GraphBase):
    """Graphical representation of classes

    Attributes:
        G (Digraph): Graphviz Graph
        classes (dict): Collected classes
        subgraphs (dict): Use unique subgraphs
        edges (list): List of available edges

    """

    def __init__(self):
        self.G = gv.Digraph()

        self.packages = {}
        self.classes = {}
        self.subgraphs = {}
        self.edges = []

    def add_class(self, class_obj):
        """Add new class object to graph

        Args:
            class_obj (dict): Class dict as obtained directly from the DB

        """

        # First add a package node
        if class_obj.class_package not in self.packages:
            # Create new graph
            subgraph = gv.Digraph(
                name='cluster_%s' % class_obj.class_package)

            # Add additional attributes
            subgraph.body.append('label = "%s"' % class_obj.class_name)

            # Add new node
            add_nodes(subgraph, [
                (
                    '%s' % class_obj.class_package,
                    {
                        'label': class_obj.class_package
                    }
                )
            ])

            package_node = class_obj.class_package
            self.packages[package_node] = subgraph
            package_graph = subgraph
        else:
            package_node = class_obj.class_package
            package_graph = self.packages[package_node]

        class_label = "--- %s\\r\\r" % class_obj.class_name

        # Add properties
        class_label += "Properties:\l\l"
        for p in class_obj.properties:
            class_label += "[P] %s %s\l" % (p.property_type, p.property_name)

        # Add methods to graph
        class_label += "\l\lMethods:\l\l"
        for m in class_obj.methods:
            # method_node = "%s_method_%d" % (class_obj.class_name, m.id)
            class_label += "[M] %s %s()\l" % (m.method_type, m.method_name)

        # Add class node
        class_node = "%s_class_%d" % (class_obj.class_name, class_obj.id)

        # Add class node to package graph
        node_attr = {'label': class_label}

        # Add methode node attributes
        for k in GraphConfig.ClassGraphConfig.class_nodes['nodes'].keys():
            node_attr[k] = GraphConfig.ClassGraphConfig.class_nodes['nodes'][k]

        add_nodes(package_graph, [(class_node, node_attr)])

        # Add edge
        if not (package_node, class_node) in self.edges:
            add_edges(package_graph, [((package_node, class_node))])
            self.edges.append((package_node, class_node))
        else:
            log.info("match")

        if class_obj.class_package not in self.subgraphs:
            self.subgraphs[class_obj.class_package] = package_graph

    def finalize(self):
        """Finalize graph

        After all classes have been inserted into the graph,
        generate subgraphs and apply graph styles

        """

        # First make subgraphs
        for k in self.subgraphs.keys():

            # Add styles
            apply_styles(self.subgraphs[k], GraphConfig.ClassGraphConfig.cluster_styles)

            # Make subgraph
            self.G.subgraph(self.subgraphs[k])

        # Add global graph styles
        apply_styles(self.G, GraphConfig.ClassGraphConfig.graph_styles)


class CallGraph(GraphBase):
    """Graphical representation of calls

    Attributes:
        G (Digraph): Graphviz graph
        packages (dict): Available packages
        subgraphs (dict): Available subgraphs
        edges (list): Available edges
        classes (dict): Available classes

    """

    def __init__(self):
        self.G = gv.Digraph()
        self.packages = {}
        self.subgraphs = {}
        self.edges = []
        self.classes = {}

    def add_class_subgraph(self, class_node):
        """Adds a new subgraph depending on the node

        Args:
            class_node (str): Name of the new class node

        Returns:
            Graph: Returns a sub-graph

        """

        # Check if node already in graph
        if class_node not in self.classes:

            # Create new graph
            class_subgraph = gv.Digraph(
                name='cluster_%s' % class_node)

            # Add additional attributes
            class_subgraph.body.append('compound = "true"')
            class_subgraph.body.append('label = "%s"' % class_node)

            # Add invsible class subgraph node
            add_nodes(class_subgraph, [
                (
                    '%s' % class_node,
                    {
                        'label': class_node, 'style': 'invis'
                    }
                )
            ])

            # Add new graph
            self.classes[class_node] = {}
            self.classes[class_node]['graph'] = class_subgraph

            # Add empty methods list
            self.classes[class_node]['methods'] = []
        else:
            class_subgraph = self.classes[class_node]['graph']

        return class_subgraph

    def add_call(self, call_obj):
        """Add new call object to graph

        Args:
            call_obj (dict): Call object as obtained directly from the DB

        """

        # From
        from_class_node = call_obj.from_class
        from_method_node = "%s_%s" % (from_class_node, call_obj.from_method)

        # Destination
        to_class_node = call_obj.dst_class
        to_method_node = "%s_%s" % (to_class_node, call_obj.dst_method)

        # Add new subgraphs
        from_subgraph = self.add_class_subgraph(from_class_node)
        to_subgraph = self.add_class_subgraph(to_class_node)

        # Add from_method
        if from_method_node not in self.classes[from_class_node]['methods']:
            method_node_attr = {'label': "[M] %s\l" % call_obj.from_method}

            # Add additional methode node attributes
            for k in GraphConfig.CallsGraphConfig.method_nodes['nodes'].keys():
                method_node_attr[k] = GraphConfig.CallsGraphConfig.method_nodes['nodes'][k]

            # Add node
            add_nodes(from_subgraph, [(
                from_method_node, method_node_attr

            )])
            self.classes[from_class_node]['methods'].append(from_method_node)

        # Add to_method
        if to_method_node not in self.classes[to_class_node]['methods']:
            method_node_attr = {'label': "[M] %s\l" % call_obj.dst_method}

            # Add methode node attributes
            for k in GraphConfig.CallsGraphConfig.method_nodes['nodes'].keys():
                method_node_attr[k] = GraphConfig.CallsGraphConfig.method_nodes['nodes'][k]

            # Add node
            add_nodes(to_subgraph, [(
                to_method_node, method_node_attr
            )])
            self.classes[from_class_node]['methods'].append(to_method_node)

        # Add edge <from_method> -> <to_method>
        if not "%s-%s" % (from_method_node, to_method_node) in self.edges:
            edge_attr = {}

            # Add edge attributes
            for k in GraphConfig.CallsGraphConfig.method_edges['edges'].keys():
                edge_attr[k] = GraphConfig.CallsGraphConfig.method_edges['edges'][k]

            # Add edge
            add_edges(self.G, [
                ((from_method_node, to_method_node), edge_attr)
            ])
            self.edges.append("%s-%s" % (from_method_node, to_method_node))

    def finalize(self):
        """Finalizes graph

        Make subgraphs and apply graph styles.

        """

        # First make subgraphs
        for k in self.classes.keys():

            # Apply styles
            apply_styles(self.classes[k]['graph'], GraphConfig.CallsGraphConfig.cluster_styles)

            # Make subgraph
            self.G.subgraph(self.classes[k]['graph'])

        # Apply general graph styles
        apply_styles(self.G, GraphConfig.CallsGraphConfig.graph_styles)
