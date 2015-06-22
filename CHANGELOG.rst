===========
Changelog
===========

0.2 (2015-06-22)

* Bugs

    * Fixed issue #2
    * Fixed issue #3
    * Fixed issue described in pull #5

* Parsing

    * Added concurrency to the parser
    * You can specify by "-j" the number of jobs/workers 
    * Have a look at this `blog post <http://blog.dornea.nu/2015/05/06/adding-concurrency-to-smalisca/>`_

* Configuration
    
    * Added configuration files
    * Specify configuration file by "-c" parameter

* Web API

    * Added REST API to access the SQLite DB
    * Use http://<host>:<port>/api/<table name> to access JSON data
    * Based on `Flask <http://flask.pocoo.org/>`_ and `Flask Restless <https://flask-restless.readthedocs.org/en/latest/>`_


0.1 (2015-04-01)
================

* General
   
    * Minor bugs
    * Small changes related to versioning
    * Create PyPI package

* Parser
    
    * Parse for const string (const-string) as well

* Analyzer

    * Added analyzer command (scs) for const strings
    * Added global search
    * Search for pattern(s) in tables

* Added Makefile

    * Use make {install, uninstall, clean}


0.1-RC1 (2015-03-11)
====================

* Implemented basic project structure 
  
    * Basic CLI application
    * Use cement als stable CLI framework

* Add basic parsing functionalities 

    * Parse classes, methods, properties
    * JSONify results
    * No use of complex regexp (due to performance issues)

* Add filter functionalities

    * Search for classes, methods, properties
    * Create directed graphs (CFGs)

* Output results 

    * JSON
    * DOT (Graphviz)
