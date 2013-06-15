appfap
======

AppNap for Linux prototype

setup
=====

# chown youruser:yourgroup /sys/fs/cgroup/cpu/
$ mkdir /sys/fs/cgroup/cpu/fapped
$ echo 10000 > /sys/fs/cgroup/cpu/fapped/cpu.cfs_period_us
$ python appfap.py

