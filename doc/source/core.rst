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

Work In Progress
================

The "Work in progress" (WIP) label tells anyone looking at a change
that more updates are still needed. Both the change's owner and any
core reviewer can set the WIP statusː

* A change owner can set this label on their own review to mark that
  additional changes are still being made, and to avoid unnecessary
  reviews while that happens.

* A core reviewer can set the WIP label to acknowledge that a
  contributor will definitely need to do more work on a change rather
  than merely expressing an opinion on its readiness. This can be a
  great convenience to fellow reviewers. It allows the core reviewer
  to politely send the message that the change needs additional work
  while simultaneously removing it from the list of ready changes
  until that happens.

A WIP label gets reset when a new patch is uploaded. The reviewer
that sets a WIP label, can also reset it.
