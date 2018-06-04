# CentOS 6 installation in ESXi 5.5

There's little special about installing centOS-6 under ESXi. Here's one way to do it using the vSphere client.


## assumptions

* iso images are on the ESXi host and therefore mountable to boot off of

## initial installation

* configure in the VSphere client as a linux / centos6 host, only 1GB ram needed at least initially
* set the iso to point to your DVD image on the ESXi host, device enabled
* power up the vm do installation, default answers should be fine.
* Initially select just the basic server installation. You should see anaconda install approximately 217 rpms
* take the reboot at the end

## firstboot configuration

mount the iso image

    mkdir /media/cdrom
    mount /dev/sr0 /media/cdrom

add git

    yum --disablerepo=\* --enablerepo=c6-media install -y git

configure git so checkins work

    git config --global user.name root
    git config --global user.email root 

##optionally add network configuration gui

* similarly, add system-config-network-tui if you want a graphical tool for setting the network configuration

unmount the DVD image

    umount /dev/sr0

## optionally add vmtools

use the VSphere gui to select installing the tools

    mount /dev/sr0 /media/cdrom
    cd /tmp
    tar zxvf /media/cdrom/VMware*tgz
    umount /dev/sr0
    cd vmware-tools
    ./vmware-tools-install.pl --default
    (and reboot)
