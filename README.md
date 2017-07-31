Wikimedia Cloud VPS hostgroup generator
=======================================

Helper scripts for creating and using lists of Cloud VPS project hosts. These
lists can be used with dsh/pssh and/or clush to make it easier to do bulk
maintenance on Cloud VPS hosted VMs.

Usage
-----
```
$ pip install .
$ mkdir -p ~/.config/clustershell/groups.conf.d
$ cp conf/groups.conf ~/.config/clustershell/groups.conf
$ wmcs-hgg --all --classifiers conf/classifiers.yaml --output ~/.config/clustershell/groups.conf.d --clush
$ nodeset -L
$ clush -b -w @bastions -- uname -a
```

You will need to setup your `~/.config/clustershell/clush.conf` file properly
for the `clush` call to work.

License
-------
Copyright (c) 2017 Wikimedia Foundation and contributors
Copyright (c) 2017 Yuvi Panda

Licensed under the Apache License, Version 2.0. See the [`LICENSE`](LICENSE)
file for more details.
