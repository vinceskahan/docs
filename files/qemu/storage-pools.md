# qemu-kvm storage pools

This is a nice feature that at a minimum saves typing, and also has some additional ability to let you define specific disk resources to put VMs into. For more information, see the [libvirt reference](https://libvirt.org/storage.html) or [Red Hat reference](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Virtualization_Administration_Guide/chap-Virtualization_Administration_Guide-Storage_Pools-Storage_Pools.html#sect-Virtualization-Storage_Pools-Creating-Dedicated_Disk_Devices).

## create a virtual images pool
    mkdir -p /home/libvirt/images
    virsh pool-define-as --name libvirt-images \
       --type dir --target /home/libvirt/images \
       --source-format=raw
    virsh pool-start libvirt-images
    virsh pool-autostart libvirt-images

note: be aware that selinux might get in your way if you create the pool in a new/unpredictable directory.  Watch your syslogs for selinux issues.


## create a VM referencing the pool

    virt-install \
       --network bridge:virbr0  \
       --ram=1024  --vcpus=1  \
       --disk pool=libvirt-images,format=img,size=10 \
       --graphics none  \
       --initrd-inject=/var/www/html/ks.cfg  \
       --extra-args="console=tty0 console=ttyS0,115200 ks=file:/ks.cfg"  \
       --location=/iso/CentOS-7.0-1406-x86_64-DVD/CentOS-7.0-1406-x86_64-DVD.iso  \
       --name vm12

## which pool(s) are present
```
root@nuc ~ $ virsh pool-list
Name                 State      Autostart
-----------------------------------------
default              active     yes
libvirt-images       active     yes
```

## refreshing the pool
If you do a lot of repetitive create/destroy/undefine operations and deleting the dangling VM image cycles, you can sometimes confuse qemu-kvm to the point where it will not successfully clone a VM.  The workaround is to:

```virsh pool-refresh my_pool_name```

It's probably wise to pool-refresh whenever you delete a VM.

