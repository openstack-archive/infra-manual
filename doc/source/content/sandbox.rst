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

this will take you into your editor which you set in the git configuration
above. `Create a title for your commit message and add some text in the body.
<https://wiki.openstack.org/wiki/GitCommitMessages#Summary_of_GIT_commit_message_structure>`_
Then save the file and close the editor. Next submit your patch to gerrit::

  git review

You will get some output including a URL to your patch, click on the URL
and view your patch.

Now create a second patchset, in the same git branch as your first patchset,
make some changes, either create a new file or add or delete content in your
first file. Save your changes and stage them. To ensure you submit your new
patchset to the same change execute::

  git commit --amend

this takes you into your prior git commit message, which you can edit but you
don't have to, then save and close the editor containing the commit message.
Then run::

  git review

and again you should see a url that links to your patch. Viewing the patch
you should see a new patchset as patchset 2 below your original patchset 1,
you should not see a new change.
