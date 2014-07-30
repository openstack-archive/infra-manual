:title: Third-Party Guide

.. _third-party_manual:

Third-Party Guide
#################

Quick Reference
===============

Here is a small schema of the components of a working Openstack CI::

    >
    >   +--------+   ssh (1)  +------------------+
    >   | gerrit | <--------> | Zuul  +----------+
    >   +--------+   event    |       | Gearmand |
    >                stream   +-------+----------+
    >                                      ^
    >                                      |
    >                                      v
    >                              +-----------+-------+
    >         +------------+       |    Jobs   |       |
    >         |  Jenkins   |       | Templates |       |
    >         |   Slave    |  ssh  +-----------+       |
    >         | (Test env) |<----->|      Jenkins      |
    >         |            |       |       Master      |
    >         +------------+       +-------------------+
    >

Understanding the CI
====================

This section describes the CI components and their roles, for you to understand
how the CI works within openstack's infrastructure. The best way for you to set
up your third-party CI is to reproduce this setup.

Zuul
----
* server
* merger

Gearmand
--------
* run internally by zuul
* communication zuul-jenkins

Jenkins
-------
* Defines Job templates for zuul to instantiate
* Actual CI Job-manager

Getting Started
===============

Account Setup
-------------
* Point to third_party.rst for System Account Requesting
* Remind role and limitations of a System Account


Installing the CI components
============================

Most of the install process is relatively eased by jaypipes puppet scripts,
even though they might generate some errors.

There is a script for installing the Jenkins master (installs zuul too),
and one for the jenkins slave.

Zuul
----
Should be installed by jaypipes' scripts.

Jenkins
-------
* Advised to use latest stable release from jenkins instead of official
  package (that's how openstack-infra does this)

Issues with jaypipe's scripts
-----------------------------
* zuul's layout.yaml regexp for recheck syntax are outdated
* Jobs didn't appear automagically within jenkins, manual configuration
  required
* Scripts are rigid/unclear about naming some parts differently than what
  jaypipe's tutorial explains (name of the slave node, path to jenkin's ssh
  key)
* Scripts remove passworded ssh access to the servers. Beware if you want to
  keep it


Configuring your CI system
==========================

Configuring Zuul
----------------
zuul.conf relevant sections and parameters:
* [gearman]

 * server=adress

* [gearman_server]

 * start=boolean

* [gerrit]

 * server=review.openstack.org
 * user=system-account
 * sshkey=/path/to/private_key

* [zuul]

 * git_dir=/path/to/zuul/git

* [merger]

 * git_dir=/path/to/zuul/git
 * zuul_url=ssh://user@host/path/to/zuul/git (${ZUUL_URL} in Jenkins jobs)

layout.yaml:

* Point to reference yaml in openstack-infra/config
* Describe what's a pipeline and a project
* List relevant 3rd-party pipelines:

 * check (To disable reporting, comment start/success/failure blocks)

* Describe how to configure a project (git repo, piepelines to match, job
  list, etc.)

Configuring Jenkins
-------------------
* Setup jenkins master/slave ssh channel: User + SSH Key
* List relevant ZUUL parameters (or link to relevant page) for understanding
* Configuring a job template (manually?):

 * Create free-style job
 * Use the same name as inside zuul's pipeline/project
 * Source code management:

  * Select 'git':

   * url = ${ZUUL_URL}/PROJECT  (project might be openstack-dev/sandbox for
     sandbox testing)
   * select credentials for slave/master communication (for cloning
     zuul-merger's git branch)
   * In advanced mode: Set Refspec=${ZUUL_REF}
   * branch=${ZUUL_COMMIT}


Testing and Debugging your CI system
====================================

Checking gearman connection
---------------------------
* From command line to see the configured jenkins jobs and zuul tasks::
   $> echo status | nc -q 3 localhost 4730
* From jenkins in the configuration section, click the check connection button

Test against openstack-dev/sandbox
----------------------------------
* Try the recheck syntaxes, comments, commits

