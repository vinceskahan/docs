# installing debian netinst from local iso image

This builds a minimal debian VM using a local copy of the netinst image, attached to the local bridged network adaptor.

```
virt-install --accelerate --hvm \
  --cdrom /iso/debian-7.8.0-amd64-netinst.iso --name debian \
  --ram 1024 --disk pool=libvirt-images,format=img,size=10 \
  --network bridge:br0 --vnc
```


This kicked to the installer gui, which wasn't readable over a ssh connection.  VNC'd into the host and ran *virt-manager* then opened the running session which
got me access to the console to answer the questions.

Obviously longer term, a fully scripted installation with a DevOps tool or the debian equivalent to kickstart would be nice to know how to do.

### potential gotchas

*  over ssh, the console grabbed the cursor and it wouldn't release it, so be forewarned

* after completing, shut down the vm from its console and 'then' could get to the view console window to kill it

* then did a 'virsh start yourImageName' and ssh'd in just fine


