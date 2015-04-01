=========================================
Static Code Analysis for Smali
=========================================

If you ever have looked at Android applications you know to appreciate
the ability of analyzing your target at the most advanced level. Dynamic
programm analysis will give you a pretty good overview of your applications
activities and general behaviour. However sometimes you'll want to just
analyze your application **without** running it. You'll want to have a look
at its components, analyze how they interact and how data is tainted
from one point to another.

This is was the major factor driving the development of *smalisca*. There
are indeed some good reasons for a *static code analysis* before the
*dynamic* one. Before interacting with the application I like to know
how the application has been build, if there is any API and generate all
sort of *call flow graphs*. In fact graphs have been very important to
me since they *visualize* things. Instead of jumping from file to file,
from class to class, I just look at the graphs.

While graph building has been an important reason for me to code such a
tool, *smalisca* has some other neat **features** you should read about.


Features
========

At the moment there are some few major functionalities like:

* **parsing**

  You can parse a whole directory of **Smali** files and **extract**:

  * class information
  * class properties
  * class methods
  * calls between methods of different classes

  You can then **export** the results as **JSON** or **SQLite**.

  Have a loot at the `parsing page <http://smalisca.readthedocs.org/en/latest/parsing.html>`_ for more information.



* **analyzing**

  After exporting the results you'll get an **interactive prompt** to take
  a closer look at your parsed data. You can **search** for classes, properties,
  methods and even method calls. You can then apply several **filters** to your search
  criterias like::

      smalisca> sc -c class_name -p test -r 10 -x path -s class_type

  This command will search for *10* (-r 10) classes which contain the pattern *test* (-p)
  in their *class name* (-c). Afterwards  the command will exclude the column *path*
  (-x path) from the results and sort them by the *class type* (-s).

  Let's have a look at another example::

      smalisca> scl -fc com/android -fm init -r 10

  This will search for all **method calls** whose *calling* class name contains the pattern
  *com/android* (-fc). Additionally we can look for calls originating from methods whose
  name contain the pattern *init* (-fm).

  You can of course read your commands from a file and analyze your results in a *batch*-
  like manner::

    $ cat cmd.txt
    sc -c class_name -p com/gmail/xlibs -r 10 -x path
    quit
    $ ./smalisca.py analyzer -i results.sqlite -f sqlite -c cmd.txt
    ...

  Have a loot at the `analysis page <http://smalisca.readthedocs.org/en/latest/analysis.html>`_ for more information.



* **visualizing**

  I think this the **most** valuable feature of *smalisca*. The ability to visualize your
  results in a structured way makes your life more comfortable. Depending on what you're
  interested in, this tool has several graph drawing features I'd like to promote.

  At first you can draw your packages including their classes, properties and methods::

    smalisca> dc -c class_name -p test -f dot -o /tmp/classes.dot
    :: INFO       Wrote results to /tmp/classes.dot
    smalisca>

  This will first search classes whose class name contains *test* and then export the
  results in the **Graphviz DOT** language. You can then manually generate a graph using
  *dot*, *neato*, *circo* etc. Or you do that using the interactive prompt::

    smalisca> dc -c class_name -p test -f pdf -o /tmp/classes.pdf --prog neato
    :: INFO       Wrote results to /tmp/classes.pdf
    smalisca>

  Have a loot at the `drawing page <http://smalisca.readthedocs.org/en/latest/drawing.html>`_ for more information.

Screenshots
===========

.. figure:: http://smalisca.readthedocs.org/en/latest/_images/smalisca_search_classes.png
   :scale: 99%
   :alt: Basic usage
   
   Output results as table.
   


.. figure:: http://smalisca.readthedocs.org/en/latest/_images/smalisca_dxcl_dot_0.png
   :scale: 99%
   :alt: Cross calls
   
   Basic relationships between classes and modules.


Have a look at the `screenshots page <http://smalisca.readthedocs.org/en/latest/screenshots.html>`_.


Installation
============

Refer to the `installation page <http://smalisca.readthedocs.org/en/latest/installation.html>`_.
Requirements:

* Python (2.x / 3.x)
* `cement <http://builtoncement.com/>`_
* Graphviz
* SQLAlchemy


How to use it
=============

After installing the tool, you may want to first pick up an Android application (APK)
to play with. Use `apktool <https://code.google.com/p/android-apktool/>`_ or my own tool
`ADUS <https://github.com/dorneanu/adus>`_ to dump the APKs content. For the sake of
simplicity I'll be using **FakeBanker** which I've analyzed in a previous
`blog post <http://blog.dornea.nu/2014/07/07/disect-android-apks-like-a-pro-static-code-analysis/>`_.

First touch
-----------

But first let's have a look at the tools main options::

    $ smalisca --help
                                ___
                               /\_ \    __
      ____    ___ ___      __  \//\ \  /\_\    ____    ___     __
     /',__\ /' __` __`\  /'__`\  \ \ \ \/\ \  /',__\  /'___\ /'__`\
    /\__, `\/\ \/\ \/\ \/\ \L\.\_ \_\ \_\ \ \/\__, `\/\ \__//\ \L\.\_
    \/\____/\ \_\ \_\ \_\ \__/.\_\/\____\\ \_\/\____/\ \____\ \__/.\_\
     \/___/  \/_/\/_/\/_/\/__/\/_/\/____/ \/_/\/___/  \/____/\/__/\/_/



    --------------------------------------------------------------------------------
    :: Author:       Victor <Cyneox> Dorneanu
    :: Desc:         Static Code Analysis tool for Smali files
    :: URL:          http://nullsecurity.net, http://{blog,www}.dornea.nu
    :: Version:      1.0
    --------------------------------------------------------------------------------

    usage: smalisca.py (sub-commands ...) [options ...] {arguments ...}

    [--] Static Code Analysis (SCA) tool for Baskmali (Smali) files.

    commands:

      analyzer
        [--] Analyze results using an interactive prompt or on the command line.

      parser
        [--] Parse files and extract data based on Smali syntax.

    optional arguments:
      -h, --help            show this help message and exit
      --debug               toggle debug output
      --quiet               suppress all output
      --log-level {debug,info,warn,error,critical}
                            Change logging level (Default: info)
      -v, --version         show program's version number and exit




Parsing
-------

I'll first **parse** some directory for **Smali** files before doing the analysis stuff::

    $ smalisca parser -l ~/tmp/FakeBanker2/dumped/smali -s java -f sqlite  -o fakebanker.sqlite

    ...

    :: INFO       Parsing .java files in /home/victor/tmp/FakeBanker2/dumped/smali ...
    :: INFO       Finished parsing!
    :: INFO       Exporting results to SQLite
    :: INFO         Extract classes ...
    :: INFO         Extract class properties ...
    :: INFO         Extract class methods ...
    :: INFO         Extract calls ...
    :: INFO         Commit changes to SQLite DB
    :: INFO         Wrote results to fakebanker.sqlite
    :: INFO       Finished scanning

Also have a look at the `parsing page <http://smalisca.readthedocs.org/en/latest/parsing.html>`_ for further information.


Analyzing
----------

Now you're free to do whatever you want with your generated exports. You can inspect the **SQLite DB**
directly or use *smaliscas* **analysis** features::

    $ smalisca analyzer -f sqlite -i fakebanker.sqlite

    ...


    smalisca>sc -x path -r 10
    +----+-----------------------------------------------------------------------------------------+--------------------+--------------------------+-------+
    | id | class_name                                                                              | class_type         | class_package            | depth |
    +----+-----------------------------------------------------------------------------------------+--------------------+--------------------------+-------+
    | 1  | Landroid/support/v4/net/ConnectivityManagerCompat                                       | public             | Landroid.support.v4.net  | 5     |
    | 2  | Landroid/support/v4/view/AccessibilityDelegateCompat$AccessibilityDelegateJellyBeanImpl |                    | Landroid.support.v4.view | 5     |
    | 3  | Landroid/support/v4/view/ViewCompat$ViewCompatImpl                                      | interface abstract | Landroid.support.v4.view | 5     |
    | 4  | Landroid/support/v4/app/ActivityCompatHoneycomb                                         |                    | Landroid.support.v4.app  | 5     |
    | 5  | Landroid/support/v4/app/NoSaveStateFrameLayout                                          |                    | Landroid.support.v4.app  | 5     |
    | 6  | Landroid/support/v4/net/ConnectivityManagerCompatHoneycombMR2                           |                    | Landroid.support.v4.net  | 5     |
    | 7  | Lcom/gmail/xpack/BuildConfig                                                            | public final       | Lcom.gmail.xpack         | 4     |
    | 8  | Landroid/support/v4/app/BackStackRecord$Op                                              | final              | Landroid.support.v4.app  | 5     |
    | 9  | Landroid/support/v4/app/FragmentManagerImpl                                             | final              | Landroid.support.v4.app  | 5     |
    | 10 | Landroid/support/v4/app/ShareCompat$ShareCompatImpl                                     | interface abstract | Landroid.support.v4.app  | 5     |
    +----+-----------------------------------------------------------------------------------------+--------------------+--------------------------+-------+

Also refer to the `analysis page <http://smalisca.readthedocs.org/en/latest/analysis.html>`_ for more available **commands** and options.


Drawing
-------

Please refer to the `drawing page <http://smalisca.readthedocs.org/en/latest/drawing.html>`_ for full examples.


License
========

*smalisca* has been released under the **MIT** license. Have a look at the **LICENSE.rst** file.

Credits
=======

This tool is dedicated to **Lică**. Many thanks also go to:

* `Stephen McAllister <https://de.linkedin.com/pub/stephen-mcallister/13/843/71a>`_

    * Many thanks for all those hours full of APK debugging and great ideas

* My gf

    * Thank you very much for your patience and understanding!

* `nullsecurity.net <http://nullsecurity.net>`_

    * Hack the planet!
