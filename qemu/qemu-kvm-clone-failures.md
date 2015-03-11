# qemu-kvm failing to clone under some circumstances

If you do a lot of virt-install, virsh undefine, virtual image deletion, etc. with the same ‘name’ of the vm, especially using a virtual disk pool, you can confuse qemu-kvm to the point where it will error out when you try to clone the VM.

The workaround/fix is to refresh the pool with:

```
virsh pool-refresh my_pool_name
```