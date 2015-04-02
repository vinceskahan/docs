# qemu-kvm installation of windows-8.1 pro

Installing Windows 8.1 Pro in a qemu-kvm VM under centos7 is similar to installing any other operating system. 


### create a .iso image of the Windows installation media

In this case lack of centos7 qemu-kvm device passthrough made me need to create a .iso image of my installation media with 'dd' and save it to the host.

```dd if=/dev/sr0 bs=1M of=/iso/win8.1pro/win8.1pro.iso```

### Connect into the host via VNC
On the Macbook Air, I have found that Microsoft Remote Desktop works the best for a free solution

### Create the VM via the usual virt-install command syntax

In this case we specify br0 so the VM will appear on the LAN, set the ram to 4G which seems to be a good default for light use, create a 30GB disk image in the "libvirt-images" storage pool on disk, and so on

Be sure to 'su' to get a root shell first...

    virt-install --network bridge=br0 --ram=4096 \
       --disk pool=libvirt-images,format=img,size=30 \
       --name win8 --cdrom=/iso/win8.1pro.iso
    
