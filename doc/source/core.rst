:title: Core Reviewer's Guide

.. _core_manual:

Core Reviewer's Guide
#####################

Maintaining the Core Group
==========================

+/-2 votes
==========

Only core reviewers can give +2 and -2 votes. A vote of +2 indicates
that the core reviewer agrees that the patch can merge as is.

A vote of -2 blocks a patch completely, it should only be given in
exceptional cases. For example, if a patch is approved and currently
in the gate pipeline, a -2 will block it from merging.

Note that -2 votes are the only votes that are not reset when a new
patch gets uploaded. The core reviewer that gave a -2 is the only
person that can remove it again.

Approval
========

Once a patch has two +2 votes and neither any -2 votes or a Work in
Progress tag set, it is ready to be merged. Any core reviewer can
approve such a patch. A core reviewer can give a +2 and approval in
the same review.

Re-approval
===========

