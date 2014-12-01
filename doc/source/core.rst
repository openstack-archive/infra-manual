:title: Core Reviewer's Guide

.. _core_manual:

Core Reviewer's Guide
#####################

Maintaining the Core Group
==========================

+/-2 votes
==========
Only core reviewers can give +2 and -2 votes. A vote of +2 indicates
that the core reviewer is agreeing with the patch.

A vote of -2 blocks a patch, it should only be given as exception.
For example, if a patch is approved and currently in the gate pipeline,
a -2 will block it from merging.

Note that -2 votes are the only votes that are sticky, they are not
reset when a new patch gets uploaded.

Approval
========

Once a patch has two +2 votes and neither any -2 votes or a Work in
Progress tag set, it is ready to be merged. Any core reviewer can
approve such a patch. A core reviewer can give a +2 and approval in
the same review.

Re-approval
===========

