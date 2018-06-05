:title: IRC Guide

.. TODO(mordred) Replace https://wiki.openstack.org/wiki/IRC with a link to
   this page.

.. _irc-guide:

IRC Guide
#########

The OpenStack Project makes heavy use of `Freenode`_ IRC. While the canonical
reference for Freenode is found in the `Freenode Knowledgebase`_, this document
contains some more specific information for those who are new to IRC and would
like to know more about common OpenStack practices.

.. _Freenode: http://freenode.net
.. _Freenode Knowledgebase: http://freenode.net/kb/all

Channel Logging
---------------

OpenStack IRC Channels and OpenStack IRC Meetings are logged to `eavesdrop`_.

.. _eavesdrop: http://eavesdrop.openstack.org/

.. TODO(mordred) Publish a list of Official Channels from the
   accessbot/channels.yaml file to eavesdrop.openstack.org and point to that
   list here.

Just Start Talking
------------------

Also known as "`No Naked Pings`_".

When interacting with other OpenStack Developers over IRC, just start talking.
Starting with "ping", "hi, are you there?" or "do you have a minute?" might
seem polite, but it's actually more distracting. If you have a question, just
ask it.

Be prepared that it might not get answered the first time as people tend to
multi-task. It's ok to re-ask after a while, but try to be aware if there is a
lot of activity going on that the person or people you are looking for may not
be in a position to answer right at that moment.

.. _No Naked Pings: https://fedoraproject.org/wiki/No_naked_pings

Talking to specific people
--------------------------

To talk to a specific person, prefix the line with their name. For instance,
to ask ``mordred`` a question:

::
  mordred: I'm having a problem with this patch, https://review.openstack.org/#/c/530978/, could you help me figure out it?

It is not required or useful to prefix someone's name with an ``@``, it's
just extra typing and looks weird in IRC clients.

Use a pastebin for communicating long content
---------------------------------------------

OpenStack runs a `pastebin service`_ that can be used for pasting content and
then getting a link that can be copied into IRC. Pasting more than one or two
lines floods the channel and makes other communication difficult.

.. _pastebin service: http://paste.openstack.org/

.. _irc-technical-support:

Technical Support
-----------------

The OpenStack Infra team is responsible for maintaining the developer
infrastructure systems used by the OpenStack project. The team is in the
``#openstack-infra`` channel. As they are technical support for the entire
OpenStack project, the channel can be quite busy. However, they are there to
help, so if you have issues, asking in ``#openstack-infra`` is completely
appropriate. Just remember that it's best to just ask your question, and that
sometimes it might be extra busy so you might need to be patient.
If there is an issue that seems to require urgent attention by someone with
access to one of the servers, you can mention ``infra-root`` in your message.
Likewise, if you would like to get the attention of the core reviewers for
one of our configuration repositories, use the keyword ``config-core``.

Persistent Clients and IRC Bouncers
-----------------------------------

Many OpenStack developers prefer to run an "IRC Bouncer" to allow for being
always connected.

.. note:: It is **NOT** required to have a persistent IRC connection. Indeed,
          some developers explicitly disconnect. The information here is
          intended to be helpful for those who would like to have a persistent
          connection but are not sure how.

A common pattern is to run either `weechat`_ or `irssi`_ inside of `screen`_
or `tmux`_ on a Cloud Server or some other computer that is always connected
to the Internet.

For those who prefer graphical IRC clients, another approach is to run a
proxy server like `ZNC`_ or `bip`_ and connect through it.

For people who do not have access to a convenient persistent Cloud Server or
do not care to manage a long-lived server, `IRCCloud`_ is a web-based
IRC client that provides an optional (paid) persistent connection.

.. note:: As an OpenStack developer, it may be worth the effort to find an
          OpenStack Cloud on which to run a bouncer. Being an OpenStack End
          User is a great way to ensure good context for the End User
          experience.

.. _irssi: https://irssi.org/
.. _weechat: https://weechat.org/
.. _screen: https://www.gnu.org/software/screen/
.. _tmux: https://github.com/tmux/tmux/wiki
.. _znc: https://en.wikipedia.org/wiki/ZNC
.. _bip: https://bip.milkypond.org/
.. _irccloud: https://www.irccloud.com
