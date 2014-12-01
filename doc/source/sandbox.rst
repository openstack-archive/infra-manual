.. _sandbox:

Learn the Gerrit Workflow in the Sandbox
----------------------------------------

OpenStack has a sandbox repository for learning and testing purposes:
https://git.openstack.org/cgit/openstack-dev/sandbox. This is a great
repository to begin your OpenStack learning. It allows you to experiment
with the workflow and try different options so you can learn what they do.
Please only create 2 or 3 different changes and submit new patchsets to
those few changes. Please don't create 10 or more changes, this is not the
intention of this repository.

Clone the sandbox repo::

  git clone https://git.openstack.org/openstack-dev/sandbox.git

Move into the root directory for the sandbox repo. Configure Git::

  git config user.name "<firstname lastname>"
  git config user.email "<yourname@yourdomain.tld>"
  git config user.editor "<yourfavouriteeditor>"

Then configure git-review so that it knows about Gerrit. If you don't, it will
do so the first time you submit a change for review. You will probably want to
do this ahead of time though so the Gerrit Change-Id commit hook gets
installed. To do so::

  cd sandbox
  git review -s

Create a git branch locally from the sandbox repo master branch::

  git checkout -b <new-branch>

Create a new file, add some content and save the file.
Run::

  git status

and stage your changes with::

  git add <filename>

or::

  git add .

or::

  git add -a

Next commit your change with::

  git commit

.. note::
    This will take you into your editor which you set with ``git config user.editor``.

`Create a title for your commit message and add some text in the body.
<https://wiki.openstack.org/wiki/GitCommitMessages#Summary_of_GIT_commit_message_structure>`_
Then save the file and close the editor. Next submit your patchset to gerrit::

  git review

You will get some output including a URL to your change, click on the URL
and view your patchset.

Now create a second patchset, in the same git branch as your first patchset,
make some changes, either create a new file or add or delete content in your
first file. Save your changes and stage them. To ensure you submit your new
patchset to the same change execute::

  git commit --amend

this takes you into your prior git commit message, which you can edit but you
don't have to, then save and close the editor containing the commit message.
Then run::

  git review

and again you should see a URL that links to your change. Viewing the change
you should see a new patchset as patchset 2 below your original patchset 1,
you should not see a new change.
