# ESXi quick reference
Capturing ESXi trivia for easy searching....

## Which VMs are currently running

```
esxcli vm process list
```

## Force stop/kill a VM

```
esxcli vm process list
     get the World ID from the output
esxcli vm process kill -t soft|hard|force -w world_id_here
```

## host control from the commandline
unfortunately, this requires the vim-cmd suite of commands

```
# example - enter maintenance mode
vim-cmd hostsvc/maintenance_mode_enter
```

putting the host into maint mode when it is already there will return an error


## Clone a VM from the command line – (see also) (see also)

```
cd /vmfs/volume/vm
mkdir NEW_DIR
ls OLD_DIR  and note the filename of the big disk .vmdk file

vmkfstools -i OLD_DIR/FILENAME.vmdk NEW_DIR/FILENAME.vmdk -d thin

create a new VM in the VSphere gui, select custom configuration
use existing VM
navigate to the new directory and pick the .vmdk filename

boot the new vm up and login via the vSphere console, change its hostname and reboot

```
After the new VM boots up with its new hostname, register it with Spacewalk:

```
rhnreg_ks –activationkey=KEY_HERE –serverurl=htp://spacewalk.localdomain/XMLRPC [ –force ]
```

add the new VM to DNS

add to /etc/hosts on the DNSMASQ server and reset DNSMASQ to make it take effect

## ESXi versions of typical commands

top => esxtop   ([VMware KB link](https://communities.vmware.com/docs/DOC-9279))

* on a Mac you probably need to set TERM=xterm to get correct appearance
