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

As covered in :ref:`automated-testing`, developers can take steps when
Jenkins tests fail. Core reviewers, like other developers, can use these
same steps when rerunning tests. Core reviewers have an additional tool
for cases where gate testing fails due to reasons unrelated to the
current change, re-approval.

Core reviewers can approve changes again to trigger gate testing for
that particular change. Core reviewers should still heed the advice in
:ref:`automated-testing` to ensure that unrelated failures are properly
tracked.

When re-approving, core reviewers may need to work around a specific set
of Gerrit behavior. Gerrit only emits vote values in its event stream
when a reviewer's vote values change. This means that if a core reviewer
has already voted +1 Approved in the workflow category they will need
to leave a comment of +0 in the workflow category then re-approve with
a new +1 Approved comment.
