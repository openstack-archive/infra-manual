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
about all the projects that are hosted on OpenStack Gerrit in the
appropriate IRC channels.

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

