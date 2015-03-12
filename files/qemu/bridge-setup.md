# qemu-kvm network setup

This is largely grabbed from the excellent [Dell whitepaper (pdf)](asdfasdfasdf) but is replicated here just in case the upstream page disappears in the future.

## create a bridge device to the local LAN

    # create a ifcfg-br0 and bring it up on the LAN with DHCP
    DEVICE="br0"
    BOOTPROTO="dhcp"
    IPV6INIT="yes"
    IPV6_AUTOCONF="yes"
    ONBOOT="yes"
    TYPE="Bridge"
    DELAY="0"

## set the wired NIC to bridge through the new device

    # add to your existing ifcfg-eno1
    BRIDGE=br0
        
 

## restart/refresh networking
    service NetworkManager restart
    (or equivalent systemctl command, or reboot)


## the resulting ‘ip a’ for the system

In this example, eno1 = wired, wlp2s0 = wireless (off), br0 = bridge to LAN, virbr0 = private bridge within qemu-kvm. Note the ip address is applied to the br0 bridge now, and not the (previous) location on the eno1 wired nic.

    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
    valid_lft forever preferred_lft forever
    2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP qlen 1000
    link/ether c0:3f:d5:66:c7:a4 brd ff:ff:ff:ff:ff:ff
    3: wlp2s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN qlen 1000
    link/ether a0:a8:cd:0f:46:d7 brd ff:ff:ff:ff:ff:ff
    4: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
    link/ether c0:3f:d5:66:c7:a4 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.138/24 brd 192.168.0.255 scope global dynamic br0
    valid_lft 8639425sec preferred_lft 8639425sec
    inet6 2601:8:b500:42f:c23f:d5ff:fe66:c7a4/64 scope global dynamic
    valid_lft 345259sec preferred_lft 345259sec
    inet6 fe80::c23f:d5ff:fe66:c7a4/64 scope link
    valid_lft forever preferred_lft forever
    5: virbr0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
    link/ether fe:54:00:47:28:65 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.1/24 brd 192.168.122.255 scope global virbr0
    valid_lft forever preferred_lft forever
    inet6 fe80::fc54:ff:fe47:2865/64 scope link
    valid_lft forever preferred_lft forever
    7: vnet0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master virbr0 state UNKNOWN qlen 500
    link/ether fe:54:00:47:28:65 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc54:ff:fe47:2865/64 scope link
    valid_lft forever preferred_lft forever
    
