:title: Core Reviewer's Guide

.. _core_manual:

Core Reviewer's Guide
#####################

Maintaining the Core Group
==========================

+/-2 votes
==========

Approval
========

Re-approval
===========

As covered in ref:`failed-tests` developers can take steps when Jenkins
tests fail. Core reviewers, like other developers, can use these same
steps when rerunning tests. Core reviewers have an additional tool for
cases where gate testing fails due to reasons unrelated to the current
change, re-approval.

Core reviewers can approve changes again to trigger gate testing for
that particular change. Core reviewers should still heed the advice in
ref:`failed-tests` to ensure that unrelated failure are properly tracked.
