:title: Project Creator's Guide

========================
 Project Creator's Guide
========================

Before You Start
================

This is a long document. It's long because it has to be, not because
we want it to be. If you follow it, everything will be fine.

It is important that you perform all of the steps, in the order they
are given here. Don't skip any steps. Don't try to do things in
parallel. Don't jump around.

If your project is already set up in the OpenDev infrastructure,
you might want to see :ref:`zuul_best_practices` for information on
adding new tests to a repository.

Decide Status and Namespace of your Project
===========================================

OpenDev is used by different projects which often use different
namespaces. Some of these namespaces have special policies.

If your project does not fit into one of the existing namespaces, you
may create a new one, or use the catch-all ``x`` namespace if you
cannot decide.

For OpenStack and thus the ``openstack`` namespace, the policies are:

* Official OpenStack projects are those that have applied for this
  status with the technical committee. The `governance site`_ contains
  details on how to become one and the list of current `OpenStack
  Project Teams`_. The `Project Team Guide`_ explains how OpenStack
  project teams work.

* If you add a new repository, you can make it part of an existing
  official OpenStack project, use it to start a new official project, or
  start as a `related project`_ (formerly known as *StackForge*).

* Note that only official OpenStack projects may use certain parts of
  the OpenStack infrastructure, especially the docs.openstack.org and
  specs.openstack.org server.

.. _governance site: https://governance.openstack.org
.. _OpenStack Project Teams: https://governance.openstack.org/tc/reference/projects/index.html
.. _Project Team Guide: https://docs.openstack.org/project-team-guide/
.. _related project: https://docs.openstack.org/infra/system-config/unofficial_project_hosting.html

Choosing a Good Name for Your Project
=====================================

It is important to choose a descriptive name that does not conflict
with other projects. There are several places you'll need to look to
ensure uniqueness and suitability of the name.

.. note::

   If you encounter any issues establishing a valid unique name across
   all of the tools we use, consult with the Release Manager before
   going any further.

Character Set
-------------

We prefer to use names made up of lower case ASCII letters and the
``-`` punctuation symbol to avoid issues with various installation
tools.

git repository
--------------

The base name of the repository should be unique across all of the
namespace directories for git repositories under
https://opendev.org/explore/repos.  That is, it is not sufficient to have
``openstack/foo`` and ``openstack-dev/foo`` because that prevents us
from moving those two repositories into the same namespace at some
point.

PyPI
----

Python packages need to have a unique name on the Python Package
Index (https://pypi.org) so we can publish source
distributions to be installed via pip.

It is best to name the repository and the top level Python package
the same when possible so that the name used to install the dist and
the name used to import the package in source files match. Try
"python-" as a prefix if necessary (for example,
"python-stevedore").

Project Team Rules
------------------

Some hosted project teams have naming conventions that must be
followed. For example, the OpenStack Oslo team has `instructions for
choosing a name`_ for new Oslo libraries.

.. _instructions for choosing a name: https://wiki.openstack.org/wiki/Oslo/CreatingANewLibrary#Choosing_a_Name

.. _register-pypi:

Give OpenDev Permission to Publish Releases
===========================================

New Python packages without any releases need to be manually
registered on PyPI.

If you do not have PyPI credentials, you should create them at
https://pypi.org/account/register/ as they are
required for the next step.

Once you have PyPI credentials see
https://packaging.python.org/tutorials/packaging-projects/
to create and upload your initial package. The initial package should
contain a ``PKG-INFO`` file for a nonexistent version ``0`` of your
package (that way any release you make is guaranteed to be higher).
It can be as simple as a plain text file containing the following
two lines (where ``packagename`` is replaced by the desired package
name)::

  Name: packagename
  Version: 0

Next your package needs to be updated so the "openstackci" user has
"Owner" permissions.

Visit
``https://pypi.org/manage/project/<projectname>/collaboration/``
and add "openstackci" in the "User Name" field, set the role to "Owner",
and click "Add Role".

.. image:: images/pypi-role-maintenance.png
   :height: 476
   :width: 800

Adding the Project to the CI System
===================================

To add a project to the CI System, you need to modify some
infrastructure configuration files using git and the OpenDev gerrit
review server.

Note that you need two changes to set up your new project
for testing with OpenDev CI systems.

* First change to create the git repository, configure ACLs, and add
  the git repository to the OpenDev CI system, see
  :ref:`add_project_to_master_projects_list` and following sections.

  For official OpenStack projects, this change should also link via
  ``Needed-By`` to a change for the ``openstack/governance``
  repository to add the new repository under the project team, see
  :ref:`add-to-governance-repo`.

  This change is for ``openstack/project-config`` repository.

* Second change to add jobs to your project, see
  :ref:`add_jobs_for_project`. This one can only pass Zuul internal
  testing once the first change is merged, the repository gets
  created and Zuul reloads its configuration.

.. _add_project_to_master_projects_list:

Add the project to the master projects list
-------------------------------------------

#. Edit ``gerrit/projects.yaml`` to add a new section like:

   .. code-block:: yaml

     - project: <namespace>/<projectname>
       description: Latest and greatest cloud stuff.
       use-storyboard: true

   The ``use-storyboard: true`` is added so that repos will be automatically
   created as projects in `StoryBoard <https://docs.openstack.org/infra/storyboard/>`_
   (community tool for managing work being done in your project and tracking tasks).

#. Provide a very brief description of the project.

#. If you have an existing repository that you want to import (for
   example, when bringing a repository
   into gerrit from github), set the "upstream" field to the URL of
   the publicly reachable repository and also read the information
   in :ref:`setup_review`:

   .. code-block:: yaml

     - project: <namespace>/<projectname>
       description: Latest and greatest cloud stuff.
       upstream: https://github.com/awesumsauce/<projectname>.git

   .. note::

      If you do not configure the upstream source here and get the project
      imported at project creation time you will have to push existing
      history into Gerrit and "review" then approve it or push some squashed
      set of history and "review" then approve that. If you need to preserve
      history the best option is to configure the upstream properly for
      Gerrit project creation. **If you have a lot of history to import,
      please use the upstream field instead of creating a repository and then
      pushing the patches one at a time. Pushing a large number of related patches
      all at one time causes the CI infrastructure to slow down, which impacts
      work on all of the other projects using it.**

   .. note::

      The groups list is used by Storyboard to be able to present grouped
      views of projects, stories, and tasks across multiple related repositories.

      Example:

      .. code-block:: yaml

        - project: <namespace>/<projectname>
          description: Latest and greatest cloud stuff.
          use-storyboard: true
          upstream: https://github.com/awesumsauce/<projectname>.git
          groups:
             - oslo

Viewing & Using Your Project's Task Tracker
-------------------------------------------

After the project-config change above has merged, all repositories will be created in
Storyboard and you will be able to interact with them- filing bugs and adding requests
for new features in the `webclient <https://storyboard.openstack.org/>`_. All
repositories will be added to the group that was associated with the repositories in
the project-config change.

.. _add-gerrit-permissions:

Add Gerrit permissions
----------------------

Each project should have a gerrit group "<projectname>-core",
containing the normal core group, with permission to
+2 changes.

For official OpenStack projects, release management is handled by the Release
Management team through the ``openstack/releases`` repository, the
default settings allow the "``Release Managers``" team to push tags
and create branches.

For all other projects, a second "<projectname>-release" team should
be created and populated with a small group of the primary maintainers
with permission to push tags to trigger releases.

Create a ``gerrit/acls/openstack/<projectname>.config`` as
explained in the following sections.

.. note::

   If the git repository you are creating is using the same gerrit
   permissions - including core groups - as another repository, do
   not copy the configuration file, instead reference it.

   To do this make an additional change to the
   ``gerrit/projects.yaml`` file as shown here:

   .. code-block:: yaml

     - project: <namespace>/<projectname>
       description: Latest and greatest cloud stuff.
       acl-config: /home/gerrit2/acls/openstack/other-project.config


Minimal ACL file
~~~~~~~~~~~~~~~~

The minimal ACL file allows working only on master and requires a
change-ID for each change:

.. code-block:: ini

  [access "refs/heads/*"]
  abandon = group <projectname>-core
  label-Code-Review = -2..+2 group <projectname>-core
  label-Workflow = -1..+1 group <projectname>-core

  [receive]
  requireChangeId = true

  [submit]
  mergeContent = true

Request Signing of ICLA
~~~~~~~~~~~~~~~~~~~~~~~

If your project requires signing of the Individual Contributor
License Agreement (`ICLA
<https://review.opendev.org/static/cla.html>`_), change the
``receive`` section to:

.. code-block:: ini

  [receive]
  requireChangeId = true
  requireContributorAgreement = true

Note that this is mandatory for all official OpenStack projects and
should also be set for projects that want to become official.

Creation of Tags
~~~~~~~~~~~~~~~~

If your project is not handled by the OpenStack release team, you can
allow the project-specific release team to create tags by adding a new
section containing:

.. code-block:: ini

  [access "refs/tags/*"]
  pushSignedTag = group <projectname>-release

Note the ACL file enforces strict alphabetical ordering of sections,
so ``access`` sections like heads and tags must go in order and before
the ``receive`` section.

Deletion of Tags
~~~~~~~~~~~~~~~~

Tags should be created with care and treated as if they cannot be deleted.

While deletion of tags can be done at the source and replicated to the git
mirrors, deletion of tags is not propagated to existing git pulls of the repo.
This means anyone who has done a remote update, including systems in the
OpenStack infrastructure which fire on tags, will have that tag indefinitely.

Creation of Branches
~~~~~~~~~~~~~~~~~~~~

For projects not handled by the Openstack release team, to allow
creation of branches to the project release
team, add a ``create`` rule to it the ``refs/heads/*`` section:

.. code-block:: ini

  [access "refs/heads/*"]
  abandon = group <projectname>-core
  create = group <projectname>-release
  label-Code-Review = -2..+2 group <projectname>-core
  label-Workflow = -1..+1 group <projectname>-core

Deletion of Branches
~~~~~~~~~~~~~~~~~~~~

Members of a team that can create branches do not have access to delete
branches. Instead, someone on the OpenDev team with gerrit administrator
privileges will need to complete this request.

Stable Maintenance Team
~~~~~~~~~~~~~~~~~~~~~~~

If your team has a separate team to review stable branches, add a
``refs/heads/stable/*`` section:

.. code-block:: ini

  [access "refs/heads/stable/*"]
  abandon = group Change Owner
  abandon = group Project Bootstrappers
  abandon = group <projectname>-stable-maint
  exclusiveGroupPermissions = abandon label-Code-Review label-Workflow
  label-Code-Review = -2..+2 group Project Bootstrappers
  label-Code-Review = -2..+2 group <project-name>-stable-maint
  label-Code-Review = -1..+1 group Registered Users
  label-Workflow = -1..+0 group Change Owner
  label-Workflow = -1..+1 group Project Bootstrappers
  label-Workflow = -1..+1 group <project-name>-stable-maint

The ``exclusiveGroupPermissions`` avoids the inheritance from
``refs/heads/*`` and the default setup. The other lines grant the
privileges to the stable team and add back the default privileges for
owners of a change, gerrit administrators, and all users.

Voting Third-Party CI
~~~~~~~~~~~~~~~~~~~~~

To allow some third-party CI systems to vote Verify +1 or -1 on
proposed changes for your project, add a ``label-Verified`` rule to
the ``refs/heads/*`` section:

.. code-block:: ini

  [access "refs/heads/*"]
  abandon = group <projectname>-core
  label-Code-Review = -2..+2 group <projectname>-core
  label-Verified = -1..+1 group <projectname>-ci
  label-Workflow = -1..+1 group <projectname>-core

Optionally, if you only want them to be able to Verify +1 you can
adjust the vote range to ``0..+1`` instead.

Once the project is created it is strongly recommended you go to the
*General* settings for the ``<projectname>-ci`` group in Gerrit's
WebUI and switch the *Owners* field to your ``<projectname>-core``
group (or ``<projectname>-release`` if you have one) so that it is
no longer self-managed, allowing your project team to control the
membership without needing to be members of the group themselves.

Extended ACL File
~~~~~~~~~~~~~~~~~

So, if your official project requires the ICLA signed and allow voting
third-party CI systems, create a
``gerrit/acls/<namespace>/<projectname>.config`` like:

.. code-block:: ini

  [access "refs/heads/*"]
  abandon = group <projectname>-core
  label-Code-Review = -2..+2 group <projectname>-core
  label-Verified = -1..+1 group <projectname>-ci
  label-Workflow = -1..+1 group <projectname>-core

  [receive]
  requireChangeId = true
  requireContributorAgreement = true

  [submit]
  mergeContent = true

If your project does not require the ICLA signed, has a release
team that will create tags and branches, and allow voting third-party
CI systems, create a ``gerrit/acls/<namespace>/<projectname>.config``
like:

.. code-block:: ini

  [access "refs/heads/*"]
  abandon = group <projectname>-core
  create = group <projectname>-release
  label-Code-Review = -2..+2 group <projectname>-core
  label-Verified = -1..+1 group <projectname>-ci
  label-Workflow = -1..+1 group <projectname>-core

  [access "refs/tags/*"]
  pushSignedTag = group <projectname>-release

  [receive]
  requireChangeId = true

  [submit]
  mergeContent = true

See other files in the same directory for further examples.

Create an IRC Channel for Realtime Collaboration
------------------------------------------------

This step is not required, but if you're considering adding a new IRC
channel, see the `IRC services
<https://docs.openstack.org/infra/system-config/irc.html>`_
documentation.

Configure GerritBot to Announce Changes
---------------------------------------

If you want changes proposed and merged to your project to be
announced on IRC, edit ``gerritbot/channels.yaml`` to add your new
project to the list of projects. For example, to announce
changes related to an OpenStack Oslo library in the ``#openstack-oslo``
channel, add it to the ``openstack-oslo`` section:

.. code-block:: yaml

   openstack-oslo:
     events:
       - patchset-created
     projects:
       - openstack/cliff
       - openstack/cookiecutter
       - openstack/hacking
       - openstack/oslo-cookiecutter
       - openstack/oslo-incubator
       - openstack/oslo-specs
       - openstack/oslo.config
       - openstack/oslo.messaging
       - openstack/oslo.rootwrap
       - openstack/oslo.test
       - openstack/oslo.version
       - openstack/oslo.vmware
       - openstack/oslosphinx
       - openstack/pbr
       - openstack/stevedore
       - openstack/taskflow
     branches:
       - master

.. _basic_zuul_jobs:

Add Project to Zuul
-------------------

Test jobs are run by Zuul. For information on how to configure your
repositories to run Zuul jobs you can refer to the Zuul `documentation
<https://zuul-ci.org/docs/zuul/reference/config.html>`__.

Edit ``zuul/main.yaml`` and add your project in alphabetical order to the
``untrusted-projects`` section in the ``openstack`` tenant after the
comment that reads::

  # After this point, sorting projects alphabetically will help
  # merge conflicts

Submitting Infra Change for Review
----------------------------------

At this point, you should submit all the additions discussed so far as a
single change to gerrit.

When submitting the change to ``openstack/project-config`` for
review, use the "new-project" topic so it receives the appropriate
attention:

.. code-block:: console

     $ git review -t new-project

Hold onto the Change-Id for this patch.  You will need to include
it in the commit message when you :ref:`add-to-governance-repo`
later.

.. _add_jobs_for_project:

Add Jobs for your Project
-------------------------

Every project needs at least one test job or patches will not be able to land.

You can add jobs in either your new project's ``.zuul.yaml`` file or
in file the ``zuul.d/projects.yaml`` in the central repository
``openstack/project-config``. This *must* be a separate change from the
one you created earlier to add your entry in ``zuul/main.yaml``, since
these additions will fail with Zuul syntax errors until that merges.

Official OpenStack projects should implement the OpenStack wide jobs
mentioned in the `Project Testing Interface`_ (PTI) document. For more
information on adding additional jobs into your project, see
:ref:`in-repo-zuul-jobs`.

For adding jobs to your project's ``.zuul.yaml`` file, your very first
change to merge after the repository is created or imported needs to
add this file and add jobs for both check and gate pipelines. The file
should not pre-exist in the imported repository. A minimal file that
runs no tests includes only the ``noop-jobs`` template:

.. code-block:: yaml

   - project:
       templates:
         - noop-jobs

In the past we asked that official OpenStack projects manage the PTI job
config in the central projects.yaml file. This incurs review overhead
that Zuul v3 was specifically designed to push onto projects themselves.
In an effort to take advantage of this functionality we now ask that
projects manage the PTI job config in repo.

Shared Queues for Cross-Project Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When your projects are closely coupled together, you want to make sure
changes entering the gate are going to be tested with the version of
other projects currently enqueued in the gate (since they will
eventually be merged and might introduce breaking features).

For such `cross-project testing
<https://zuul-ci.org/docs/zuul/user/gating.html#cross-project-testing>`_
you need to put projects in a comon queue. The queue configuration for
the ``integrated`` queue needs to stay in the central config
repository since this is cross-teams. If only projects of your team
are coupled, you can place this in-repo as well::

   - project:
     gate:
       queue: <queuename>

.. _central-config-exceptions:

Central Config Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~

There are several notable exceptions for job configs that should remain
in the central config repository ``openstack/project-config``:

* Translation jobs for all branches, note that only OpenStack official
  projects are translated.
* Jobs that should only run against the master branch of the project
  they are applied to.

  Examples for templates that include jobs that run only against the
  master branch are ``api-ref-jobs`` and various periodic jobs like
  ``periodic-jobs-with-oslo-master``.

* Jobs that are not "branch aware". Typically these are jobs that are
  triggered by tag based events.

  As an example, the project-templates ``publish-to-pypi`` - and its
  variants -, ``release-openstack-server``,
  ``publish-xstatic-to-pypi``, ``nodejs4-publish-to-npm``,
  ``puppet-release-jobs``, ``docs-on-readthedocs``
  include jobs that are not "branch aware"
  since they are triggered by tag based events.

* The queue configuration for the ``integrated`` queue needs to stay
  in the central config repository.

.. _add-to-governance-repo:

Add New Repository to the Governance Repository
-----------------------------------------------

If your project is not intended to be an official OpenStack project,
you may skip this step.

Each repository managed by an official OpenStack project team needs
to be listed in ``reference/projects.yaml`` in the
``openstack/governance`` repository to indicate who owns the
repository so we know where ATCs voting rights extend.

Find the appropriate section in ``reference/projects.yaml`` and add
the new repository to the list. For example, to add a new Oslo
library edit the "Oslo" section:

.. code-block:: yaml

   Oslo:
     ptl: Doug Hellmann (dhellmann)
     service: Common libraries
     mission:
       To produce a set of python libraries containing code shared by OpenStack
       projects. The APIs provided by these libraries should be high quality,
       stable, consistent, documented and generally applicable.
     url: https://wiki.openstack.org/wiki/Oslo
     tags:
       - name: team:diverse-affiliation
     projects:
       - repo: openstack/oslo-incubator
         tags:
           - name: release:has-stable-branches
       - repo: openstack/oslo.config
         tags:
           - name: release:independent
           - name: release:has-stable-branches
       - repo: openstack/oslo.messaging
         tags:
           - name: release:independent
           - name: release:has-stable-branches
       - repo: openstack/oslo.rootwrap
         tags:
           - name: release:independent
           - name: release:has-stable-branches
       - repo: openstack/oslosphinx
         tags:
           - name: release:independent
           - name: release:has-stable-branches
       - repo: openstack/cookiecutter
       - repo: openstack/pbr
         tags:
           - name: release:independent

You can check which tags to use, or the meaning of any tag, by
consulting the `list of currently allowed tags`_.

.. _list of currently allowed tags: https://governance.openstack.org/tc/reference/tags/index.html

When writing the commit message for this change, make this change
depend on the project creation change by including a link to its
Change-ID (from the previous step)::

    Depends-On: <Gerrit URL of project-config change>

Then, go back to the project-config change and add a link to the
Change-ID of the governance change in the project-config commit
message::

    Needed-By: <Gerrit URL of governance change>

so that reviewers know that the governance change has been created.

However, if you are creating an entirely new OpenStack project team
(i.e., adding a new top-level entry into
``reference/projects.yaml``), you should reverse the dependency
direction (the project creation change should depend on the
governance change because the TC needs to approve the new project
team application first).

Wait Here
---------

The rest of the process needs this initial import to finish, so
coordinate with the Infra team, and read ahead, but don't do any of
these other steps until the import is complete and the new repository
is configured.

The OpenDev team can be contacted by pinging ``infra-root`` in the
``#opendev`` channel on Freenode IRC, or via email to the `openstack-infra
<http://lists.openstack.org/cgi-bin/mailman/listinfo/openstack-infra>`_
mail list.

Update the Gerrit Group Members
-------------------------------

After the review is approved and :ref:`groups are created
<add-gerrit-permissions>` ask the Infra team to add you to both groups in
Gerrit, and then you can add other members by going to
https://review.opendev.org/#/admin/groups/ and filtering for your group's
names.

The project team lead (PTL), at least, should be added to
"<projectname>-release", and other developers who understand the
release process can volunteer to be added as well.

.. note::

   These Gerrit groups are self-managed. This means that any member
   of the group is able to add or remove other members. Consider
   this fact carefully when deciding to add others to a group, as
   you need to trust them all to collaborate on group management
   with you.

Updating devstack-vm-gate-wrap.sh
---------------------------------

The ``devstack-gate`` tools let us install OpenStack projects in a
consistent way so they can all be tested with a common
configuration. If your project will not need to be installed for
devstack gate jobs, you can skip this step.

Check out ``openstack/devstack-gate`` and edit
``devstack-vm-gate-wrap.sh`` to add the new project::

  PROJECTS="openstack/<projectname> $PROJECTS"

Keep the list in alphabetical order.

Preparing a New Git Repository using cookiecutter
=================================================

All OpenStack projects should use one of our cookiecutter_
templates for creating an initial repository to hold the source
code.

If you had an existing repository ready for import when you submitted
the change to project-config, you can skip this section.

Start by checking out a copy of your new repository:

.. code-block:: console

   $ git clone https://opendev.org/openstack/<projectname>

.. _cookiecutter: https://pypi.org/project/cookiecutter

.. code-block:: console

   $ pip install cookiecutter

Choosing the Right cookiecutter Template
----------------------------------------

The template in ``openstack/cookiecutter`` is suitable for
most projects.  It can be used as follows:

.. warning::

   Cookiecutter with '-f' option overwrites the contents of the
   <projectname> directory. Be careful when working with non-empty
   projects, it will overwrite any files you have which match names in the
   cookiecutter repository.

.. code-block:: console

   $ cookiecutter -f https://opendev.org/openstack/cookiecutter

Remember, as mentioned earlier, these commands should typically be used only
if you are working with an empty repository.

The template in ``openstack/specs-cookiecutter`` should be used for
specs:

.. code-block:: console

   $ cookiecutter -f https://opendev.org/openstack/specs-cookiecutter

The template in ``openstack/oslo-cookiecutter`` should be used for
Oslo libraries:

.. code-block:: console

   $ cookiecutter -f https://opendev.org/openstack/oslo-cookiecutter

The template in ``openstack/ui-cookiecutter`` should be used for
Horizon plugins:

.. code-block:: console

   $ cookiecutter -f https://opendev.org/openstack/ui-cookiecutter

Other templates are available; the full list can be seen at
https://opendev.org/explore/repos?q=cookiecutter&tab=.

Applying the Template
---------------------

Running cookiecutter will prompt you for several settings, based on
the template's configuration. It will then update your project
with a skeleton, ready to have your other files added.

.. code-block:: console

   $ cd <projectname>
   $ git review

.. _in-repo-zuul-jobs:

Adding In-Repo Zuul Jobs
------------------------

Every project needs test jobs.

OpenDev has a number of jobs and project-templates that can be used
directly in your project's Zuul config. You can also make new jobs that
inherit from existing jobs or or you can write your own from scratch.

To get yourself started with a completely minimal set that don't actually
do anything but do it successfully, you should add the ``noop-jobs`` template
to your project in a file called ``.zuul.yaml``:

.. code-block:: yaml

  - project:
      templates:
        - noop-jobs

Once your project is up and running you'll be able to add more jobs as you
go and are ready for them. When you do, make sure to remove the ``noop-jobs``
template, as it'll be telling Zuul to run jobs that don't do anything, which
is not needed once you have real jobs.

For more information on writing jobs for Zuul, see
https://zuul-ci.org/docs/zuul/reference/config.html and :ref:`zuul_best_practices`.

Mirroring Projects to Git Mirrors
=================================

Mirroring of git projects happens automatically to GitHub only for
OpenStack projects, mirroring for all other namespaces and to other
mirrors needs to be set up by the project team themselves.

To replicate your git project to a custom location, create a job that
inherits from the `upload-git-mirror
<https://zuul-ci.org/docs/zuul-jobs/general-roles.html#role-upload-git-mirror>`_
job.

This job wraps around the `upload-git-mirror
<https://zuul-ci.org/docs/zuul-jobs/general-roles.html#role-upload-git-mirror>`_
Ansible role that is part of the zuul-jobs library.

In order to use this job, you must supply a secret in the following format:

.. code-block:: none

    - secret:
        name: <name of your secret>
        data:
          user: <ssh user of the remote git server>
          host: <address of the remote git server>
          host_key: <ssh host key of the remote git server>
          ssh_key: <private key to authenticate with the remote git server>

For GitHub, the ``user`` parameter is ``git``, not your personal
username.

The ``host_key`` parameter can be retrieved from your ``known_hosts`` file
or with a command like `ssh-keyscan -H <host>` or `ssh-keyscan -t rsa
<host>`.

For example, the ``host_key`` when pushing to GitHub would be, on a single line::

    github.com ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==

The ``ssh_key`` parameter should be encrypted before being committed
to the git repository. Zuul provides a tool for easily encrypting
files such as SSH private keys and you can find more information about
it in the `documentation
<https://zuul-ci.org/docs/zuul/user/encryption.html>`_.

For example, encrypting a key for the "recordsansible/ara" project would
look like this:

.. code-block:: console

    $ zuul/tools/encrypt_secret.py \
      --infile /home/dmsimard/.ssh/ara_git_key \
      --strip \
      --tenant openstack https://zuul.openstack.org recordsansible/ara

You can then use the secret in a job inheriting from
``upload-git-mirror`` as such:

.. code-block:: none

   - job:
       name: <project>-upload-git-mirror
       parent: upload-git-mirror
       description: Mirrors <namespace>/<project> to neworg/<project>
       vars:
         git_mirror_repository: neworg/<project>
       secrets:
         - name: git_mirror_credentials
           secret: <name of your secret>
           pass-to-parent: true

Finally, the job must be set to run in your project's ``post``
pipeline which is triggered every time a new commit is merged to the
repository::

    - project:
        check:
          jobs:
            # [...]
        gate:
          jobs:
            # [...]
        post:
          jobs:
            - <project>-upload-git-mirror

Note that the replication would only begin *after* the change has
merged, meaning that merging the addition of the post job would not
trigger the post job itself immediately.
The post job will only trigger the next time that a commit is merged.

Verify That Gerrit and the Test Jobs are Working
================================================

The next step is to verify that you can submit a change request for
the project, have it pass the test jobs, approve it, and then have
it merge.

.. _setup_review:

Configure ``git review``
------------------------

If the new project you have added has a specified upstream you
will need to add a ``.gitreview`` file to the repository once it has
been created. This new file will allow you to use ``git review``.

The basic process is clone your new repository, add file, push to Gerrit,
review and approve:

.. code-block:: console

  $ git clone https://opendev.org/<namespace>/<projectname>
  $ cd <projectname>
  $ git checkout -b add-gitreview
  $ cat > .gitreview <<EOF
  [gerrit]
  host=review.opendev.org
  port=29418
  project=<namespace>/<projectname>.git
  EOF
  $ git review -s
  $ git add .gitreview
  $ git commit -m 'Add .gitreview file'
  $ git review

Verify that the Tests Pass
--------------------------

If you configure tests for an imported project, ensure that all
of the tests pass successfully before importing. Otherwise your
first change needs to fix all test failures. You can run most of the
tests locally using ``tox`` to verify that they pass.

Verify the Gerrit Review Permissions
------------------------------------

When your project is added to gerrit, the groups defined in the
ACLs file (see :ref:`add-gerrit-permissions`) are created, but they
are empty by default. Someone on the infrastructure team with gerrit
administrator privileges will need to add you to each group. After
that point, you can add other members.

To check the membership of the groups, visit
``https://review.opendev.org/#/admin/projects/openstack/<projectname>,access``
-- for example,
https://review.opendev.org/#/admin/projects/openstack/infra-manual,access
-- and then click on the group names displayed on that page to review
their membership.

Prepare an Initial Release
==========================

Make Your Project Useful
------------------------

Before going any farther, make the project do something useful.

If you are importing an existing project with features, you can
go ahead.

If you are creating a brand new project, add some code and tests
to provide some minimal functionality.

Provide Basic Project Documentation
-----------------------------------

Update the ``README.rst`` file to include a paragraph describing the
new project.

Update the rest of the documentation under ``doc/source`` with
information on how to contribute to the project. Add project-specific
documentation covering different content areas based on the intended audience,
such as installation, configuration, and administration. Follow the layout
of project documentation as described in `Project guide setup
<https://docs.openstack.org/doc-contrib-guide/project-guides.html>`_.

Tagging an Initial Release
--------------------------

To verify that the release machinery works, push a signed tag to the
"gerrit" remote. Use the smallest version number possible. If this is
the first release, use "0.1.0". If other releases of the project
exist, choose an appropriate next version number.

.. note::

   You must have GnuPG installed and an OpenPGP key configured for
   this step.

Run:

.. code-block:: console

  $ git tag -s -m "descriptive message" $version
  $ git push gerrit $version

Wait a little while for the pypi job to run and publish the release.

If you need to check the logs, you can use the `git-os-job`_ command:

.. code-block:: console

  $ git os-job $version

.. _git-os-job: https://pypi.org/project/git-os-job

See :ref:`tagging-a-release` in the Project Driver's Guide for more
detail on tag pushing workflows.

Allowing Other OpenStack Projects to Use Your Library
=====================================================

OpenStack projects share a common global requirements list so that all
components can be installed together on the same system. If you are
importing a new library project, you need to update that list to allow
other projects to use your library.

Update the Global Requirements List
-----------------------------------

If you have a library that is used by OpenStack repositories,
check out the ``openstack/requirements`` git repository and modify
``global-requirements.txt`` to:

#. add the new library
#. add any of the library's direct dependencies that are not already listed

Setting up Gate Testing
=======================

The devstack gate jobs install all OpenStack projects from source so
that the appropriate git revisions (head, or revisions in the merge
queue) are tested together. To include the new library in these tests,
it needs to be included in the list of projects in the devstack gate
wrapper script. For the same feature to work for developers outside of
the gate, the project needs to be added to the appropriate library
file of devstack.

Updating devstack
-----------------

#. Check out ``openstack/devstack``.

#. Edit the appropriate project file under ``lib`` to add a variable
   defining where the source should go. For example, when adding a new
   Oslo library add it to ``lib/oslo``::

     <PROJECTNAME>_DIR=$DEST/<projectname>

#. Edit the installation function in the same file to add commands to
   check out the project. For example, when adding an Oslo library,
   change :func:`install_oslo` in ``lib/oslo``.

   When adding the new item, consider the installation
   order. Dependencies installed from source need to be processed in
   order so that the lower-level packages are installed first (this
   avoids having a library installed from a package and then re-installed
   from source as a dependency of something else)::

     function install_oslo() {
       ...
       _do_install_oslo_lib "<projectname>"
       ...
     }

#. Edit ``stackrc`` to add the other variables needed for configuring the
   new library::

     # new-project
     <PROJECTNAME>_REPO=${<PROJECTNAME>_REPO:-${GIT_BASE}/openstack/<projectname>.git}
     <PROJECTNAME>_BRANCH=${<PROJECTNAME>_BRANCH:-master}

Add Links to Your Project Documentation
=======================================

If your project is not an official OpenStack project, skip this section.

Update the https://docs.openstack.org/ site with links to your project
documentation by following the instructions at `Template generator details
<https://docs.openstack.org/doc-contrib-guide/doc-tools/template-generator.html>`_.

.. _zuul_best_practices:

Zuul Best Practices
-------------------

There are a couple of best practices for setting up jobs.

Jobs that run outside of a branch context (release and tag jobs are
examples), should be in your tenant's ``project-config`` repository.
This repository should have a single branch named master removing
any ambiguity of which version of a job should run outside of a branch
contenxt.

You should also keep jobs that are expected to apply widely to a
tenants' repos here. As that helps keep coordination of changes
centralized.

Adding a New Job
~~~~~~~~~~~~~~~~

Jobs in Zuul are self-testing, which means that the change adding a
new job can run with that job applied into the project's pipelines. It's
a good idea when adding a new job in your project to put it at least
into the ``check`` pipeline so that you can verify that it runs as expected.

Use Templates
~~~~~~~~~~~~~

For many common cases, there are templates of jobs defined that can be applied
to your project. For instance:

.. code-block:: yaml

  - project-template:
      name: openstack-python27-jobs
        check:
          - openstack-tox-pep8
          - openstack-tox-py27
        gate:
          - openstack-tox-pep8
          - openstack-tox-py27

To apply that to your project, add it to the ``templates`` section:

.. code-block:: yaml

  - project:
      name: openstack/<projectname>
      templates:
        - openstack-python27-jobs

If you use the same set of tests in several repositories, introduce a
new template and use that one.

Non-Voting Jobs
~~~~~~~~~~~~~~~

A job can either be voting or non-voting. If you have a job that
is voting in one repository but non-voting in another, you can indicate
this by using a variant.

To make a single job non-voting everywhere, add ``voting: false`` in the
job definition.

.. code-block:: yaml

  - job:
      parent: devstack
      name: <projectname>-tempest-devstack-mongodb-full
      voting: false

and add it to your project pipelines:

.. code-block:: yaml

  - project:
      name: openstack/<projectname>
      templates:
        - openstack-python-jobs
      check:
        jobs:
          - <projectname>-tempest-devstack-mongodb-full

To use a job that is otherwise voting in your project but in a non-voting
manner, add ``voting: false`` to its entry in your project pipeline definition.

.. code-block:: yaml

  - project:
      name: openstack/<projectname>
      templates:
        - openstack-python-jobs
      check:
        jobs:
          - openstack-tox-py35:
              voting: false

Non-voting jobs should only be added to ``check`` queues. Do not add
them to the ``gate`` queue since running non-voting jobs in the gate
is just a waste of resources.

Running Jobs Only on Some Branches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to run the job only on a specific stable branch, add a branch
matcher to the job definition.

.. code-block:: yaml

  - job:
      parent: devstack
      name: <projectname>-tempest-devstack-mongodb-full
      voting: false
      branches: ^(?!stable/(juno|kilo)).*$

If, instead, you want to use an existing job in your project but only on
a specific branch, apply it in the project pipeline definition.

.. code-block:: yaml

  - project:
      name: openstack/<projectname>
      templates:
        - openstack-python-jobs
      check:
        jobs:
          - openstack-tox-py35:
              branches: ^(?!stable/(juno|kilo)).*$

The job above will run on ``master`` but also on newer stable
branches like ``stable/mitaka``. It will not run on the old
``stable/juno`` and ``stable/kilo`` branches.

Project Renames
===============

.. note::

   If you rename a project to move out from "openstack" namespace to
   any other namespace, follow `this OpenStack TC resolution
   <https://governance.openstack.org/tc/resolutions/20190711-mandatory-repository-retirement.html>`_
   instead.

The first step of doing a rename is understanding the required
governance changes needed by the rename. You can use the following
criteria:

For a project being added to existing official OpenStack project:
Create an ``openstack/governance`` change and add a "Depends-On:
project-change-url" of the change you make in the following steps to
the commit message, and add a comment in the
``openstack/project-config`` change that references the
governance change. You will also make sure the PTL has expressed
approval for the addition in some way.

When preparing to rename a project, begin by making changes to the
files in the ``openstack/project-config`` repository related
to your project.

When uploading your change, make sure the topic is "project-rename"
which can be done by submitting the review with the following
git review command:

.. code-block:: console

   $ git review -t project-rename

Members of the infrastructure team will review your change.

Finally, add it to the `Upcoming Project Renames
<https://wiki.openstack.org/wiki/Meetings/InfraTeamMeeting#Upcoming_Project_Renames>`_
section of the Infrastructure Team Meeting page to make sure
it's included in the next rename window.

.. note::

   Renames have to be done during a Gerrit maintenance window
   scheduled by the Infrastructure team, so it may take a few
   weeks for your rename to be completed.

Post rename, a member of the Infrastructure team will submit a patch to update
the :file:`.gitreview` file in the renamed project to point to the new project
name.

Other projects you may need to update post-rename:

* projects.txt in ``openstack/requirements``

Review List for New Projects
============================

Before approving a review for a new project creation, double check
the following:

#. Is there existing content to import? If the team want to preserve the
   history, they have to use the upstream key word to import. The
   infra team will not push anything to your repo - and cannot hand
   out those permissions either.

#. Will this be an official project? Then it needs a governance
   review, with a link to it via "Needed-By", and get PTL+1.

#. Will the repo release on pypi? Check that it https://pypi.org
   is set up correctly.

.. _Project Testing Interface: https://governance.openstack.org/tc/reference/project-testing-interface.html
