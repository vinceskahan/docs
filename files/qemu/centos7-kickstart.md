# qemu-centos7-kickstart

Hands-off kickstarts rock :-)

## optional: create a virtual images pool
    mkdir -p /home/libvirt/images
    virsh pool-define-as --name libvirt-images \
       --type dir --target /home/libvirt/images \
       --source-format=raw
    virsh pool-start libvirt-images
    virsh pool-autostart libvirt-images

note: be aware that selinux might get in your way if you create the pool in a new/unpredictable directory.  Watch your syslogs for selinux issues.


## create the VM and launch its kickstart

Create a 10GB disk, 1GB ram, one-cpu VM attached to the host-only virbr0  network.

    virt-install \
       --network bridge:virbr0  \
       --ram=1024  --vcpus=1  \
       --disk pool=libvirt-images,format=img,size=10 \
       --graphics none  \
       --initrd-inject=/var/www/html/ks.cfg  \
       --extra-args="console=tty0 console=ttyS0,115200 ks=file:/ks.cfg"  \
       --location=/iso/CentOS-7.0-1406-x86_64-DVD/CentOS-7.0-1406-x86_64-DVD.iso  \
       --name vm12

The slick thing here is the *--initrd-inject* to insert the ks.cfg file into the initrd at runtime.  The pathname for this file has to be readable by the non-root user qemu runs as on centos7.  This example used the web document root.

note: 
If your host networking is not set up correctly, the installation can seem to hang especially if your VM is set to DHCP. Definitely follow the excellent Dell [howto (pdf)](http://linux.dell.com/files/whitepapers/KVM_Virtualization_in_RHEL_7_Made_Easy.pdf) document for how to set up your ethernet and bridge configurations on centos.

# minimal centos7 ks.cfg
    
    # autoreboot at the end
    reboot
    # suppress the eula 'hit return'
    eula --accept
    # set a root password we can remember
    rootpw --plaintext root_pass_here
    # suppress the timezone prompt
    #    potentially add --nontp if you want that off initially
    timezone America/Los_Angeles --isUtc
    # suppress the add a user prompt
    #    this example creates an admin user
    user --groups=wheel --name=joeuser --password=joeuser
    # Use CDROM installation media
    cdrom
    # Use text mode install
    text
    # Partition clearing information
    clearpart --all --initlabel --drives=vda
    #
    ## ---- automatically partition ----
    ## (after /boot and swap, / and /home will essentially split the disk)
    #
    autopart --type=lvm
    #
    ## ---- or manually partition ----
    #     part /boot --fstype=ext4 --size=500
    #     part pv.01        --grow --size=1
    #     volgroup vg1 pv.01
    #     logvol /           --fstype=xfs --name=lv_root   --vgname=vg1 --grow --size=1024 --maxsize=10240
    #     logvol swap                     --name=lv_swap   --vgname=vg1 --grow --size=6144 --maxsize=6144
    #     logvol /opt/puppet --fstype=xfs --name=lv_puppet --vgname=vg1 --grow --size=1024 --maxsize=51200
    #
    # System bootloader configuration
    bootloader --location=mbr --boot-drive=vda
    # Network information
    #-- dhcp
    network  --bootproto=dhcp --device=eth0 --onboot=off --ipv6=auto
    #-- or static
    #network  --bootproto=static --device=eth0 --onboot=off --ipv6=auto --ip=192.168.122.20 --netmask=255.255.255.0 --gateway=192.168.122.1 --nameserver=192.168.122.1
    # hostname
    network  --hostname=kvmtest.localdomain
    %packages
    @core
    # for arp
    net-tools
    # for diagnostics
    tcpdump
    %end



