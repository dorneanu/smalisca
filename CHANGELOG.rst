===========
Changelog
===========


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
