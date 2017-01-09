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
guide <http://docs.openstack.org/project-team-guide/other-branches.html#feature-branches>`_.

To get started with a feature branch you will need to create the new
branch in Gerrit with the 'feature/' prefix. Note that Gerrit ACLs do
not allow for pushing of new branches via git, but specific groups of
Gerrit users can create new branches. For official OpenStack projects
the Release Manager creates feature branches. Unofficial projects may
update their Gerrit ACLs to allow their release teams to create these
branches. For similar Gerrit ACL reasons branch deletion is typically
limited to the Infra team. Keep this in mind before creating many
branches that will need cleanup.

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
team guide <http://docs.openstack.org/project-team-guide/release-management.html>`_.

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

* Go to https://review.openstack.org/ and sign in
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
<http://docs.openstack.org/project-team-guide/stable-branches.html>`_.

Tagging a Release
~~~~~~~~~~~~~~~~~

This step should be performed by the OpenStack Release Management Team
when the release is made. If you are managing your own releases, you may
have permission to do this yourself.

Tag the tip of the appropriate branch (stable/<series> for server
projects using release candidates, master for the others) with a release tag
and push that tag to Gerrit by running the following commands::

  git checkout <branch name>
  git pull --ff-only
  git tag -s <version number>
  git push gerrit <version number>

.. note::

  * Git won't have a remote named gerrit until the first time git-review
    runs. You may need to run ``git review -s`` before the push.

  * The -s option to git tag signs the tag using GnuPG, so it's
    important to ensure that the person making the release has a
    suitable OpenPGP key.

  * Make sure you're only adding a single tag when pushing to
    gerrit, like in the example above.

  * After a tag is created the release build will generate a source code
    tarball and may publish it to a repository such as PyPI.

  * Tags need to follow the format of `PEP 440
    <https://www.python.org/dev/peps/pep-0440/>` which consists for
    final releases of one or more non-negative integer values,
    separated by dots. Be aware that ``pbr`` needs a three component
    version, like ``1.0.0`` or ``1.2.3``.

    If you need to support other version schemes, you might need to
    use the ``tag`` pipeline instead of the default ``release``
    pipeline. Best discuss this with the OpenStack Infra team.

Gerrit IRC Notifications
========================

The intent of this section is to detail how to set up notifications
about all the projects that are hosted on OpenStack Gerrit in the
appropriate IRC channels.

GerritBot is an IRC bot that listens to the OpenStack Gerrit server
for events and notifies those on Freenode's OpenStack channels.

GerritBot is able to notify the channel for events like creation of
patchsets, changes merged, comments added to patchsets and updates to
refs.  These event notifications can be configured per project, so the
channel can have multiple notifications per project.

Before you can configure GerritBot, you need to give channel permissions with
an accessbot configuration specific to the channel where you want
notifications posted. The configuration file is hosted in
`openstack-infra/project-config
<http://git.openstack.org/cgit/openstack-infra/project-config/>`_. Edit
``accessbot/channels.yaml`` to add your IRC channel if it is not
already listed.

In order for GerritBot to post notifications on the IRC channel of the
project you are configuring, you need to add your GerritBot
configuration into
``gerritbot/channels.yaml``.  This file
is hosted in `openstack-infra/project-config
<http://git.openstack.org/cgit/openstack-infra/project-config/>`_.

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

There are two major components in getting jobs running under Zuul. First
you must ensure that the job you want to run is defined in the `JJB
config <https://git.openstack.org/cgit/openstack-infra/project-config/tree/jenkins/jobs>`_.
The `JJB documentation <http://docs.openstack.org/infra/jenkins-job-builder/>`_
is extensive as are the examples in our JJB config so we will not cover
that here.

The second thing you need to do is update `Zuul's layout file
<https://git.openstack.org/cgit/openstack-infra/project-config/tree/zuul/layout.yaml>`_
instructing Zuul to run your job when appropriate. This file is organized
into several sections.

#. Zuul python includes. You can largely ignore this section as it
   declares arbitrary python functions loaded into Zuul and is managed
   by the Infra team.
#. Pipelines. You should not need to add or modify any of these
   pipelines but they provide information on why each pipeline exists
   and when it is triggered. This section is good as a reference.
#. Project templates. Useful if you want to collect several jobs under
   a single name that can be reused across projects.
#. Job specific overrides. This section is where you specify that a
   specific job should not vote or run only against a specific set
   of branches.
#. Projects. This is the section where you will likely spend most of
   your time. Note it is organized into alphabetical subsections based
   on git repo name prefix.

To add a job to a project you will need to edit your project in the
projects list or add your project to the list if it does not
exist. You should end up with something like::

  - name: openstack/<projectname>
    template:
      - name: merge-check
    check:
      - gate-new-<projectname>-job
    gate:
      - gate-new-<projectname>-job

The template section applies the common ``merge-check`` jobs to the
project (every project should use this template). Then we have
``gate-new-<projectname>-job`` listed in the check and gate
pipelines. This says if an event comes in for
``openstack/<projectname>`` that matches the check or gate pipeline
triggers run the ``gate-new-<projectname>-job`` job against
``openstack/<projectname>`` in the matching pipeline.

Integration Tests
-----------------

One of Zuul's most powerful features is the ability to perform complex
integration testing across interrelated repositories.  Projects that
share one or more jobs are combined into a shared change queue.  That
means that as changes are approved, they are sequenced in order and
can be tested together.  It also means that if a change specifies that
it depends on another change with a "Depends-On:" header, those
changes can be tested together and merged in rapid succession.

In order to use this to its full advantage, your job should allow Zuul
to perform all of the git operations for all of the projects related
to the integration test.  If you install the software under test from
the git checkouts supplied by Zuul, the test run will include all of
the changes that will be merged ahead of the change under test.

To do this, use the ``zuul-cloner`` command as follows::

  sudo -E /usr/zuul-env/bin/zuul-cloner --cache-dir /opt/git \
      https://git.openstack.org \
      openstack/project1 \
      openstack/project2 \
      openstack/projectN

Where the final arguments are the names of all of the projects
involved in the integration test.  They will be checked out into the
current directory (e.g., ``./openstack/project1``).  If you need them
to be placed in a different location, see the ``clonemap`` feature of
``zuul-cloner`` which allows for very flexible (including regular
expressions) directory layout descriptions.

Use that command in a single Jenkins Job Builder definition that you
then invoke from all of the related projects.  This way they all run
the same job (which tests the entire system) and Zuul knows to combine
those projects into a shared change queue.

Zuul comes with extensive `documentation <http://docs.openstack.org/infra/zuul/>`_
too and should be referenced for more information.

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

Step 1: End Project Gating
--------------------------

Check out a copy of the ``openstack-infra/project-config`` repository
and edit ``zuul/layout.yaml``.  Find the section for your project and
change it to look like this::

  - name: openstack/<projectname>
    template:
      - name: merge-check
      - name: noop-jobs

Also, remove your project from ``jenkins/jobs/projects.yaml``, and if
you have created any other jobs specific for your project in
``jenkins/jobs/``, remove them as well.

Submit that change and make sure to mention in the commit message that
you are ending project gating for the purposes of retiring the
project.  Wait for that change to merge and then proceed.

Step 2: Remove Project Content
------------------------------

Once Zuul is no longer running tests on your project, prepare a change
that removes all of the files from your project except the README.
Double check that all dot files (such as ``.gitignore``, ``.testr.conf``,
and ``.gitreview``) are also removed.

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
  openstack-dev@lists.openstack.org or join #openstack-dev on
  Freenode.

Merge this commit to your project.

.. note::

  Before removing ``.gitreview`` be sure to run ``git review -s``,  this
  will record the necessary information about the repository.

If any users missed the announcement that the project is being
retired, removing the content of the repository will cause any users
who continuously deploy the software as well as users who track
changes to the repository to notice the retirement.  While this may be
disruptive, it is generally considered better than continuing to
deploy unmaintained software.  Potential contributors who may not have
otherwise read the README will in this case, as it is the only file in
the repository.

Step 3: Remove Project from Infrastructure Systems
--------------------------------------------------

Once your repository is in its final state, prepare a second change to
the ``openstack-infra/project-config`` repository that does the
following:

* Remove your project from ``zuul/layout.yaml``.

* By default, project ACLs are defined in a file called
  ``gerrit/acls/openstack/<projectname>.config``. If this file exists,
  replace the contents with::

    [project]
    state = read only

* If a file called ``gerrit/acls/openstack/<projectname>.config`` does
  not exist, that implies that your project shared ACLs with some other
  project(s). You will need to do two things in that case:

  #. Find the entry for your project in ``gerrit/projects.yaml`` and
     delete the line which defines the acl-config. This will cause the
     default to be used, and that default is a file that you create
     next.

  #. Create and submit a new file called
     ``gerrit/acls/openstack/<projectname>.config`` which contains the
     text::

       [project]
       state = read only

* Remove your project from ``gerritbot/channels.yaml``.

Step 4: Remove Repository from the Governance Repository
--------------------------------------------------------

If this was an official OpenStack project, remove it from the
``reference/projects.yaml`` file and add it to the file
``reference/legacy.yaml`` in the ``openstack/governance`` repository.
Note that if the project was recently active, this may have
implications for automatic detection of ATCs.

Package Requirements
====================

The OpenStack CI infrastructure sets up nodes for testing that contain
a minimal system and a number of convenience distribution packages.

If you want to add additional packages, you have several options.

If you run Python tests using ``tox``, you can install them using
``requirements.txt`` and ``test-requirements.txt`` files (see also the
`global requirements process
<http://docs.openstack.org/developer/requirements/>`_). If these
Python tests need additional distribution packages installed as well
and if those are not in the nodes used for testing, they have to be
installed explicitly.

If you run devstack based tests, then list missing binary packages
below the `files
<http://git.openstack.org/cgit/openstack-dev/devstack/tree/files>`_
directory of devstack.

For non-devstack based tests, add a ``bindep.txt`` file
containing listing the required distribution packages. It is a
cross-platform list of all dependencies needed for running tests. The
`bindep <http://docs.openstack.org/infra/bindep/>`_ utility will be
used to install the right dependencies per distribution when running
in the OpenStack CI infrastructure.

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

The OpenStack CI infrastructure will install packages marked for a
`profile
<http://docs.openstack.org/infra/bindep/readme.html#profiles>`__ named
"test" along with any packages belonging to the default profile of the
``bindep.txt`` file. Add any build time requirements and any
requirements specific to the test jobs to the "test" profile, add
requirements for both test and runtime to the base profile::

   # A runtime dependency
   libffi6
   # A build time dependency
   libffi-devel [test]
