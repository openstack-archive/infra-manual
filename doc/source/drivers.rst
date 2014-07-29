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

