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
Gerrit users can create new branches. For OpenStack projects the Infra
team and the OpenStack Release Managers can create branches. Stackforge
projects can update their Gerrit ACLs to allow their release teams to
create these branches. For similar Gerrit ACL reasons branch deletion
is typically limited to the Infra team. Keep this in mind before
creating many branches that will need cleanup.

One additional thing to keep in mind is that feature branches should be
treated like master in most cases. They are specifically not for sustained
long term development like stable branches.

Merge Commits
-------------

An important activity when using feature branches is syncing to and from
the project's master branch. During development on a feature branch a
project will want to merge master into the feature branch periodically
to keep up to date with changes over time. Then when development on the
feature branch is complete, it will need to be merged into master.

Before this can happen the project's release group will need to have
access to push merge commits in Gerrit::

  [access "refs/for/refs/*"]
  pushMerge = group <project>-release

Should be added to the project's ACL file in the project-config repo.

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
  git merge origin/feature-branch
  # Amend the merge commit to automatically add a Change-ID to the commit message:
  GIT_EDITOR=/bin/true git commit --amend
  git review -R
  git checkout master
  git branch -D merge-branch

Release Management
==================

Milestones
----------

Create milestone-proposed Branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Authoring Changes for milestone-proposed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Submit Changes in master to milestone-proposed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Submit Changes in milestone-proposed to master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tagging a Release
~~~~~~~~~~~~~~~~~

End of Milestone
~~~~~~~~~~~~~~~~

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

