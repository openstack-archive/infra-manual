:title: Zuul v3 Migration Guide

Zuul v3 Migration Guide
#######################

This is a temporary section of the Infra Manual to assist in the
conversion to Zuul v3.  Some of the content herein will only be
relevant before and shortly after we move from Zuul v2 to v3.

What is Zuul v3?
================

.. sidebar:: Quick Links

   * `Zuul v3 manual <https://zuul-ci.org/docs/zuul/>`__
   * `zuul-jobs  <https://zuul-ci.org/docs/zuul-jobs/>`__
   * `openstack-zuul-jobs <https://docs.openstack.org/infra/openstack-zuul-jobs/>`__

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
the development process for all OpenStack developers.  But we also know
that not everyone needs to know everything about Zuul v3 in order for
this to work.  The sections below provide increasing amounts of
information about Zuul v3.  Please at least read the first section,
and then continue reading as long as subsequent sections remain
relevant to the way you work.

.. _Zuul v3 spec: https://docs.opendev.org/opendev/infra-specs/latest/specs/zuulv3.html

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

All existing jobs will be migrated automatically
------------------------------------------------

Jobs covered by the Consistent Testing Interface will all be
migrated automatically to newly written v3 native jobs and you should
not need to do anything special.

The rest of the jobs will be migrated to new auto-generated jobs. As the
content of these is auto-generated from JJB template transformation, these
jobs will need post-migration attention.

If you have custom jobs for your project, you or someone from your project
should keep reading this document, and see :ref:`legacy-job-migration-details`.

Web-based log streaming
-----------------------

Zuul v3 restores a feature lost in Zuul v2.5: web-based console log
streaming.  If you click on the name of a running job on the status
page, a live stream of the job's console log will appear and
automatically update.  It is also possible to access streaming logs
from the terminal using a ``finger`` client (so you may watch a job's
progress from the terminal, or pipe it through ``grep``), though the
command to do so is not yet incorporated into the status page; expect
that to be added soon.

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
<https://zuul-ci.org/docs/zuul/user/config.html#job>`_
for more information on how jobs are configured.

Where Jobs Are Defined in Zuul v3
---------------------------------

Zuul v3 loads its configuration directly from git repos.  This lets
us accomplish a number of things we have long desired: instantaneous
reconfiguration and in-repo configuration.

Zuul starts by loading the configuration in the `project-config zuul.d`_
directory in the `project-config`_ repository.
This contains all of the pipeline definitions and some very basic job
definitions.  Zuul looks for its configuration in files named
``zuul.yaml`` or ``.zuul.yaml``, or in directories named ``zuul.d`` or
``.zuul.d``.  Then it loads configuration from the `zuul-jobs zuul.yaml`_
file in the `zuul-jobs`_ repository. This
repository contains job definitions intended to be used by any Zuul
installation, including, but not limited to, OpenStack's Zuul.  Then
it loads jobs from the `openstack-zuul-jobs zuul.d`_ directory in the
`openstack-zuul-jobs`_ repository which is where we keep most of
the OpenStack-specific jobs.  Finally,
it loads jobs defined in all of the repositories in the system.  This
means that any repo can define its own jobs.  And in most cases,
changes to those jobs will be self-testing, as Zuul will dynamically
change its configuration in response to proposed changes.

This is very powerful, but there are some limitations.  See the
sections of the Zuul User Guide about `Security Contexts
<https://zuul-ci.org/docs/zuul/user/config.html#security-contexts>`_
and `Configuration Loading
<https://zuul-ci.org/docs/zuul/user/config.html#configuration-loading>`_
for more details.

Note that all OpenStack projects share a single namespace for job
names, so we have established some guidelines detailed in
:ref:`v3_naming` for how to name jobs.  Adhere to these so that we may
avoid collisions between jobs defined in various repositories.

Zuul jobs are documented in their own repositories.  Here are links to
the documentation for the repositories mentioned above:

* `zuul-jobs documentation`_
* `openstack-zuul-jobs documentation`_

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
   <https://zuul-ci.org/docs/zuul/user/config.html#job>`_

Job definitions may appear more than once in the Zuul configuration.
We call these multiple definitions *variants*.  Job definitions have
several fields, such as ``branches`` and ``files``, which act as
*matchers* to determine whether the job is applicable to a change.
When Zuul runs a job, it builds up a new job definition with all of
the matching variants applied.  Later variants can override settings
on earlier definitions, but any settings not overridden will be
present as well.

For example, consider this simple job definition for a job named
``fedstack``:

.. code-block:: yaml

   - job:
       name: fedstack
       nodeset: fedora-26
       vars:
         neutron: true

This may then be supplemented with a job variant:

.. code-block:: yaml

   - job:
       name: fedstack
       branches: stable/pike
       nodeset: fedora-25

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
will run the job described in the first definition above.  A change on
the stable/pike branch will combine *both* variants and use the new
merged definition when running the job.

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

As long as at least one variant matches a change, the job will run; a
variant can't be used to "undo" an earlier matching variant.

One final note about variants: in some cases Zuul attaches an implied
branch matcher to job definitions.  The rules are `tricky
<https://zuul-ci.org/docs/zuul/user/config.html#attr-job.branches>`_,
but in general, jobs defined in a multi-branch project get an implied
branch matcher of their current branch.  This makes it so that we can
branch a project from master along with all of its job definitions,
and jobs will continue to work as expected.

I Write Jobs, How Does Zuul v3 Actually Work?
=============================================

We previously covered some things you need to know if you simply want
already-existing jobs to be run on your project.  If you want to
create or alter the behavior of jobs, you'll want to read this
section.  Zuul v3 has a number of facilities to promote code re-use,
so as a job author, your work may range in complexity from a simple
variable tweak, to stacking some existing roles together, and on to
creating new Ansible roles.

Job Inheritance
---------------

We discussed job variance earlier -- it's a method for making small
changes to jobs in specific contexts, such as on a certain branch or a
certain project.  That allows us to avoid creating many nearly
identical jobs just to handle such situations.  Another method of job
reuse is inheritance.  Just as in object-oriented programming,
inheritance in Zuul allows us to build on an existing job.

.. sidebar:: Further reading

   Base jobs and inheritance are discussed in more detail in the
   `Job section of the Zuul manual
   <https://zuul-ci.org/docs/zuul/user/config.html#job>`_

Every job in Zuul has a parent, except for jobs which we call *base
jobs*.  A base job is intended to handle fundamental tasks like
setting up git repositories and archiving logs.  You probably won't be
creating base jobs; we expect to have very few of them, and they can
only be created in the ``project-config`` repository.  Instead, all
other jobs inherit from, at the very least, one of the base jobs.

A job in Zuul has three execution phases: pre-run, run, and post-run.
Each of these correspond to an Ansible playbook, but we'll discuss
that in more detail later.  The main action of the job -- the part
that is intended to succeed or fail based on the content of the change
-- happens in the run phase.  Actions which should always succeed,
such as preparing the environment or collecting results, happen in the
pre-run and post-run phases respectively.  These have a special
behavior when inheritance comes into play: child jobs "nest" inside of
parent jobs.  Take for example a job named ``tox-py27`` which inherits
from ``tox`` which inherits from ``unittests`` which inherits from
``base`` (this example is not contrived -- this is actually how the
``tox-py27`` job is implemented).  The pre- and post-run execution
phases from all of those jobs come in to play; however, only the run
phase of the terminal job is executed.  The sequence, indented for
visual clarity, looks like this:

.. sidebar:: Inheritance vs. Roles

   This isn't the only way we could have made this job.  Each of these
   playbooks uses Ansible roles to do the bulk of the work, so we
   could have flattened it so that tox-py27 inherited directly from
   base, and then used those roles in a single playbook.  In this
   case, we chose inheritance to make it easy for folks to create
   minor variations on unit test jobs that handle a wide range of
   situations.

::

   base pre-run
     unittests pre-run
       tox pre-run
         tox-py27 pre-run
         tox-py27 run
         tox-py27 post-run
       tox post-run
     unittests post-run
   base post-run

The base pre- and post-run playbooks handle setting up repositories
and archiving logs.  The unittests pre- and post-run playbooks run
bindep and collect testr output.  The tox pre- and post-run playbooks
install tox and collect tox debugging logs.  Finally, the tox-py27 run
playbook actually runs tox.

A Simple Shell Job
------------------

Zuul v3 uses Ansible to run jobs, and that gives us a lot of power and
flexibility, especially in constructing multi-node jobs.  But it can
also get out of the way if all you want to do is run a shell script.

See :ref:`howto_in_repo` below for a walkthrough describing how to set
up a simple shell-based job.

Ansible Playbooks
-----------------

Every job runs several playbooks in succession.  At the very least, it
will run the pre-run playbook from the base job, the playbook for the
job itself, and the post-run playbook from the base job.  Most jobs
will run even more.

In Zuul v2 with jenkins-job-builder, we often combined the job content
-- that is, the executable code -- with the job description, putting
large shell snippets inside the JJB yaml, or including them into the
yaml, or, if scripts got especially large, writing a small amount of
shell in JJB to run a larger script found elsewhere.

In Zuul v3, the job content should always be separate from the job
description.  Rather than embedding shell scripts into Zuul yaml
configuration, the content takes the form of Ansible playbooks (which
might perform all of the job actions, or they might delegate to a
shell script).  Either way, a given job's playbook is always located
in the same repository as the job definition.  That means a job
defined in ``project-config`` will find its playbook in
``project-config`` as well.  And a job defined in an OpenStack project
repo will find its playbook in the project repo.

A job with pre- or post-run playbooks must specify the path to those
playbooks explicitly.  The path is relative to the root of the
repository.  For example:

.. code-block:: yaml

   - job:
       name: test-job
       pre-run: playbooks/test-job-pre.yaml
       post-run: playbooks/test-job-post.yaml

However, the main playbook for the job may either be explicitly
specified (with the ``run:`` attribute) or if that is omitted, an
implied value of ``playbooks/<jobname>`` is used.  In the above
example, Zuul would look for the main playbook in
``playbooks/test-job.yaml``.

Ansible Roles
-------------

Roles are the main unit of code reuse in Ansible.  We're building a
significant library of useful roles in the ``zuul-jobs``,
``openstack-zuul-jobs``, and ``project-config`` projects.  In many
cases, these roles correspond to jenkins-job-builder macros that we
used in Zuul v2.  That allows us to build up playbooks using lists of
roles in the same way that we built jobs from list of builder macros
in Zuul v2.

Ansible roles must be installed in the environment where Ansible is
run.  That means a role used by a Zuul job must be installed *before*
the job starts running.  Zuul has special support for roles to
accomodate this.  A job may use the ``roles:`` attribute to specify
that another project in the system must be installed because that job
uses roles that are defined there.  For instance, if your job uses a
role from ``zuul-jobs``, you should add the following to your job
configuration:

.. code-block:: yaml

   - job:
       name: test-job
       roles:
         - zuul: zuul/zuul-jobs

The project where the job is defined is always added as an implicit
source for roles.

.. note::

   If a project implements a *single* role, Zuul expects the root of
   that project to be the root of the role (i.e., the project root
   directory should have a ``tasks/`` subdirectory or similar).  If
   the project contains more than one role, the roles should be
   located in subdirectories of the ``roles/`` directory (e.g.,
   ``roles/myrole/tasks/``).

Ansible Variables
-----------------

In Zuul v2, a number of variables with information about Zuul and the
change being tested were available as environment variables, generally
prefixed with ``ZUUL_``.  In Zuul v3, these have been replaced with
Ansible variables which provide much more information as well as much
richer structured data.  See the `Job Content
<https://zuul-ci.org/docs/zuul/user/jobs.html>`_
section of the Zuul User Guide for a full list.

Secret Variables
----------------

.. sidebar:: Further reading

   See the `Encryption section
   <https://zuul-ci.org/docs/zuul/user/encryption.html>`_
   of the Zuul User Guide for more information on encryption and secrets

A new feature in Zuul v3 is the ability to provide secrets which can be
used to perform tasks with jobs run in post and release pipelines, like
authenticating a job to a remote service or generating cryptographic
signatures automatically. These secrets are asymmetrically encrypted for
inclusion in job definitions using per-project public keys served from a
Zuul API, and are presented in their decrypted form as Ansible variables
the jobs can use.

.. note::

   Credentials and similar secrets encrypted for the per-project keys
   Zuul uses cannot be decrypted except by Zuul and (by extension) the
   root sysadmins operating the Zuul service and maintaining the job
   nodes where those secrets are utilized. By policy, these sysadmins
   will not deliberately decrypt secrets or access decrypted secrets,
   aside from non-production test vectors used to ensure the feature is
   working correctly. They will not under any circumstances be able to
   provide decrypted copies of your project's secrets on request, and so
   you cannot consider the encrypted copy as a backup but should instead
   find ways to safely maintain (and if necessary share) your own backup
   copies if you're unable to easily revoke/replace them when lost.


If you want to encrypt a secret, you can use the
``tools/encrypt_secret.py`` script from project
``zuul/zuul``. For example, to encrypt file
``file_with_secret`` for project ``openstack/kolla`` use:

.. code-block:: shell

   $ tools/encrypt_secret.py --infile file_with_secret \
     --tenant openstack https://zuul.openstack.org openstack/kolla


Periodic Jobs
-------------

In Zuul v3 periodic jobs are just like regular jobs. So instead of
putting ``periodic-foo-master`` and ``periodic-foo-pike`` on a
project, you just put ``foo`` in the periodic pipeline. Zuul will then
emit trigger events for every project-branch combination.

So if you add a periodic job to a project it will run on all of that
project's branches. If you only want it to run on a subset of
branches, just use branch matchers in the project-pipeline in the
regular way.

The following will run ``tox-py35`` on all branches in the project:

.. code-block:: yaml

      - project:
        name: openstack/<projectname>
        periodic:
          jobs:
            - tox-py35

This example runs ``tox-py35`` only on ``master`` and
``stable/queens`` branches:

.. code-block:: yaml

      - project:
        name: openstack/<projectname>
        periodic:
          jobs:
            - tox-py35:
                branches:
                  - master
                  - stable/queens

Changes to OpenStack tox jobs
=============================

One of the most common job types in OpenStack are tox-based tests. With the
Zuul v3 rollout there are new and shiny versions of the tox jobs.

There are a few important things to know about them.

tox vs. tox-py27 vs. vs. openstack-tox vs. openstack-tox-py27
-------------------------------------------------------------

There is a base ``tox`` job and a set of jobs like ``tox-py27`` and
``tox-py35``. There is also a base ``openstack-tox`` job and a set of jobs like
``openstack-tox-py27``, ``openstack-tox-py35``.

The ``tox`` base job is what it sounds like - it's a base job. It knows how to
run tox and fetch logs and results. It has parameters you can set to control its
behavior, see the `description in zuul-jobs
<https://zuul-ci.org/docs/zuul-jobs/jobs.html#job-tox>`__ for details.

``tox-py27`` is a job that uses the ``tox`` base job and sets ``tox_envlist``
to ``py27``. We've made jobs for each of the common tox environments.

Those are jobs that just run tox. As Zuul v3 is designed to have directly
shareable job definitions that can be used across Zuul deployments, these jobs
do not contain OpenStack specific logic. OpenStack projects should not use
them, but non-OpenStack projects using OpenStack's Zuul may want to.

``openstack-tox`` is a base job that builds on the ``tox`` base job and adds
behaviors specific to OpenStack. Specifically, it adds
``openstack/requirements`` to the ``required-projects`` list and sets the
``tox_constraints_file`` variable to point to
``src/opendev.org/openstack/requirements/upper-constraints.txt``.

``openstack-tox-py27`` is like ``tox-py27`` but uses ``openstack-tox`` as a
base job.

OpenStack projects with custom tox environments should base them on
``openstack-tox``, not ``tox``:

.. code-block:: yaml

    - job:
        name: tooz-tox-py35-etcd3
        parent: openstack-tox
        vars:
          tox_envlist: py35-etcd3

Installation of 'sibling' requirements
--------------------------------------

One of Zuul's strengths is doing multi-repo testing. We obviously all use
the heck out of that for integration tests, but for tox things it has
historically been a bit harder to manage.

In Zuul v3, we've added functionality to the base ``tox`` job that will look
to see if there are other git repos in the ``required-projects`` list. If there
are, it will look at the virtualenv that tox creates, get the list of installed
packages, see if any of the git repos present provides that package, and if so
will update the virtualenv with an installation of that project from its git
repository.

Long story short, if you wanted to make a job for awesome-project that did
tox-level testing against patches to keystoneauth, you'd do this:

.. code-block:: yaml

    - job:
        name: awesome-project-tox-py27-keystoneauth
        parent: openstack-tox-py27
        required-projects:
          - openstack/keystoneauth

Then put that job into your project pipelines. If you do that, that job will
inject master of keystoneauth (or a speculative master state if there are any
Depends-On lines involved) into tox's py27 virtualenv before running tests.

If you want to disable this behavior, it's controlled by a variable
``tox_install_siblings``.

.. _howto_in_repo:

HOWTO: Add an in-repo job
=========================

This is a simple guide that shows how to add a Zuul v3 job to your
OpenStack project.

#. Create a ``.zuul.yaml`` file in your project. This is where you will configure
   your project and define its jobs.

#. In your ``.zuul.yaml``, define your project. You will need to define
   which pipelines will run jobs, and the names of the jobs
   to run in each pipeline. Below is an example project which adds two jobs to
   the ``check`` pipeline:

   .. code-block:: yaml

      - project:
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
   ``tox-pep8``, and ``tox-docs`` are defined in the `zuul-jobs zuul.yaml`_
   file.

   The predefined OpenStack-specific jobs, such as
   ``openstack-doc-build`` and ``tox-py35-constraints``
   are defined in the
   `openstack-zuul-jobs jobs.yaml` file.

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
              chdir: "{{ zuul.project.src_dir }}"

   This playbook will execute on our host named ``ubuntu-xenial``,
   which we get for free from the Zuul base job. If you need more
   nodes, or a node of a different type, you will need to define these
   in your ``.zuul.yaml`` file.

   Note that some playbook actions are restricted in the Zuul
   environment. Also multiple roles are available for your use in the
   `zuul-jobs roles`_ and `openstack-zuul-jobs roles`_ directories.

#. For more detailed information on jobs, playbooks, or any of the
   topics discussed in this guide, see the complete `Zuul v3 documentation`_.

.. _legacy-job-migration-details:

Legacy Job Migration Details
============================

Project-specific jobs are migrated to jobs prefixed with ``legacy-``.
This makes them easy to spot as jobs that were not written for v3 but
instead were auto-converted.

With in-repo config, the best place for most of these jobs is actually in
the project repositories themselves so that the project cores are the ones
who review the jobs and not the Infra team. Moving the jobs from their
migrated location to the project will be a good opportunity to clean them
up and rewrite them to use the new Zuul v3 features.

Migrated Job Locations
----------------------

Automigrated jobs have their job definitions in `openstack-zuul-jobs`_ in the
files `zuul.d/zuul-legacy-jobs.yaml`_, project templates in
`zuul.d/zuul-legacy-project-templates.yaml`_ and the playbooks containing the
job content itself in `playbooks/legacy`_.

The ``project-pipeline`` definitions for automigrated jobs are in
`project-config`_ in the `zuul.d/projects.yaml`_ file.

Migrated Job Naming
-------------------

Jobs which correspond to newly-written v3 jobs were mapping to the appropriate
new v3 job.

If an old job did not yet have a corresponding v3 job, the following rules
apply for the name of the new auto-generated job:

* project names are removed from jobs
* the ``gate-`` prefix is removed, if one exists
* the ``legacy-`` prefix is added
* the string ``ubuntu-xenial`` is removed from the name if it exists
* the ``-nv`` suffix used to indicate non-voting jobs is removed and the
  job is marked as non-voting directly

Migrated Job and Project Matchers
---------------------------------

In v2 there was a huge section of regexes at the top of the layout file that
filtered when a job was run. In v3, that content has been moved to matchers
and variants on the jobs themselves. In some cases this means that jobs
defined in a project-template for a project have to be expanded and applied
to the project individually so that the appropriate matchers and variants
can be applied. As jobs are reworked from converted legacy jobs to new and
shiny v3 native jobs, some of these matches can be added to the job definition
rather than at the project-pipeline definition and can be re-added to
project-templates.

HOWTO: Update Legacy Jobs
=========================

All of the auto-converted jobs prefixed with ``legacy-`` should be replaced.
They are using old interfaces and not making good use of the new system.

Some of the ``legacy-`` jobs are legitimate central shared jobs we just
haven't gotten around to making new central versions of. Don't worry about
those. (``releasenotes`` and ``api-ref`` jobs are good examples here)

For all of the jobs specific to a particular project, teams should move the
auto-converted ``legacy-`` jobs to their own repos and rework them to stop
using the legacy interfaces. There are two fundamental steps:

#. Move the jobs to your repo

#. Rework the jobs to be native v3 jobs

Both are discussed below.

Moving Legacy Jobs to Projects
------------------------------

At your earliest convenience, for every job specific to your project:

#. Copy the job definition into your ``.zuul.yaml`` file in your repo. You must
   rename the job as part of the step. Replacing the ``legacy-`` prefix with
   your project name is a good way to ensure jobs don't conflict.

#. Add the new jobs to your project pipeline definition in your ``.zuul.yaml``
   file. This will cause both the new and old ``legacy-`` copies to run.

#. Submit patches to `project-config`_ and `openstack-zuul-jobs`_ with
   Depends-On and Needed-By pointing to each other so that reviewers can
   verify both patches. The `openstack-zuul-jobs`_ patch should Depends-On the
   `project-config`_ patch. Specifically, these patches should contain:

   * A patch to `project-config`_ to remove the legacy jobs from your project's
     pipeline definition in ``zuul.d/projects.yaml`` which is Needed-By the
     next patch. (See `what_not_to_convert`_ for information about which jobs
     should stay.)

   * A patch to `openstack-zuul-jobs`_ removing the jobs from
     ``zuul.d/zuul-legacy-jobs.yaml`` and their corresponding playbooks from
     ``playbooks/legacy``. It should Depends-On the `project-config`_ patch.

   The `openstack-zuul-jobs`_ patch will give a config error because the
   `project-config`_ patch removing use of the jobs hasn't landed. That's ok.
   We'll recheck it once the `project-config`_ patch lands.

Stable Branches
~~~~~~~~~~~~~~~

If your project has stable branches, you should also add a
``.zuul.yaml`` file (with job and project definitions -- just as on
master) and any playbooks to each stable branch.  Zuul will
automatically add branch matchers for the current branch to any jobs
defined on a multi-branch project.  Jobs defined in a stable branch
will therefore only apply to changes on the stable branch, and
likewise master.  Backporting these changes is a little more work now
during the transition from Zuul v2 to v3, but when we make the next
stable branch from master, no extra would should be required -- the
new branch will already contain all the right content, and
configuration on both the master and stable branches will be able to
diverge naturally.

Reworking Legacy Jobs to be v3 Native
-------------------------------------

Once the jobs are under your control you should rework them to no longer use
a base job prefixed with ``legacy-`` or any of the legacy v2 interfaces.

See if you can just replace them with something existing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We didn't try to auto-convert non-standard tox jobs to use the `openstack-tox`_
base job as there was too much unknown for us to do it automatically. For you,
just switching to using that's likely the **easiest** thing to do.

For instance, the job ``legacy-tooz-tox-py35-etcd3`` can just become:

.. code-block:: yaml

   - job:
       name: tooz-tox-py35-etcd3
       parent: openstack-tox
       vars:
         tox_envlist: py35-etcd3

and you can just delete ``playbooks/legacy/tooz-tox-py35-etcd3/``.

Converting Custom dsvm jobs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your job is a custom dsvm job - try to migrate it to use the new
``devstack`` or ``devstack-tempest`` base jobs.

.. note:: There may be a couple of edge cases they can't handle yet.

You can see https://review.opendev.org/#/c/500365/ for an example of just
about everything you might want to do using the new devstack base job.

Converting Other Legacy Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If those don't apply, this will mean the following changes:

* Add the repos you need to the job's ``required-projects`` list. This will
  make sure that zuul clones what you need into ``src/``.

* Stop using zuul-cloner. The repos are on disk in ``src/``. Just reference
  them.

* Stop using ``ZUUL_`` env vars, the ``/etc/nodepool`` directory, and the
  ``WORKSPACE`` and ``BUILD_TIMEOUT`` environment variables. Zuul and nodepool
  info is available in the zuul and nodepool ansible vars. Timeout information
  is in ``zuul.timeout``. WORKSPACE isn't really a thing in v3. Tasks all start
  in ``/home/zuul``, and the source code for the project that triggered the
  change is in ``src/{{ zuul.project.canonical_name }}``.

  We added a ``mkdir /home/zuul/workspace`` to each generated playbook, but
  that's not really a thing, it's just for transition and is not needed in new
  jobs.

* Remove ``environment: '{{ zuul | zuul_legacy_vars }}'`` from tasks once they
  don't need the legacy environment variables.

* Rework log collection. The synchronize commands in the generated
  ``post.yaml`` are very non-ideal.

* Stop using nodesets prefixed with ``legacy-``. Each of them should have an
  equivalent non-legacy nodeset.

.. _what_not_to_convert:

What to Convert?
~~~~~~~~~~~~~~~~

Some jobs should not be migrated and should always stay in `project-config`_.
Refer to :ref:`central-config-exceptions` for up to date info on which jobs
should remain in centralized config.

Outside of these jobs, most jobs can be migrated to a project repository. If a
job is used by a single project then migration is simple: you should move the
job to that project's repository. If a job is used by multiple projects then
things get a little trickier. In this scenario, you should move the job to the
project that is mostly testing and where the developers are best placed to
maintain the job. For example, a job that validates interaction between nova
and os-vif might be run for both of these projects. However, the job is mostly
focused on os-vif and it's likely that os-vif developers would be best placed
to resolve issues that may arise. As a result, the job should live in os-vif.
More information is provided below.

Where Should Jobs And Templates Live?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have a global namespace for jobs and project-templates, you can
easily define a job or a template in one project and use it in others.
Thus, do not blindly convert jobs but consider how to group and use
them. Some recommendations and examples:

* Some projects like devstack, tempest, and rally, should define a
  common set of jobs that others can reuse directly or via
  inheritance.

* If your project consists of a server and a client project where you
  have common tests, define one place for these common tests. We
  recommend to use the server project for this.

* The puppet team is defining a common set of jobs and templates in
  ``openstack/puppet-openstack-integration``.

* The requirements team has the ``check-requirements`` job in the
  ``openstack/requirements`` project so that other projects can use
  it.

* The documentation team defines common jobs and templates in
  ``openstack/openstack-manuals`` projects and other projects like
  ``openstack/security-guide`` reuse these easily.

Options for Restricting When Jobs are Triggered
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zuul v3 allows to specify when jobs are triggered to run based on
changed files. You can define for a job either a list of
``irrelevant-files`` or a list of ``files``. Do not use both together.

See the `Zuul User Guide
<https://zuul-ci.org/docs/zuul/user/config.html#job>`_
for more information on how jobs are configured.

.. _Project Testing Interface: https://governance.openstack.org/tc/reference/project-testing-interface.html
.. _Zuul v3 documentation: https://zuul-ci.org/docs/zuul/
.. _openstack-zuul-jobs documentation: https://docs.openstack.org/infra/openstack-zuul-jobs/
.. _openstack-zuul-jobs jobs.yaml: https://opendev.org/openstack/openstack-zuul-jobs/src/zuul.d/jobs.yaml
.. _openstack-zuul-jobs roles: https://opendev.org/openstack/openstack-zuul-jobs/src/roles
.. _openstack-zuul-jobs zuul.d: https://opendev.org/openstack/openstack-zuul-jobs/src/zuul.d
.. _openstack-zuul-jobs: https://opendev.org/openstack/openstack-zuul-jobs
.. _openstack-tox: https://docs.openstack.org/infra/openstack-zuul-jobs/jobs.html#job-openstack-tox
.. _playbooks/legacy: https://opendev.org/openstack/openstack-zuul-jobs/src/playbooks/legacy
.. _project-config zuul.d: https://opendev.org/openstack/project-config/src/zuul.d
.. _project-config: https://opendev.org/openstack/project-config
.. _zuul-jobs documentation: https://zuul-ci.org/docs/zuul-jobs/
.. _zuul-jobs roles: https://opendev.org/zuul/zuul-jobs/src/roles
.. _zuul-jobs zuul.yaml: https://opendev.org/zuul/zuul-jobs/src/zuul.yaml
.. _zuul-jobs: https://opendev.org/zuul/zuul-jobs
.. _zuul.d/zuul-legacy-jobs.yaml: https://opendev.org/openstack/openstack-zuul-jobs/src/zuul.d/zuul-legacy-jobs.yaml
.. _zuul.d/zuul-legacy-project-templates.yaml: https://opendev.org/openstack/openstack-zuul-jobs/src/zuul.d/zuul-legacy-project-templates.yaml
.. _zuul.d/projects.yaml: https://opendev.org/openstack/project-config/src/zuul.d/projects.yaml
