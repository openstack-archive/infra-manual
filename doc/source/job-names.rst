=======================================
Consistent Naming for Jobs with Zuul v3
=======================================

With the move to version 3 of Zuul, it is time to define a guideance
on how jobs should be named for consistency across projects in the
OpenStack project.

This document describes a consistent naming scheme for jobs for Zuul
v3. The goal is to give job developer and reviewers of jobs a common
document as reference.

.. warning:: This is a living document, it will get updates as the
             migration to Zuul v3 moves forward.

Previous Naming with Zuul v2
============================

As an example for the current usage with Zuul v2, here are some
job names:

* gate-REPO-python27
* gate-REPO-python35-nv
* gate-grenade-dsvm-neutron-forward
* gate-neutron-dsvm-api-ubuntu-trusty
* gate-neutron-fwaas-requirements
* gate-tempest-dsvm-neutron-full-ssh
* gate-neutron-docs-ubuntu-xenial
* neutron-docs-ubuntu-xenial

The current (Zuul v2) naming scheme as used at time of writing
(July 2017) is basically:

* Jobs in check and gate queues start with ``gate``
* Jobs in periodic queue start with ``periodic``
* Jobs in post and release queues have no special starting name
* Jobs that use devstack setup include ``dsvm`` in the name
* Jobs include the name of the repository
* Jobs can have a suffix of ``-nv`` to mark them as non-voting
* Jobs can have node name like ``ubuntu-xenial`` as last part of
  name - only followed by the optional ``-nv`` suffix.

Naming with Zuul v3
===================

The way Zuul v3 handles jobs, allows us to make changes to the job
names and also gives the chance to remove some relicts:

* Remove ``gate`` prefix, it's not really needed.
* Make clear what are publishing jobs. Name the test job and the
  publish job (currently ``gate-nova-docs-ubuntu-xenial`` and
  ``nova-docs-ubuntu-xenial``) clearer.
* Remove ``dsvm`` in name, it is a historic relict.
* Remove the ``{repository}`` from the name, it is not needed anymore.


This all leads to the following naming scheme:

* The general pattern is
  ``{prefix-}MAINPURPOSE-DETAILS{-}{node}{suffix}``.

* Jobs in check, gate, post, release queues have in general no special
  prefix, there's no need to use ``gate-`` as it was done with Zuul
  v2.

* There is in general no need to give the name of the repository as
  part of the job as it was done with Zuul v2.

* Jobs in periodic queue have the prefix ``periodic``.

* Publishing jobs, like documentation or tarball uploads, have a
  prefix of ``publish`` like ``publish-tarball`` and
  ``publish-sphinx-docs``.

  These jobs are normally run in a post queue.

* Jobs that build an artefact without uploading  ``build`` like
  ``build-sphinx-docs``.

* Jobs have the optional suffixes ``{node}`` and ``{suffix}`` where
  only ``-nv`` is valid for ``{suffix}``. If both exist, the order is
  ``{node}{suffix}``.

* The suffix ``{node}`` is used when a test should be run on different
  platforms like on CentOS, Fedora, openSUSE,  or Ubuntu - or on
  different versions of these. For jobs that are only run on one
  platform, the suffix ``{node}`` should be avoided.
  The suffix ``{node}`` is the name for the node the job runs on. If
  this is a a multi-node job, it's the name of the underlying single
  node.

* Use consistent names like "integration", "functional", "rally",
  "tempest", "grenade", "devstack" (what do we need? Those should be
  explained) as ``MAINPURPOSE``.

* Components of job names are separated by ``-``.

* Do not use "." for versions, just cat them together like ``35`` for
  Python 3.5.

* Since Zuul v3 allows overriding of job and definition of jobs, care
  should be taken not to use the same name for different jobs:

  * If you override a generic Zuul job for global OpenStack usage,
    name it ``openstack-``.
  * If you define a job in a specific repo, the name of the job should
    use the repository name as ``prefix`` or as first part of it.

So, this would change the initial list of names as follows:

* gate-REPO-python27 -> tox-py27 or openstack-py27
* gate-REPO-python35-nv -> tox-py35-nv or openstack-py35-nv
* gate-grenade-dsvm-neutron-forward -> grenade-neutron-forward
* gate-neutron-dsvm-api-ubuntu-trusty -> neutron-dsvm-api (or
  neutron-dsvm-api-ubuntu-trusty if multiple OSes need to be tested)
* gate-neutron-fwaas-requirements -> requirements
* gate-tempest-dsvm-neutron-full-ssh -> tempest-neutron-full-ssh
* gate-neutron-docs-ubuntu-xenial -> build-sphinx-docs
* neutron-docs-ubuntu-xenial -> publish-sphinx-docs
