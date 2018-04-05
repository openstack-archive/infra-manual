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

Move into the root directory for the sandbox repo::

  cd sandbox

Configure Git::

  git config user.name "firstname lastname"
  git config user.email "yourname@yourdomain.tld"
  git config core.editor "yourfavouriteeditor"

Then configure git-review so that it knows about Gerrit. If you don't, it will
do so the first time you submit a change for review. You will probably want to
do this ahead of time though so the Gerrit Change-Id commit hook gets
installed. To do so::

  git review -s

Create a git branch locally from the sandbox repo master branch::

  git checkout -b new-branch

Create a new file, add some content and save the file::

  cat > first-file << EOF
     This is my first changeset for OpenStack.
  EOF

Run::

  git status

and stage your changes with::

  git add first-file

or::

  git add .

or::

  git add -a

Next commit your change with::

  git commit

.. note::
    This will take you into your editor which you set with ``git config core.editor``.

`Create a title for your commit message and add some text in the body.
<https://wiki.openstack.org/wiki/GitCommitMessages#Summary_of_Git_commit_message_structure>`_
Then save the file and close the editor. Next submit your patchset to gerrit::

  git review

You will see on screen a message confirming that the change has been
submitted for review and a URL to your change on
https://review.openstack.org. Click on the URL and view your patchset.

You will also receive one or more emails from the
`automatic testing system <https://docs.openstack.org/infra/manual/developers.html#automated-testing>`_,
reporting the testing results of your newly committed change.

Now create a second patchset, in the same git branch as your first patchset.
Make some changes, add or delete content to the first-file or create a
new file::

  cat > second-file << EOF
   This is my second OpenStack file for that first changeset.
  EOF
  
Now add the second file::

  git add second-file
  
or::

  git add .

or::

  git add -a

To ensure you submit your new patchset to the same change execute::

  git commit -a --amend

this takes you into your prior git commit message, which you can edit but you
don't have to. Don't modify the line starting with Change-Id. You can
save and close the editor containing the commit message. Then run::

  git review

and again you should see a URL that links to your change. Open the
web browser and look at the changeset you just submitted: notice that
there are two patchsets now, with patchset 2 below your original
patchset 1. If you have two different URI something went wrong, most
likely you have not used ``--amend`` in your git commit or you've
changed the line Change-Id in your commit message.

As a last step, you should abandon your change. You can do this from
the web UI by visiting the URL of the change and hitting the *Abandon*
button. Alternatively you can abandon a change from command
line using `Gerrit ssh commands <https://review.openstack.org/Documentation/cmd-review.html>`_::

  ssh -l <YOUR_GERRIT_USERNAME>\
      -p 29418 \
      review.openstack.org 'gerrit review' \
      --project openstack-dev/sandbox.git \
      --abandon <THE_CHANGE_ID>,2
