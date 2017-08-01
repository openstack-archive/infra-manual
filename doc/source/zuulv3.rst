:title: Zuul v3 Migration Guide

Zuul v3 Migration Guide
#######################

This is a temporary section of the Infra Manual to assist in the
conversion to Zuul v3.  Some of the content herein will only be
relevant before and shortly after we move from Zuul v2 to v3.

What is Zuul v3?
================

Zuul v3 is the third major version of the project gating system
developed for use by the OpenStack project as part of its software
development process.  It includes several major new features and
backwards incompatible changes from previous versions.

It was first described in the `Zuul v3 spec`_.

In short, the major new features of interest to OpenStack developers
are:

* In-repo configuration
* Native support for multi-node jobs
* Ansible job content
* Integration with more systems

We're pretty excited about Zuul v3, and we think it's going to improve
the devolpment process for all OpenStack developers.  But we also know
that not everyone needs to know everything about Zuul v3 in order for
this to work.  The sections below provide increasing amounts of
information about Zuul v3.  Please at least read the first section,
and then continue reading as long as subsequent sections remain
relevant to the way you work.

.. _Zuul v3 spec: http://specs.openstack.org/openstack-infra/infra-specs/specs/zuulv3.html

What's the Minimum I Need to Know?
==================================

You have stuff to do, and most of it doesn't involve the CI system, so
this will be short.

The name of the CI system will be changing
------------------------------------------

For varied historical reasons, the name OpenStack's CI system used to
report to Gerrit has been Jenkins, even 5 years after it actually
became Zuul doing the reporting and 1 year after we stopped using
Jenkins altogether.  We're *finally* changing it to Zuul.  If you see
a comment from **Jenkins**, it's Zuul v2.  If you see a comment from
**Zuul**, it's Zuul v3.

Job names will be changing
--------------------------

In Zuul v2, almost every project has a unique `python27` job.  For
example, `gate-nova-python27`.  In v3, we will have a single python27
job that can be used for every project.  So when Zuul reports on your
changes, the job name will now be `openstack-py27` rather than
`gate-project-python27`.

.. TODO: xref job naming guide

Most jobs will be migrated automatically
----------------------------------------

The jobs covered by the Consistent Testing Interface will all be
migrated automatically and you should not need to do anything.  Most
devstack jobs should be migrated as well.  If your project uses only
these jobs, you shouldn't need to do anything; we'll handle it for
you.

If you have custom jobs for your project, you or someone from your
project should keep reading this document.

My Project Has Customized Jobs, Tell Me More
============================================

TODO

I Write Jobs From Scratch, How Does Zuul v3 Actually Work?
==========================================================

TODO
