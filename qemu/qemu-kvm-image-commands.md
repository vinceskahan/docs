# qemu-kvm image-related commands

list images

```virsh list --all```

stop an image

```virsh destroy imagename```

remove an image from the list

    virsh undefine imagename
    (then delete the .img file where it's located)

