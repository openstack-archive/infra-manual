:title: Project Driver's Guide

.. _driver_manual:

Project Driver's Guide
######################

Feature Branches
================

Merge Commits
-------------

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

For OpenStack projects this should be performed by the OpenStack
Release Manager at the Release Branch Point.  If you are managing
branches for your project you may have permission to do this yourself.

* Go to https://review.openstack.org/ and sign in
* Select 'Admin', 'Projects', then the project
* Select 'Branches'
* Enter ``proposed/<series>`` in the 'Branch Name' field, and ``HEAD``
  as the 'Initial Revision', then press 'Create Branch'.
  Alternatively, you may run ``git branch proposed<series> <sha> &&
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

``git cherry-pick`` master will pick the most recent commit from master
to apply, if you want a different patch, use the SHA1 of the commit
instead.

The ``-x`` flag will ensure the commit message records the SHA1 hash of
the original commit in master.

If there are conflicts when cherry-picking, do not delete the
'Conflicts' lines GIT adds to the commit message. These are valuable
to reviewers to identify files which need extra attention.


Tagging a Release
~~~~~~~~~~~~~~~~~

This step should be performed by the OpenStack Release Manager when
the release is made.  If you are managing your own releases, you may
have permission to do this yourself.

Tag the tip of the appropriate branch (proposed/<series> for server
projects, master for clients/libraries) with a release tag and push
that tag to Gerrit by running the following commands::

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
* Select 'Admin', 'Projects', then the project
* Select 'Branches'
* Select the checkbox next to 'proposed/<series>' and hit 'Delete'

Targeting Blueprints
====================

Blueprints for a program or project are posted to
https://blueprints.launchpad.net/<projectname>. Project drivers need to review
blueprints regularly and assign them to a target. For each release there are three
milestones. Based on interactions with the proposer and/or assignee of the blueprint,
the project driver assigns the blueprint to a milestone
(release-1, release-2 or release-3) or defers it to a later release.

Many projects have repositories entitled <project>-specs. If a project has a spec
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
about all the projects that are hosted on OpenStack Gerrit in the appropiate IRC channels.

GerritBot is an IRC bot that listens to the OpenStack Gerrit server
for events and notifies those on Freenode's OpenStack channels.

GerritBot is able to notify the channel for events like creation of patchsets, changes merged,
comments added to patchsets and updates to refs.
These event notifications can be configured per project, so the channel can have multiple
notifications per project.

In order for GerritBot to post notifications on the IRC channel of the
project you are configuring,
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
          - <project name>
        branches:
          - <branch name>

Please note that the text between the angle brackets are placeholder values. Multiple projects and branches can be
listed in the YAML file.

Running Jobs with Zuul
======================

