:title: Zuul v3 Migration Guide

Zuul v3 Migration Guide
#######################

This is a temporary section of the Infra Manual to assist in the
conversion to Zuul v3.  Some of the content herein will only be
relevant before and shortly after we move from Zuul v2 to v3.

What is Zuul v3?
================

Zuul v3 is the third major version of the project gating system
developed for use by the OpenStack project as part of its software
development process.  It includes several major new features and
backwards incompatible changes from previous versions.

It was first described in the `Zuul v3 spec`_.

In short, the major new features of interest to OpenStack developers
are:

* In-repo configuration
* Native support for multi-node jobs
* Ansible job content
* Integration with more systems

We're pretty excited about Zuul v3, and we think it's going to improve
the devolpment process for all OpenStack developers.  But we also know
that not everyone needs to know everything about Zuul v3 in order for
this to work.  The sections below provide increasing amounts of
information about Zuul v3.  Please at least read the first section,
and then continue reading as long as subsequent sections remain
relevant to the way you work.

.. _Zuul v3 spec: http://specs.openstack.org/openstack-infra/infra-specs/specs/zuulv3.html

What's the Minimum I Need to Know?
==================================

You have stuff to do, and most of it doesn't involve the CI system, so
this will be short.

The name of the CI system will be changing
------------------------------------------

For varied historical reasons, the name OpenStack's CI system used to
report to Gerrit has been Jenkins, even 5 years after it actually
became Zuul doing the reporting and 1 year after we stopped using
Jenkins altogether.  We're *finally* changing it to Zuul.  If you see
a comment from **Jenkins**, it's Zuul v2.  If you see a comment from
**Zuul**, it's Zuul v3.

Job names will be changing
--------------------------

In Zuul v2, almost every project has a unique ``python27`` job.  For
example, ``gate-nova-python27``.  In v3, we will have a single python27
job that can be used for every project.  So when Zuul reports on your
changes, the job name will now be ``openstack-py27`` rather than
``gate-project-python27``.

For details about job names, see :ref:`v3_naming`.

Most jobs will be migrated automatically
----------------------------------------

The jobs covered by the Consistent Testing Interface will all be
migrated automatically and you should not need to do anything.  Most
devstack jobs should be migrated as well.  If your project uses only
these jobs, you shouldn't need to do anything; we'll handle it for
you.

If you have custom jobs for your project, you or someone from your
project should keep reading this document.

.. TODO: console logs and other reporting changes

My Project Has Customized Jobs, Tell Me More
============================================

If you've read this far, you may have a passing familiarity with the
project-config repo and you have created some jobs of your own, or
customized how jobs are run on your project.

As mentioned earlier, we're going to try to automatically migrate all
of the jobs from v2 to v3.  However, some jobs may benefit from
further manual tweaks.  This section and the one following should give
you the information needed to understand how to make those.

How Jobs Are Defined in Zuul v3
-------------------------------

In Zuul v2, jobs were defined in Jenkins and Zuul merely instructed
Jenkins to run them.  This split between job definition and execution
produced the often confusing dual configuration in the project-config
repository, where we were required to define a job in ``jenkins/jobs``
and then separately tell Zuul to run it in ``zuul/layout.yaml``.

Zuul v3 is responsible for choosing when to run which jobs, and
running them; jobs only need to be added to one system.

All aspects of Zuul relating to jobs are configured with YAML files
similar to the Zuul v2 layout.  See the `Zuul User Guide
<https://docs.openstack.org/infra/zuul/feature/zuulv3/user/config.html#job>`_
for more information on how jobs are configured.

Where Jobs Are Defined in Zuul v3
---------------------------------

Zuul v3 loads its configuration directly from git repos.  This lets
us accomplish a number of things we have long desired: instantaneous
reconfiguration and in-repo configuration.

Zuul starts by loading the configuration in the `project-config
repository
<https://git.openstack.org/cgit/openstack-infra/project-config/tree/zuul.yaml>`_.
This contains all of the pipeline definitions and some very basic job
definitions.  Zuul looks for its configuration in files named
``zuul.yaml`` or ``.zuul.yaml``, or in directories named ``zuul.d`` or
``.zuul.d``.  Then it loads configuration from the `zuul-jobs
repository
<https://git.openstack.org/cgit/openstack-infra/zuul-jobs/tree/zuul.yaml>`_. This
repository contains job definitions intended to be used by any Zuul
installation, including, but not limited to, OpenStack's Zuul.  Then
it loads jobs from the `openstack-zuul-jobs repository
<http://git.openstack.org/cgit/openstack-infra/openstack-zuul-jobs/tree/zuul.yaml>`_
which is where we keep most of the OpenStack-specific jobs.  Finally,
it loads jobs defined in all of the repositories in the system.  This
means that any repo can define its own jobs.  And in most cases,
changes to those jobs will be self-testing, as Zuul will dynamically
change its configuration in response to proposed changes.

This is very powerful, but there are some limitations.  See the
sections of the Zuul User Guide about `Security Contexts
<https://docs.openstack.org/infra/zuul/feature/zuulv3/user/config.html#security-contexts>`_
and `Configuration Loading
<https://docs.openstack.org/infra/zuul/feature/zuulv3/user/config.html#configuration-loading>`_
for more details.

Note that all OpenStack projects share a single namespace for job
names, so we have established some guidelines detailed in
:ref:`v3_naming` for how to name jobs.  Adhere to these so that we may
avoid collisions between jobs defined in various repositories.

Zuul jobs are documented in their own repositories.  Here are links to
the documentation for the repositories mentioned above:

* `zuul-jobs documentation <https://docs.openstack.org/infra/zuul-jobs/>`_
* `openstack-zuul-jobs documentation <https://docs.openstack.org/infra/openstack-zuul-jobs/>`_

How Jobs Are Selected to Run in Zuul v3
---------------------------------------

How Zuul v3 determines which jobs are run (and with which parameters)
is, to put it mildly, different than Zuul v2.

In Zuul v2, we accomplished most of this with 2,500 lines of
incomprehensible regular expressions.  They are gone in v3.
Instead we have a number of simple concepts that work together to
allow us to express when a job should run in a human-friendly manner.

.. sidebar:: Further reading

   Jobs, variants, and matchers are discussed in more detail in the
   `Job section of the Zuul manual
   <https://docs.openstack.org/infra/zuul/feature/zuulv3/user/config.html#job>`_

Job definitions may appear more than once in the Zuul configuration.
We call the first instance the *reference* definition, and subsequent
definitions *variants*.  Job definitions have several fields, such as
``branches`` and ``files``, which act as *matchers* to determine
whether the job is applicable to a change.  When Zuul runs a job, it
builds up a new job definition with all of the matching variants
applied.  Later variants can override settings on earlier definitions,
but any settings not overridden will be present as well.

For example, consider this simple reference job definition for a job
named ``fedstack``:

.. code-block:: yaml

   - job:
       name: fedstack
       nodes: fedora-26
       vars:
         neutron: true

This may then be supplemented with a job variant:

.. code-block:: yaml

   - job:
       name: fedstack
       branches: stable/pike
       nodes: fedora-25

This variant indicates that, while by default, the fedstack job runs
on fedora-26 nodes, any changes to the stable/pike branch should run
on fedora-25 nodes instead.  In both cases, the ``neutron`` variable
will be set to ``true``.

Such job variants apply to any project that uses the job, so they are
appropriate when you know how the job should behave in all
circumstances.  Sometimes you want to make a change to how a job runs,
but only in the context of a specific project.  Enhancements to the
project definition help with that.  A project definition looks like
this:

.. code-block:: yaml
   :emphasize-lines: 3-5

   - project:
       name: openstack/cloudycloud
       check:
         jobs:
           - fedstack

We call the highlighted portion the ``project-pipeline`` definition.
That says "run the fedstack job on changes to the cloudycloud project
in the check pipeline".  A change to the master branch of cloudycloud
will run the job described in the reference definition above.  A
change on the stable/pike branch will combine *both* the reference
definition and the variant and use the new merged definition when
running the job.

If we want to change how the job is run *only* for the cloudycloud
project, we can alter the project-pipeline definition to specify a
project-local variant.  It behaves (almost) just like a regular job
variant, but it only applies to the project in question.  To specify
that fedstack jobs are non-voting on cloudycloud, we would do the
following:

.. code-block:: yaml
   :emphasize-lines: 3-6

   - project:
       name: openstack/cloudycloud
       check:
         jobs:
         - fedstack:
             voting: false

This variant is combined with all other matching variants to indicate
that all fedstack jobs run on cloudycloud are non-voting, and
additionally, stable/pike jobs run on fedora-25 instead of fedora-26.

One final note about variants: in some cases Zuul attaches an implied
branch matcher to job definitions.  The rules are `tricky
<https://docs.openstack.org/infra/zuul/feature/zuulv3/user/config.html#attr-job.branches>`_,
but in general, jobs and variants defined in the master branch of a
project will apply to all branches, and any further variants defined
in other branches get an implied branch matcher of their current
branch.  This makes it so that we can branch a project from master
along with all of its job definitions, and jobs will continue to work
as expected.

I Write Jobs From Scratch, How Does Zuul v3 Actually Work?
==========================================================

TODO:

* inheritance
* ansible (and how it's optional)
* playbooks
* roles

Quickstart Guide for OpenStack Projects
=======================================

This is the tl;dr guide for those who just want to add their OpenStack
project to Zuul v3. It's a simple, step-by-step howto on getting up and
going.

#. Create a ``.zuul.yaml`` file in your project. This is where you will configure
   your project and define its jobs.

#. In your ``.zuul.yaml``, define your project. You will need to identify your
   project name, which pipeline queues will run jobs, and the names of the jobs
   to run in each pipeline. Below is an example project which adds two jobs to
   the ``check`` pipeline:

   .. code-block:: yaml

      - project:
        name: openstack/<projectname>
        check:
          jobs:
            - <projectname>-functional
            - tox-py35

#. In ``.zuul.yaml``, you will also define custom jobs, if any. If you define your
   own jobs, note that job names should be prefixed with the project name to avoid
   accidentally conflicting with a similarly named job, as discussed in
   :ref:`v3_naming`.

   For our example project, our custom job is defined as:

   .. code-block:: yaml

      - job:
          name: <projectname>-functional

   The actual magic behind the ``<projectname>-functional`` job is
   found in the Ansible playbook that implements it. See the next step
   below.

   Zuul v3 comes with many pre-defined jobs that you may use. The
   non-OpenStack specific jobs, such as ``tox-py27``, ``tox-py35``,
   ``tox-pep8``, and ``tox-docs`` are defined in the file
   `zuul-jobs:main.yaml
   <https://git.openstack.org/cgit/openstack-infra/zuul-jobs/tree/zuul.yaml>`_.

   The predefined OpenStack-specific jobs, such as ``openstack-doc-build``,
   ``tox-py35-constraints``, and ``publish-openstack-python-tarball``
   are defined in the file
   `openstack-zuul-jobs:main.yaml <https://git.openstack.org/cgit/openstack-infra/openstack-zuul-jobs/tree/zuul.yaml>`_.

#. Write any Ansible playbooks for your custom jobs. By default, these
   are placed in the ``playbooks`` directory of your project. Our
   ``<projectname>-functional`` job playbook will
   be placed in the file ``playbooks/<projectname>-functional.yaml``.
   Below are the contents:

   .. code-block:: yaml

      - hosts: all
        tasks:
          - name: Run functional test script
            command: run-functional-tests.sh
            args:
              chdir: "src/{{ zuul.project.canonical_name }}"

   This playbook will execute on our host named ``ubuntu-xenial``,
   which we get for free from the Zuul base job. If you need more
   nodes, or a node of a different type, you will need to define these
   in your ``.zuul.yaml`` file.

   Note that some playbook actions are restricted in the Zuul environment. Also multiple
   roles are available for your use in the `zuul-jobs
   <https://git.openstack.org/cgit/openstack-infra/zuul-jobs/tree/roles>`_
   and `openstack-zuul-jobs
   <https://git.openstack.org/cgit/openstack-infra/openstack-zuul-jobs/tree/roles>`_
   repos.

#. For more detailed information on jobs, playbooks, or any of the
   topics discussed in this quickstart guide, see the complete `Zuul
   v3 documentation
   <https://docs.openstack.org/infra/zuul/feature/zuulv3>`_.
