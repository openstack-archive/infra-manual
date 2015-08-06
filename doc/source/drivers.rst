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
proposed change.

To get started with a feature branch you will need to create the new
branch in Gerrit with the 'feature/' prefix. Note that Gerrit ACLs do
not allow for pushing of new branches via git, but specific groups of
Gerrit users can create new branches. For OpenStack repositories the
Release Manager creates feature branches. Stackforge repositories
may update their Gerrit ACLs to allow their release teams to create
these branches. For similar Gerrit ACL reasons branch deletion is
typically limited to the Infra team. Keep this in mind before
creating many branches that will need cleanup.

If more than one repository is involved in a feature development
effort, the same feature branch name should be used across all such
repositories. This will cause integration testing with Zuul to use
the respective feature branch from any repository that carries it.
Repositories without an equivalently named feature branch will use
master instead. Use care not to create a feature branch with the
same name as a feature branch for an unrelated effort in another
repository.

One additional thing to keep in mind is that feature branches should be
treated like master in most cases. They are specifically not for sustained
long term development like stable branches.

Merge Commits
-------------

An important activity when using feature branches is syncing to and from
the repository's master branch. During development on a feature
branch a repository will want to merge master into the feature branch
periodically to keep up to date with changes over time. Then when
development on the feature branch is complete, it will need to be
merged into master.

Before this can happen the project team's release group will need to
have access to push merge commits in Gerrit::

  [access "refs/for/refs/*"]
  pushMerge = group <projectname>-release

Should be added to the repository's ACL file in the project-config
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

Release Branches
----------------

Between RC1 and the final release, there needs to be a separate branch
in Gerrit for release-critical changes destined for the final
release. Meanwhile, development on the master branch should continue
as normal (with the addition that changes proposed for the final
release should also be proposed for master, and some changes for
master may need to be applied to the release branch).

This process creates an ephemeral proposed/<series> (for example,
proposed/juno) branch that is only available in Gerrit during the
final release process. At final release, a tag is applied to the final
commit to record the state of the branch at the time.

Create proposed/* Branch
~~~~~~~~~~~~~~~~~~~~~~~~

For OpenStack repositories this should be performed by the OpenStack
Release Manager at the Release Branch Point. If you are managing
branches for your repository you may have permission to do this
yourself.

* Go to https://review.openstack.org/ and sign in
* Select 'Admin', 'Projects', then the repository
* Select 'Branches'
* Enter ``proposed/<series>`` in the 'Branch Name' field, and ``HEAD``
  as the 'Initial Revision', then press 'Create Branch'.
  Alternatively, you may run ``git branch proposed/<series> <sha> &&
  git push gerrit proposed/<series>``

In your local checkout::

  git checkout master
  git pull
  git checkout proposed/<series>

Authoring Changes for proposed/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. (jeblair) This probably belongs in developer.rst

Create topic branches as normal, but branch them from proposed/\*
rather than master::

  git checkout proposed/<series>
  git pull
  git checkout -b <topic branch>

Changes for proposed/\* should be submitted with::

  git review proposed/<series>

Submit Changes in master to proposed/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. (jeblair) This probably belongs in developer.rst

If a change to master should also be included in proposed/\*, use this
procedure to cherry-pick that change and submit it for review::

  git checkout proposed/<series>
  git pull
  git checkout -b master-to-mp
  git cherry-pick -x <SHA1 or "master">
  git review proposed/<series>
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


Tagging a Release
~~~~~~~~~~~~~~~~~

This step should be performed by the OpenStack Release Manager when
the release is made.  If you are managing your own releases, you may
have permission to do this yourself.

Tag the tip of the appropriate branch (proposed/<series> for server
repositories, master for clients/libraries) with a release tag and
push that tag to Gerrit by running the following commands::

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

  * After a tag is created the release build will get deployed to a
    repository such as PyPI.

End of Release
~~~~~~~~~~~~~~
This step should be performed by the OpenStack Release Manager after
the release is tagged.

When the release process is complete and the released commit is
tagged, remove the ``proposed/<series>`` branch. The tag will persist,
even after the branch is deleted, making it possible to restore the
state of the tree.

* Go to https://review.openstack.org/ and sign in
* Select 'Admin', 'Projects', then the repository
* Select 'Branches'
* Select the checkbox next to 'proposed/<series>' and hit 'Delete'

Targeting Blueprints
====================

Blueprints for a project are generally posted to
https://blueprints.launchpad.net/<projectname>. Project drivers need to review
blueprints regularly and assign them to a target. For each release there are three
milestones. Based on interactions with the proposer and/or assignee of the blueprint,
the project driver assigns the blueprint to a milestone
(release-1, release-2 or release-3) or defers it to a later release.

Many projects have repositories entitled <projectteam>-specs. If a project has a spec
repo, a spec needs to be submitted and linked to the launchpad blueprint. The spec
needs to be reviewed and approved prior to the launchpad blueprint being targeted to
a milestone.

Interactions with release management includes discussions of the blueprint target
page: https://launchpad.net/<projectname>/+milestone/{release name}-{1|2|3} The more
the blueprint target page reflects the reality of progress and intentions, the happier
the release management team.

Gerrit IRC Notifications
========================

The intent of this section is to detail how to set up notifications
about all the repositories that are hosted on OpenStack Gerrit in
the appropriate IRC channels.

GerritBot is an IRC bot that listens to the OpenStack Gerrit server
for events and notifies those on Freenode's OpenStack channels.

GerritBot is able to notify the channel for events like creation of patchsets, changes merged,
comments added to patchsets and updates to refs.
These event notifications can be configured per repository, so the
channel can have multiple notifications per repository.

In order for GerritBot to post notifications on the IRC channel of the
repository you are configuring,
you need to add your GerritBot configuration into
``modules/gerritbot/files/gerritbot_channel_config.yaml``.
This file is hosted in `openstack-infra/config <http://git.openstack.org/cgit/openstack-infra/config/>`_.

The syntax for configuring the notifications is::

  <IRC channel>:
        events:
          - patchset-created
          - change-merged
          - comment-added
          - ref-updated
        projects:
          - <repository name>
        branches:
          - <branch name>

Please note that the text between the angle brackets are placeholder
values. Multiple repositories and branches can be listed in the YAML
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
   a single name that can be reused across repositories.
#. Job specific overrides. This section is where you specify that a
   specific job should not vote or run only against a specific set
   of branches.
#. Projects. This is the section where you will likely spend most of
   your time. Note it is organized into alphabetical subsections based
   on git repo name prefix.

To add a job to a repository you will need to edit your repository
in the projects list or add your repository to the list if it does
not exist. You should end up with something like::

  - name: openstack/<repositoryname>
    template:
      - name: merge-check
    check:
      - gate-new-<repositoryname>-job
    gate:
      - gate-new-<repositoryname>-job

The template section applies the common ``merge-check`` jobs to the
repository (every repository should use this template). Then we have
``gate-new-<repositoryname>-job`` listed in the check and gate
pipelines. This says if an event comes in for
``openstack/<repositoryname>`` that matches the check or gate
pipeline triggers run the ``gate-new-<repositoryname>-job`` job
against ``openstack/<repositoryname>`` in the matching pipeline.

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
      git://git.openstack.org \
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
