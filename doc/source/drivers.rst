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

Running Jobs with Zuul
======================

