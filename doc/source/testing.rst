:title: Test Environment Information

.. _test_env:

Test Environment
################

This document should give you a good idea of what you can count on
in the test environments managed by the Infrastructure team. This
information may be useful when creating new jobs or debugging existing
jobs.

Unprivileged Single Use VMs
===========================

All jobs currently run on these nodes. These are single use VMs
booted in OpenStack clouds. You should start here unless you know you
have a reason to use a privileged VM.

Each single use VM has these attributes which you can count on:

* Every instance has a public IP address. This may be an IPv4 address
  or an IPv6 address or maybe both.

  * You may not get both, it is entirely valid for an instance to have
    only a public IPv6 address and for another to have only a public
    IPv4 address.

  * In some cases the public IPv4 address is provided via NAT and the
    instance will only see a private IPv4 address. In some cases
    instances may have both a public and a private IPv4 address.

  * It is also possible that these addresses are on multiple network
    interfaces.

* CPUs are all running x86-64.
* There is at least 8GB of system memory available.
* There is at least 80GB of disk available. This disk may not all be
  exposed in a single filesystem partition and so not all mounted at
  /. Any additional disk can be partitioned, formatted and mounted
  by the root user; though if you need this it is recommended to use
  devstack-gate which takes care of it automatically and mounts the
  extra space on /opt early in its setup phase.
  To give you an idea of what this can look like most clouds just give
  us an 80GB or bigger /. One cloud gives us a 40GB / and 80GB /opt.
  Generally you will want to write large things to /opt to take
  advantage of available disk.
* Swap is not guaranteed to be present. Some clouds give us swap and
  others do not. Some tests (like devstack-gate based tests) will create
  swap either using a second disk device if available or by using a
  file otherwise. Be aware you may need to create swap if you need it.
* Filesystems are ext4. If you need other filesystems you can create
  them on files mounted via loop devices.
* Package mirrors for PyPi, NPM, Ubuntu, Debian, and Centos 7 (including
  EPEL) are provided and preconfigured on these instances before starting
  any jobs. We also have mirrors for Ceph and Ubuntu Cloud Archive that
  jobs must opt into using (details for these are written to disk on the
  test instances but are disabled by default).

Because these instances are single use we are able to give jobs full
root access to them. This means you can install system packages, modify
partition tables, and so on. Note that if you reboot the test instances
you will need to restart the zuul-console process.

If jobs need to perform privileged actions they can do so using Zuul v3's
secrets. Things like AFS access tokens or dockerhub credentials can
be stored in Zuul secrets then used by jobs to perform privileged
actions requiring this data. Please refer to the Zuul documentation
for more info.

Known Differences to Watch Out For
==================================

* Underlying hypervisors are not all the same. You may run into KVM
  or Xen and possibly others depending on the cloud in use.
* CPU count, speed, and supported processor flags differ, sometimes
  even within the same cloud region.
* Nested virt is not available in all clouds. And in clouds where it
  is enabled we have observed a higher rate of crashed test VMs when
  using it. As a result we enforce qemu when running devstack and
  may further restrict the use of nested virt.
* Some clouds give us multiple network interfaces, some only give
  us one. In the case of multiple network interfaces some clouds
  give all of them Internet routable addresses and some others do
  not.
* Geographic location is widely variable. We have instances all across
  North America and in Europe. This may affect network performance
  between instances and network resources geographically distant.
* Some network protocols may be blocked in some clouds. Specfically
  we have had problems with GRE. You can rely on TCP, UDP, and ICMP
  being functional on all of our clouds.
