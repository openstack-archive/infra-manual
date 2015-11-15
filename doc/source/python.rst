:title: Python Developer's Guide


Python Developer's Guide
#########################


The goal of this document is to explain OpenStack wide standard
practices around the use of Python.

.. _python_unit_tests:

Running Python Unit Tests
=========================

Before submitting your change, you should test it. Repositories generally have
several categories of tests:

* Style Checks -- Check source code for style issues
* Unit Tests --  Self contained in each repository
* Integration Tests -- Require a running OpenStack environment

This section covers how to run the style check and unit tests. Both are run
through `Tox`_.

.. _`Tox`: https://tox.readthedocs.org/en/latest/


Install `pip`_::

  [apt-get | yum] install python-pip

Use pip to install tox::

  pip install --upgrade tox


.. _`pip`: http://pip.readthedocs.org/en/latest/installing/

Run The Tests
^^^^^^^^^^^^^

Navigate to the repository's root directory and execute::

  tox

Note: completing this command may take a long time (depends on system resources),
also you might not see any output until tox is complete.


Run One Set of Tests
^^^^^^^^^^^^^^^^^^^^

Tox will run your entire test suite in the environments specified in the
repository tox.ini::

  [tox]

  envlist = <list of available environments>

To run just one test suite in envlist execute::

  tox -e <env>

so for example, run the test suite in py27::

  tox -e py27


Running the style checks
^^^^^^^^^^^^^^^^^^^^^^^^^

Just run::

  tox -e pep8

Run One Test
^^^^^^^^^^^^

To run individual tests with tox:

If `testr`_ is in tox.ini, for example::

  [testenv]

  ... "python setup.py testr --slowest --testr-args='{posargs}'"

Run individual tests with the following syntax::

  tox -e <env> -- path.to.module:Class.test

So for example, run the test_memory_unlimited test in openstack/nova::

  tox -e py27 -- nova.tests.unit.compute.test_claims.ClaimTestCase.test_memory_unlimited

If `nose`_ is in tox.ini, for example::

  [testenv]

  ... "nosetests {posargs}"

Run individual tests with the following syntax::

  tox -e <env> -- --tests path.to.module:Class.test

So for example, run the list test in openstack/swift::

  tox -epy27 -- --tests test.unit.container.test_backend:TestContainerBroker.test_empty

.. _`testr`: https://wiki.openstack.org/wiki/Testr
.. _`nose`: https://nose.readthedocs.org/en/latest/
