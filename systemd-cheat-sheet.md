# systemd cheat sheet for sysVinit users

The Fedora Project has a great [cheat sheet](https://fedoraproject.org/wiki/SysVinit_to_Systemd_Cheatsheet) that shows the basic differences.

Short synopsis is:

* files are located under */etc/systemd/system*
* general command syntax is `systemctl verb noun` 

	for example:
	```
	systemctl enable foo
	```

CentOS7 in general supports the old format 'service' command as a compatibility measure, calling 'systemctl' appropriately.