==============
OpenDev Manual
==============

To build the manual, execute the following command::

  $ tox

After running ``tox``, the documentation will be available for viewing
in HTML format in the ``doc/build/`` directory.

Terminology
===========

A note on terminology use in the manual:

This is a manual that describes how to use the OpenDev
infrastructure.

Project hosted in OpenDev like the OpenStack project, and the
Technical Committee
(TC) in particular, from time to time uses words such as "project",
"team", "program", "repository", etc. to help classify how it
organizes the project from an administrative point of view.

This manual is in service of OpenDev, but does so primarily by
documenting how developers and project drivers can use the
infrastructure to accomplish their work.  Hosted projects may change its
terms from time to time, it is not necessary for us to change all of
the terminology in this manual to match.  We should strive for
consistent terminology that matches what developers and our tooling
use.  This manual only describes hosted project specific processes in
exceptional cases and if we do so, we should use
the current TC terminology to avoid confusion.

Generally speaking these terms should be used as follows:

Project: The overall idea that there is a bunch of people working on a
bunch of code/text/etc.  It can also refer to that actual collection
of code/text/etc (for instance, a project can be bundled up into a
tarball, and extracted into a directory).  When a tool interacts with
that collection of code/text/etc, it interacts with the project (even
if it does so via the mechanism of git).

Repository: There are times when one needs to refer to the actual
source code management system of a project, that is, "git", and the
actual technical implementations of that SCM.  In those cases where it
is important to distinguish the actual attributes of the SCM from the
project, it is useful to use the word "repository".
