
## setting up an external USB datastore on ESXi 6.7.0

This is verified on 6.7.0 on a 4th generation Intel NUC

(long details at https://www.virten.net/2016/11/usb-devices-as-vmfs-datastore-in-vsphere-esxi-6-5/)

### verify the disk is detected
  `esxcli hardware usb passthrough device list`

### stop+disable usbarbitrator so external usb disk is detected
   ```
   /etc/init.d/usbarbitrator stop
   chkconfig usbarbitrator --list
   chkconfig usbarbitrator off
   ```

### look for the disk
   `ls /dev/disks`
  
### label the disk
  in my case, the disk shows up as /dev/disks.5000000000000001 

  ```partedUtil mklabel /dev/disks/naa.5000000000000001 gpt```

### get the partition table info
  `partedUtil getptbl /dev/disks/naa.5000000000000001`

### calculate the end of the partition
  ```
     eval expr $(partedUtil getptbl /dev/disks/naa.5000000000000001 \
        | tail -1 | awk '{print $1 " \\* " $2 " \\* " $3}') - 1
  ```

### using the value returned, create a new partition table
  in my case, the value the above command returned was 195352006

  ```
   partedUtil setptbl /dev/disks/naa.5000000000000001 gpt \
     "1 2048 1953520064 AA31E02A400F11DB9590000C2911D1B8 0"
  ```

### format the new partition
  `vmkfstools -C vmfs6 -S USB-Datastore /dev/disks/naa.5000000000000001:1`
