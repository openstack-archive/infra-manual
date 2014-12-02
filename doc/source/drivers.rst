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

There are two major components in getting jobs running under Zuul. First
you must ensure that the job you want to run is defined in the `JJB
config <https://git.openstack.org/cgit/openstack-infra/project-config/tree/jenkins/jobs>`_.
The `JJB documentation <http://ci.openstack.org/jenkins-job-builder/>`_
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
   pipelines but they provide info on what each pipeline exists for
   and when it is triggered. This section is good as a reference.
#. Project templates. Useful if you want to collect several jobs under
   a single name that can be reused across projects.
#. Job specific overrides. This section is where you specify that a
   specific job should not vote or run only against a specific set
   of branches.
#. Projects. This is the section you will likely spend most of your
   time in. Note it is organized into alphabetical subsections based
   on git repo name prefix.

To add a job to a project you will need to edit your project in the
projects list or add your project to the list if it does not exist.
You should end up with something like::

  - name: openstack/<project>
    template:
      - name: merge-check
    check:
      - gate-new-<project>-job
    gate:
      - gate-new-<project>-job

The template section applies the common ``merge-check`` jobs to the
project (every project should use this template). Then we have
``gate-new-<project>-job`` listed in the check and gate pipelines. This
says if an event comes in for ``openstack/<project`` that matches the
check or gate pipeline triggers run the ``gate-new-<project>-job``
job against ``openstack/<project>`` in the matching pipeline.

Zuul comes with extensive `documentation <http://ci.openstack.org/zuul/>`_
too and should be referred to for more info.
