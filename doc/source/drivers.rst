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

The Openstack Infra team has a tool called GerritBot.
It's an IRC bot that listens to Openstack Gerrit server
for events and notifies those on Freenode's Openstack channels.

GerritBot is able to notify events like creation of patchsets, changes merged, comments added to patchsets and updates to refs. These events can be configured by project,
so you can have different notifications per project on the same channel.

In order to get GerritBot notifications for your Openstack project
IRC channel, you need to add your GerritBot configuration into ``modules/gerritbot/files/gerritbot_channel_config.yaml``.
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

Please note that text among brackets are placeholder values, and you can add 
as many projects and branches as you wish.

Therefore, you just need to add the type of events you want to notify in your
channel and replace your specific values for IRC channel, projects
and branches.

Once you have your change ready, push it for review and whenever it is approved
you should be all set.

Running Jobs with Zuul
======================

