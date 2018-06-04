# qemu-kvm kickstart a multiple-nic VM

Building a multiple-nic VM is straightforward, but be careful to specify the networks in the correct order so that the correct virtual interface in the VM lines up with the correct interface in the os *running* in the VM.


## Example

This creates a two-nic VM with its *eth0* bridged to the LAN via the host's *br0* interface, and *eth1* bridged to the private host-only network via the host's *virbr0* interface created within qemu-kvm on the host.


### in the ‘virt-install’ command

    --network bridge=br0 --network bridge=virbr0

### in the ks.cfg

    network --bootproto=dhcp --device=eth0 onboot=on ipv6=auto
    network --bootproto=dhcp --device=eth1 onboot=off ipv6=auto


Bottom line - order matters in both virt-install options, and ks.cfg network definitions.
