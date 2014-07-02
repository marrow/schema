=============
Marrow Schema
=============

    A generic declarative syntax toolkit that uses itself to define itself.  Really.

..

    © 2013-2014 Alice Bevan-McGregor and contributors.

..

    https://github.com/marrow/marrow.schema

..

    |masterstatus|

1. What is Marrow Schema?
=========================

Marrow Schema is a tiny and fully tested, Python 2.7 and 3.2+ compatible declarative syntax toolkit.  This basically
means you use high-level objects to define other high-level object data structures.  Simplified: you'll never have
to write a class constructor that only assigns instance variables again.

Examples of use include:

* Attribute-access dictionaries with predefined "slots".

* The object mapper aspect of an ORM or ODM for database access.

* `Marrow Interface <https://github.com/marrow/marrow.interface>`_, declarative schema validation for arbitrary Python
  objects similar in purpose to ``zope.interface`` or Python's own abstract base classes.

* `Marrow Widgets <https://github.com/marrow/marrow.widgets>`_ are defined declaratively allowing for far more flexible
  and cooperative subclassing.


1.1 Goals
---------

Marrow Schema was created with the goal of extracting a component common to nearly every database ORM, ODM, and widget
system into a shared library to benefit all.  While some of the basic principles (data descriptors, etc.) are simple,
few implementations are truly complete.  Often you would lose access to standard Python idioms, such as the use of
positional arguments with class constructors.

With a proven generic implementation we discovered quickly that the possibilities aren't limited to the typical uses.
One commercial project that uses Marrow Schema does so to define generic CRUD controllers declaratively, greatly
reducing development time and encouraging WORM (write-once, read-many) best practice.

Marrow Schema additionally aims to have a very narrow scope and to "eat its own dog food", using a declarative syntax
to define the declarative syntax. This is in stark contrast to alternatives (such as
`scheme <https://github.com/siq/scheme/>`_) which utilize multiple metaclasses and a hodge-podge of magical attributes
internally.  Or `guts <https://github.com/emolch/guts/>`_, which is heavily tied to its XML and YAML data processing
capabilities.  Neither of these currently support positional instantiation, and both can be implemented as a superset
of Marrow Schema.


2. Installation
===============

Installing ``marrow.schema`` is easy, just execute the following in a terminal::

    pip install marrow.schema

If you add ``marrow.schema`` to the ``install_requires`` argument of the call to ``setup()`` in your applicaiton's
``setup.py`` file, Marrow Schema will be automatically installed and made available when your own application or
library is installed.  We recommend using "less than" version numbers to ensure there are no unintentional
side-effects when updating.  Use ``marrow.schema<1.1`` to get all bugfixes for the current release, and
``marrow.schema<2.0`` to get bugfixes and feature updates while ensuring that large breaking changes are not installed.


2.1. Development Version |developstatus|
----------------------------------------

Development takes place on `GitHub <https://github.com/>`_ in the
`marrow.schema <https://github.com/marrow/marrow.schema/>`_ project.  Issue tracking, documentation, and downloads
are provided there.

Installing the current development version requires `Git <http://git-scm.com/>`_, a distributed source code management
system.  If you have Git you can run the following to download and *link* the development version into your Python
runtime::

    git clone https://github.com/marrow/marrow.schema.git
    (cd marrow.schema; python setup.py develop)

You can then upgrade to the latest version at any time::

    (cd marrow.schema; git pull; python setup.py develop)

If you would like to make changes and contribute them back to the project, fork the GitHub project, make your changes,
and submit a pull request.  This process is beyond the scope of this documentation; for more information see
`GitHub's documentation <http://help.github.com/>`_.


3. Basic Concepts
=================

There are four main classes provided for implementors:

3.1. Container
--------------

This class provides the underlying machinery for processing arguments and assigning values to instance attributes at
class instantiation time.  Basically it provides ``__init__`` so you don't have to.

You can extend this to support validation during instantiation, for example, to check for required values.

3.2. DataAttribute
------------------

The base attribute class which implements the descriptor protocol, pulling the instance value of the attribute from
the containing object's ``__data__`` dictionary.  If an attempt is made to read an attribute that does not have a
corresponding value in the data dictionary an ``AttributeError`` will be raised.

3.3. Attribute
--------------

A subclass of ``DataAttribute`` which adds the ability to re-name the ``__data__`` key (name) and define a default
value.

3.4. Attributes
---------------

A declarative attribute you can use in your own ``Container`` subclasses to provide views across the known attributes
on that container.  Can provide a filter (which uses ``isinstance``) to limit to specific attributes.

Always results in an ``OrderedDict``.


4. License
==========

Marrow Schema has been released under the MIT Open Source license.

4.1. The MIT License
--------------------

Copyright © 2013-2014 Alice Bevan-McGregor and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.. |masterstatus| image:: https://secure.travis-ci.org/marrow/marrow.schema.png?branch=master

.. |developstatus| image:: https://secure.travis-ci.org/marrow/marrow.schema.png?branch=develop
