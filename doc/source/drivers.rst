:title: Project Driver's Guide

.. _driver_manual:

Project Driver's Guide
######################

Feature Branches
================

There are times when prolonged development on specific features is easier
on a feature branch rather than on master. In particular it organizes
work to a location that interested parties can follow. Feature branches
also move merge points to specific points in time rather than at every
proposed change. Learn more about `feature branches in the project team
guide <https://docs.openstack.org/project-team-guide/other-branches.html#feature-branches>`_.

For projects under governance, new feature branches can be requested using
the same mechanism as stable branch creation. Submit a patch to the releases
repository with a new ``feature/feature-name`` branch defined. Set the
location value to the repository and commit hash from which to branch::

    ---
    branches:
      - name: feature/example-feature-work
        location:
          openstack/oslo.config: 02a86d2eefeda5144ea8c39657aed24b8b0c9a39

For more details, refer to the openstack/releases
`README.rst <https://opendev.org/openstack/releases/src/README.rst>`_
file.

For projects not under governance, new branches can be defined via Gerrit.
In the `Gerrit UI <https://review.opendev.org/>`_, under Projects > List,
locate the given project and go to the Branches option. For example::

    https://review.opendev.org/#/admin/projects/openstack/nova,branches

If you do not have the option to add a new branch, you will need to contact
the infra team to get the necessary permissions for the project.

If more than one project is involved in a feature development effort,
the same feature branch name should be used across all involved
projects. This will cause integration testing with Zuul to use the
respective feature branch from any project that carries it.
Projects without an equivalently named feature branch will use
master instead. Use care not to create a feature branch with the same
name as a feature branch for an unrelated effort in another
project.

One additional thing to keep in mind is that feature branches should be
treated like master in most cases. They are specifically not for sustained
long term development like stable branches.

Merge Commits
-------------

An important activity when using feature branches is syncing to and from
the project's master branch. During development on a feature
branch a project will want to merge master into the feature branch
periodically to keep up to date with changes over time. Then when
development on the feature branch is complete, it will need to be
merged into master.

Before this can happen the project team's release group will need to
have access to push merge commits in Gerrit::

  [access "refs/for/refs/*"]
  pushMerge = group <projectname>-release

Should be added to the project's ACL file in the project-config
repo.

Merge Master into Feature Branch
--------------------------------

::

  git remote update
  git checkout feature-branch
  git pull --ff-only origin feature-branch
  git checkout -b merge-branch
  git merge origin/master
  # Amend the merge commit to automatically add a Change-ID to the commit message
  GIT_EDITOR=/bin/true git commit --amend
  git review -R feature-branch
  git checkout master
  git branch -D merge-branch

Merge Feature Branch into Master
--------------------------------

::

  git remote update
  git checkout master
  git pull --ff-only origin master
  git checkout -b merge-branch
  # Force a merge commit by not fast-forwarding, in case master hasn't updated:
  git merge --no-ff origin/feature-branch
  # Amend the merge commit to automatically add a Change-ID to the commit message:
  GIT_EDITOR=/bin/true git commit --amend
  git review -R
  git checkout master
  git branch -D merge-branch

How To Avoid Merging Specific Files
-----------------------------------

Sometimes you may have files on one branch you don't want merged to
or from another. An easy workaround for this is to checkout the file
in question from the target branch and amend your merge commit
before pushing it for review. For example, as in the last section
you've just merged from ``origin/feature-branch`` into your local
``merge-branch`` but want to keep the ``.gitreview`` file from
``master`` because you don't want ``defaultbranch=feature-branch``
added to it. Immediately before you ``git commit --amend`` do::

  git checkout origin/master -- .gitreview

Release Management
==================

This section describes topics related to release management.

.. (jeblair) After the other sections move, this should probably
   mention that actions here require specific permissions, and name
   what they are.

Release and stable branches
---------------------------

Projects following the release:cycle-with-milestones model generate
release candidates before the final release to encourage 3rd-party
testing. The first release candidate (RC1) is cut from the master
branch. You can learn more about `release management in the project
team guide <https://docs.openstack.org/project-team-guide/release-management.html>`_.

Between RC1 and the final release, there needs to be a separate branch
in Gerrit for release-critical changes destined for the final
release. Meanwhile, development on the master branch should continue
as normal (with the addition that changes proposed for the final
release should also be proposed for master, and some changes for
master may need to be applied to the release branch).

In order to avoid tracking different branches pre- and post-release,
this process directly creates a stable/<series> (for example,
stable/mitaka) branch that will be reused as the stable maintenance
branch post-release. Specific ACLs apply to the branch pre-release,
and when the final release is tagged the generic stable branch ACLs
are applied instead.

Create stable/* Branch
~~~~~~~~~~~~~~~~~~~~~~

For OpenStack projects this should be performed by the OpenStack
Release Management Team at the Release Branch Point. If you are managing
branches for your project you may have permission to do this
yourself.

* Go to https://review.opendev.org/ and sign in
* Select 'Admin', 'Projects', then the project
* Select 'Branches'
* Enter ``stable/<series>`` in the 'Branch Name' field, and ``HEAD``
  as the 'Initial Revision', then press 'Create Branch'.
  Alternatively, you may run ``git branch stable/<series> <sha> &&
  git push gerrit stable/<series>``

Once this is done, you should push a change updating the defaultbranch in
.gitreview to match the new name of the branch, so that "git review"
automatically pushes to the right branch::

  defaultbranch=stable/<series>

To check out the new branch in your local checkout, you can use::

  git checkout master
  git pull
  git checkout stable/<series>

Authoring Changes for stable/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. (jeblair) This probably belongs in developer.rst

Create topic branches as normal, but branch them from stable/\*
rather than master::

  git checkout stable/<series>
  git pull
  git checkout -b <topic branch>

Generally the defaultbranch in .gitreview is adjusted on the new branch
so that you can directly use ``git review``. If not, changes for stable/\*
should be submitted with::

  git review stable/<series>

Submit Changes in master to stable/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. (jeblair) This probably belongs in developer.rst

If a change to master should also be included in stable/\*, use this
procedure to cherry-pick that change and submit it for review::

  git checkout stable/<series>
  git pull
  git checkout -b master-to-mp
  git cherry-pick -x <SHA1 or "master">
  git review stable/<series>
  git checkout master
  git branch -D master-to-mp

``git cherry-pick master`` will pick the most recent commit from master
to apply, if you want a different patch, use the SHA1 of the commit
instead.

The ``-x`` flag will ensure the commit message records the SHA1 hash of
the original commit in master.

If there are conflicts when cherry-picking, do not delete the
'Conflicts' lines git adds to the commit message. These are valuable
to reviewers to identify files which need extra attention.

You can learn more about `stable branches in the project team guide
<https://docs.openstack.org/project-team-guide/stable-branches.html>`_.

.. _tagging-a-release:

Tagging a Release
~~~~~~~~~~~~~~~~~

Deliverables produced by official teams and released following the
release cycle should be managed by the OpenStack Release Management
Team. See the instructions in the `README.rst
<http://opendev.org/openstack/releases/src/README.rst>`__
in openstack/releases for details.

If you are managing your own releases, you may have permission to do
this yourself.

Tag the tip of the appropriate branch (stable/<series> for server
projects using release candidates, master for the others) with a release tag
and push that tag to Gerrit by running the following commands::

  git checkout <branch name>
  git pull --ff-only
  git tag -s <version number>
  git push gerrit <version number>

.. note::

  * Pushing the tag will trigger the release pipeline in zuul, but without
    proper configuration no release will happen. A publishing job is required.
    One common way to do this is to use a `publish-to-pypi template
    <https://docs.openstack.org/infra/openstack-zuul-jobs/project-templates.html#project_template-publish-to-pypi>`_
    in `openstack/project-config <https://opendev.org/openstack/project-config/>`_.
    The publishing jobs are one of the :ref:`central-config-exceptions`.

  * Tags can't be effectively deleted once pushed, so make absolutely
    certain they're correct (ideally by locally testing release
    artifact generation commands and inspecting the results between
    the tag and push steps above).

  * Git won't have a remote named gerrit until the first time git-review
    runs. You may need to run ``git review -s`` before the push.

  * The -s option to git tag signs the tag using GnuPG, so it's
    important to ensure that the person making the release has a
    suitable OpenPGP key.

  * Make sure you're only adding a single tag when pushing to
    gerrit, like in the example above.

  * After a tag is created the release build will generate a source code
    tarball and may publish it to a repository such as PyPI.

  * Tags need to follow the format of :pep:`440` which consists for
    final releases of one or more non-negative integer values,
    separated by dots. Be aware that ``pbr`` needs a three component
    version, like ``1.0.0`` or ``1.2.3``.

    If you need to support other version schemes, you might need to
    use the ``tag`` pipeline instead of the default ``release``
    pipeline. Best discuss this with the OpenDev team.

Gerrit IRC Notifications
========================

The intent of this section is to detail how to set up notifications
about all the projects that are hosted on OpenDev Gerrit in the
appropriate IRC channels.

GerritBot is an IRC bot that listens to the OpenDev Gerrit server
for events and notifies those on Freenode's channels.

GerritBot is able to notify the channel for events like creation of
patchsets, changes merged, comments added to patchsets and updates to
refs.  These event notifications can be configured per project, so the
channel can have multiple notifications per project.

Before you can configure GerritBot, you need to give channel permissions with
an accessbot configuration specific to the channel where you want
notifications posted. The configuration file is hosted in
`openstack/project-config
<https://opendev.org/openstack/project-config/>`_. Edit
``accessbot/channels.yaml`` to add your IRC channel if it is not
already listed.

In order for GerritBot to post notifications on the IRC channel of the
project you are configuring, you need to add your GerritBot
configuration into
``gerritbot/channels.yaml``.  This file
is hosted in `openstack/project-config
<https://opendev.org/openstack/project-config/>`_.

The syntax for configuring the notifications is::

  <IRC channel>:
        events:
          - patchset-created
          - change-merged
          - comment-added
          - ref-updated
        projects:
          - <project name>
        branches:
          - <branch name>

Please note that the text between the angle brackets are placeholder
values. Multiple projects and branches can be listed in the YAML
file.

Running Jobs with Zuul
======================

Those looking to write and run jobs with Zuul can refer to Zuul's
`documentation <https://zuul-ci.org/docs/zuul/reference/config.html>`__
in order to get started.

Retiring a Project
==================

If you need to retire a project and no longer accept patches, it is
important to communicate that to both users and contributors.  The
following steps will help you wind down a project gracefully.

.. note::

   The following sections are really separate steps. If your project
   has jobs set up and is an official project, you need to submit
   *four* different changes as explained below. We recommend to link
   these changes with "Depends-On:" and "Needed-By:" headers.

Prerequirement: Announce Retirement
-----------------------------------

Use mailing lists or other channels to announce to users and
contributors that the project is being retired.  Be sure to include a
date upon which maintenance will end, if that date is in the future.

Step 1: Stop requirements syncing (if set up)
---------------------------------------------

Submit a review to the ``openstack/requirements`` project removing the
project from ``projects.txt``.  This needs to happen for stable
branches as well.

Step 2: End Project Gating
--------------------------

Check out a copy of the ``openstack/project-config`` repository
and edit ``zuul.d/projects.yaml``.  Find the section for your project and
change it to look like this::

  - project:
    name: <namespace>/<projectname>
    templates:
      - noop-jobs

Also, remove any jobs and templates you have defined. These can be
defined in ``openstack/project-config`` repository in the
directory  ``zuul.d``, or in ``openstack/openstack-zuul-jobs``
repository or in your own repository.

Submit that change and make sure to mention in the commit message that
you are ending project gating for the purposes of retiring the
project.  Wait for that change to merge and then proceed.

Step 3: Remove Project Content
------------------------------

Once Zuul is no longer running tests on your project, prepare a change
that removes all of the files from your project except the README.
Double check that all dot files (such as ``.gitignore`` and
``.testr.conf``) **except** ``.gitreview`` are also removed.

.. note::

   Removing the ``.gitreview`` file from the master branch of a
   repository breaks much of the OpenStack release tools, so it will
   be harder to continue to tag releases on existing stable branches.
   Take care to remove all files other than ``README.rst`` and
   ``.gitreview``.

Replace the contents of the README with a message such as this::

  This project is no longer maintained.

  The contents of this repository are still available in the Git
  source code management system.  To see the contents of this
  repository before it reached its end of life, please check out the
  previous commit with "git checkout HEAD^1".

  (Optional:)
  For an alternative project, please see <alternative project name> at
  <alternative project URL>.

  For any further questions, please email
  openstack-discuss@lists.openstack.org or join #openstack-dev on
  Freenode.

Merge this commit to your project.

If any users missed the announcement that the project is being
retired, removing the content of the repository will cause any users
who continuously deploy the software as well as users who track
changes to the repository to notice the retirement.  While this may be
disruptive, it is generally considered better than continuing to
deploy unmaintained software.  Potential contributors who may not have
otherwise read the README will in this case, as it is the only file in
the repository.

Step 4: Remove Project from Infrastructure Systems
--------------------------------------------------

Once your repository is in its final state, prepare a second change to
the ``openstack/project-config`` repository that does the
following:

* Remove your project from ``zuul.d/projects.yaml`` and
  ``zuul/main.yaml``.

* By default, project ACLs are defined in a file called
  ``gerrit/acls/<namespace>/<projectname>.config``. If this file exists,
  remove it.

* Now adjust the project configuration and use the shared read-only
  ACLs. Find the entry for your project in ``gerrit/projects.yaml`` and
  look for the line which defines the acl-config, update or add it
  so that it contents is::

     acl-config: /home/gerrit2/acls/openstack/retired.config

  Also prefix the project description with ``RETIRED,``::

     description: RETIRED, existing  project description

* Remove your project from ``gerritbot/channels.yaml``.

.. note::

   If there is a need to unretire a project, most steps here can be done in
   reverse. This step has some caveats to be aware of when going in reverse.

   With the removal of ACLs from the Gerrit project, the project gets marked as
   read-only. Adding those ACLs back to the configuration files does not switch
   it back to read-write. Manual intervention will be required from the infra
   team to restore the project status back to "Active" in Gerrit before ACLs
   can be reapplied successfully.

Step 5: Remove Repository from the Governance Repository
--------------------------------------------------------

If this was an official OpenStack project, remove it from the
``reference/projects.yaml`` file and add it to the file
``reference/legacy.yaml`` in the ``openstack/governance`` repository.
Note that if the project was recently active, this may have
implications for automatic detection of ATCs.

Package Requirements
====================

The OpenDev infrastructure sets up nodes for testing that contain
a minimal system and a number of convenience distribution packages.

If you want to add additional packages, you have several options.

If you run Python tests using ``tox``, you can install them using
``requirements.txt`` and ``test-requirements.txt`` files (for
OpenStack projects, see also the
`global requirements process <https://docs.openstack.org/requirements/>`_).
If these Python tests need additional distribution packages installed as well
and if those are not in the nodes used for testing, they have to be installed
explicitly.

If you are building documentation, the file ``doc/requirements.txt``
is used instead to install Python packages.

If you run devstack based tests, then list missing binary packages
below the `files
<https://opendev.org/openstack/devstack/src/files>`_
directory of devstack.

For non-devstack based tests, add a ``bindep.txt`` file
containing listing the required distribution packages. It is a
cross-platform list of all dependencies needed for running tests. The
`bindep <https://docs.openstack.org/infra/bindep/>`_ utility will be
used to install the right dependencies per distribution when running
in the OpenDev infrastructure.

If you use bindep, create a bindep tox environment as well:

.. code-block:: ini

   [testenv:bindep]
   # Do not install any requirements. We want this to be fast and work even if
   # system dependencies are missing, since it's used to tell you what system
   # dependencies are missing! This also means that bindep must be installed
   # separately, outside of the requirements files.
   deps = bindep
   commands = bindep test

This way a developer can just run bindep to get a list of missing
packages for their own system:

.. code-block:: console

   $ tox -e bindep

The output of this can then be fed into the distribution package
manager like ``apt-get``, ``dnf``, ``yum``, or ``zypper`` to install
missing binary packages.

The OpenDev infrastructure will install packages marked for a
`profile
<https://docs.openstack.org/infra/bindep/readme.html#profiles>`__ named
"test" along with any packages belonging to the default profile of the
``bindep.txt`` file. Add any build time requirements and any
requirements specific to the test jobs to the "test" profile, add any
requirements specific to documentation building to the "doc" profile, add
requirements for test, runtime, and documentation to the base profile::

   # A runtime dependency
   libffi6
   # A build time dependency
   libffi-devel [test]
   # A documentation dependency
   graphviz [doc]

Submodules
----------

The use of git submodules is not supported.  The tools that we use do
not all work correctly with submodules and we have found that
submodules can be very confusing even for experienced developers.  If
your project depends on another project, please express that as an
external dependency on a released package (i.e., through
requirements.txt, bindep.txt, or similar mechanism).

Unit Test Set up
================

Projects might need special set up for unit tests which can be done
via the script ``tools/test-setup.sh`` that needs to reside in the
repository.

Python unit tests are tests like ``coverage``, ``python27``,
``python35``, and ``pypy`` which are run using python's ``tox``
package as well as tests using the template
``openstack-tox-{envlist}`` or ``tox-{envlist}``. For these tests, the
script ``tools/test-setup.sh`` is run if it exists in the repository and is
executable after package installation. The script has ``sudo`` access
and can set up the test environment as needed. For example, it should
be used to set up the ``openstack_citest`` databases for testing.

.. _v3_naming:

Consistent Naming for Zuul Jobs
===============================

This document describes a consistent naming scheme for Zuul jobs.
The goal is to give job developer and reviewers of jobs a common
document as reference. This is particularly important because
all jobs within a Zuul tenant share a common global namespace.
Adhering to these guidelines avoids collisions between jobs defined
in various repositories within a Zuul tenant.

.. warning:: This is a living document, it may get updates as our
             use of Zuul changes over time.

Job Naming Scheme
-----------------

* The general pattern is
  ``{prefix-}MAINPURPOSE-DETAILS{-}{node}``.

* Jobs in specific pipelines have no special prefix, there's no need
  to use ``gate-`` or ``periodic`` as it was done with Zuul v2.

* There is in general no need to give the name of the repository as
  part of the job as it was done with Zuul v2, *unless*
  the job is defined in a specific repo.

* Publishing jobs, like documentation or tarball uploads, have a
  prefix of ``publish`` like ``publish-tarball`` and
  ``publish-sphinx-docs``.

  These jobs are normally run in a post pipeline.

* Jobs that build an artifact without uploading  ``build`` like
  ``build-sphinx-docs``.

* Jobs have the optional suffixes ``{node}`` which is used when a test
  should be run on different platforms like on CentOS, Fedora,
  openSUSE, or Ubuntu - or on different versions of these. For jobs
  that are only run on one platform, the suffix ``{node}`` should be
  avoided. The suffix ``{node}`` is the name for the node the job runs
  on. If this is a a multi-node job, it's the name of the underlying
  single node.

* Use consistent names like "integration", "functional", "rally",
  "tempest", "grenade", "devstack" (what do we need? Those should be
  explained) as ``MAINPURPOSE``.

* Components of job names are separated by ``-``.

* Do not use "." for versions, just cat them together like ``35`` for
  Python 3.5.

* Since Zuul allows overriding of job and definition of jobs, care
  should be taken not to use the same name for different jobs:

  * If you override a generic Zuul job for project specific usage
    prefix it with ``PROJECT-``. For example, OpenStack creates versions
    of generic jobs intended to be used globally within OpenStack and
    prefixes them with ``openstack-``.
  * If you define a job in a specific repo, the name of the job should
    use the repository name as ``prefix`` or as first part of it.

Examples of job names using these rules:

* tox-py27 or openstack-py27
* tox-py35 or openstack-py35
* grenade-neutron-forward
* neutron-api (or neutron-api-ubuntu-xenial if multiple OSes need to be tested)
* tempest-neutron-full-ssh
* build-sphinx-docs
* publish-sphinx-docs

Outbound Third-Party Testing
============================

Many organizations generously donate cloud computing resources to
OpenDev for use by its testing and automation system so that
we can maintain and improve the quality of the hosted software.  We are
stewards of these resources and strive to use them wisely and
responsibly.

These resources are available to perform integration testing with
Open-Source projects which are direct dependencies or direct
downstream consumers of hosted projects.  If you want to
set up an integration test with a non-hosted project that meets
these criteria, follow the instructions below.

Currently, Zuul is able to report on changes proposed to Gerrit
systems or GitHub.  If the project you want to test with isn't hosted
on a Gerrit or GitHub, contact the infrastructure team in
#openstack-infra to discuss options.

In all cases, before starting this process, be sure you have discussed
this with the team responsible for the project you want to test.  You
should get their approval to report test results on changes or
pull-requests.

Hosted on an External Gerrit
----------------------------

If the project you wish to test is hosted on a Gerrit system (other
than OpenDev's Gerrit), you may need to connect Zuul to it first, if
it isn't already.  To do so, propose a change to `system-config
<https://opendev.org/opendev/system-config/src/hiera/group/zuul-scheduler.yaml>`_
which adds the connection information for the new server, then work
with the infra team in #openstack-infra to set up an account.

Once this is complete, propose a change to add the project(s) to
OpenDev's Zuul.  Add them to `project-config/zuul/main.yaml
<https://opendev.org/openstack/project-config/src/zuul/main.yaml>`_
under the connection name established above.

The project should not be configured to load any configuration objects
(i.e., it should have an ``include: []`` stanza associated with it).

Hosted on GitHub
----------------

If the project you wish to test is hosted on GitHub, ask the team
managing the project to install the "OpenStack Zuul" App into the
project (or organization if multiple projects are involved).

Visit the `OpenDev Zuul App
<https://github.com/apps/opendev-zuul>`_ page on GitHub and click
the `Install` button to install the app.

Once this is complete, propose a change to add the project(s) to
OpenDev's Zuul.  Add them to `project-config/zuul/main.yaml
<https://opendev.org/openstack/project-config/src/zuul/main.yaml>`_
under the ``github:`` connection.

The project should not be configured to load any configuration objects
(i.e., it should have an ``include: []`` stanza associated with it).

Add to Pipelines
----------------

Once Zuul is configured to know about the project, it can be added to
pipelines just like any other project in Zuul.  However, external
projects should only be added to the ``third-party-check`` pipeline.
Because we are not loading any in-tree configuration from these
projects, this needs to be done in the `project-config` repo.  Define
the jobs you wish to run either in your own repos, or in
`openstack-zuul-jobs`.  Then create project definitions for the new
projects in `project-config/zuul.d/projects.yaml
<https://opendev.org/openstack/project-config/src/zuul.d/projects.yaml>`_
which adds those jobs to the new project on the `third-party-check`
pipeline.
