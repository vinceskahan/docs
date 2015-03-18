# Add a volume group to a CentOS7 system

This example adds a volume group referencing the free (unpartitioned) disk space on a second disk in a Intel NUC.  In this case, the disk is /dev/sda as this particular system has its CentOS os on /dev/sdb.

Credits - the following is loosely based on the very good [A Beginner's Guide to LVM](https://www.howtoforge.com/linux_lvm) on HowToForge from 2007.


## Create a partition on the unused portion of the disk

In this example, we'll be adding a volume group containing logical volume(s) on a pre-existing disk that is not bare.  In this case, the disk has pre-existing data from a VMware ESXi 5.5 installation that we want to keep around without damaging it.  We'll use just the rest of the data disk for our new volume group and logical volume(s).

Display the starting partition table on the disk:
  
    root@nuc ~ $ parted /dev/sda print free
    Model: ATA WDC WD10JFCX-68N (scsi)
    Disk /dev/sda: 1000GB
    Sector size (logical/physical): 512B/4096B
    Partition Table: gpt
    Disk Flags:
    
    Number  Start   End     Size    File system  Name  Flags
            17.4kB  1049kB  1031kB  Free Space
     1      1049kB  537GB   537GB
            537GB   1000GB  463GB   Free Space
  

Use 'parted' to create a partition named 'sdaPart2' using all of the free space at the top of the disk.  Initially use a type of ext2.
    
    root@nuc ~ $ parted /dev/sda mkpart sdaPart2 ext2 537GB 1000GB
    Information: You may need to update /etc/fstab.
    

Notice that parted aligned the partitions optimally, so there is a little free space unused as a result.
    
    root@nuc ~ $ parted /dev/sda print free
    Model: ATA WDC WD10JFCX-68N (scsi)
    Disk /dev/sda: 1000GB
    Sector size (logical/physical): 512B/4096B
    Partition Table: gpt
    Disk Flags:
    
    Number  Start   End     Size    File system  Name      Flags
            17.4kB  1049kB  1031kB  Free Space
     1      1049kB  537GB   537GB
     2      537GB   1000GB  463GB                sdaPart2
            1000GB  1000GB  729kB   Free Space
    

Configure the new partition as LVM:

    root@nuc ~ $ parted /dev/sda set 2 lvm on
    Information: You may need to update /etc/fstab.

Again, verify it worked:
    
    root@nuc ~ $ parted /dev/sda print free
    Model: ATA WDC WD10JFCX-68N (scsi)
    Disk /dev/sda: 1000GB
    Sector size (logical/physical): 512B/4096B
    Partition Table: gpt
    Disk Flags:
    
    Number  Start   End     Size    File system  Name      Flags
            17.4kB  1049kB  1031kB  Free Space
     1      1049kB  537GB   537GB
     2      537GB   1000GB  463GB                sdaPart2  lvm
            1000GB  1000GB  729kB   Free Space


## Create the LVM physical volume and allocate this partition to it

    root@nuc ~ $ pvcreate /dev/sda2
      Physical volume "/dev/sda2" successfully created
    
## Create the volume group, containing the LVM physical volume we just created

The disk is a Western Digital Red, so lets call it "wdRed"

    root@nuc ~ $ vgcreate wdRed /dev/sda2
      Volume group "wdRed" successfully created

## Next, use a portion of the volume group and create a logical volume

Again, it's logical volume 1 in that volume group, so name it wdRedLV1 for lack of a better idea
    
    root@nuc ~ $ lvcreate --name wdRedLV1 --size 110GB wdRed
      Logical volume "wdRedLV1" created


And format the logical volume as xfs:

    root@nuc ~ $ mkfs.xfs /dev/wdRed/wdRedLV1
    meta-data=/dev/wdRed/wdRedLV1    isize=256    agcount=4, agsize=7208960 blks
             =                       sectsz=4096  attr=2, projid32bit=1
             =                       crc=0
    data     =                       bsize=4096   blocks=28835840, imaxpct=25
             =                       sunit=0      swidth=0 blks
    naming   =version 2              bsize=4096   ascii-ci=0 ftype=0
    log      =internal log           bsize=4096   blocks=14080, version=2
             =                       sectsz=4096  sunit=1 blks, lazy-count=1
    realtime =none                   extsz=4096   blocks=0, rtextents=0

At this point the logical volume is known to device-mapper:

    root@nuc ~ $ ls -la /dev/mapper/wdRed-wdRedLV1
    lrwxrwxrwx. 1 root root 7 Mar 17 15:50 /dev/mapper/wdRed-wdRedLV1 -> ../dm-5

        
    
## Add the new logical volume to fstab, mounting it by its UUID

xfs_admin conveniently has a -u option to print out the uuid of a device:
    
    root@nuc ~ $ xfs_admin -u /dev/mapper/wdRed-wdRedLV1
    UUID = 2411f8c1-8f07-4c84-8f7b-59e52272f63f

add a line to fstab referencing the UUID:



    root@nuc ~ $ echo \
         "UUID=2411f8c1-8f07-4c84-8f7b-59e52272f63f  /mnt  xfs   defaults  1 3"  \
    >> /etc/fstab

verify it:

    root@nuc ~ $ cat /etc/fstab
    
    #
    # /etc/fstab
    # Created by anaconda on Tue Feb 10 14:13:54 2015
    #
    # Accessible filesystems, by reference, are maintained under '/dev/disk'
    # See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
    #
    /dev/mapper/centos-root /                       xfs     defaults        1 1
    UUID=be517111-d11c-4710-8d5b-1270451ca394 /boot                   xfs     defaults        1 2
    UUID=2190-C30A          /boot/efi               vfat    umask=0077,shortname=winnt 0 0
    /dev/mapper/centos-home /home                   xfs     defaults        1 2
    /dev/mapper/centos-swap swap                    swap    defaults        0 0
    
    UUID=2411f8c1-8f07-4c84-8f7b-59e52272f63f /mnt  xfs   defaults  1 3

Now mount it via fstab as a test:

    root@nuc ~ $ mount -av
    /                        : ignored
    /boot                    : already mounted
    /boot/efi                : already mounted
    /home                    : already mounted
    swap                     : ignored
    mount: /mnt does not contain SELinux labels.
           You just mounted an file system that supports labels which does not
           contain labels, onto an SELinux box. It is likely that confined
           applications will generate AVC messages and not be allowed access to
           this file system.  For more details see restorecon(8) and mount(8).
    /mnt                     : successfully mounted


we'll get to the selinux whining in a second, lets verify it mounted ok:

    root@nuc ~ $ df -h
    Filesystem                  Size  Used Avail Use% Mounted on
    /dev/mapper/centos-root      50G   15G   36G  29% /
    devtmpfs                    7.7G     0  7.7G   0% /dev
    tmpfs                       7.8G  364K  7.8G   1% /dev/shm
    tmpfs                       7.8G   18M  7.7G   1% /run
    tmpfs                       7.8G     0  7.8G   0% /sys/fs/cgroup
    /dev/sdb2                   494M  154M  341M  32% /boot
    /dev/sdb1                   200M  9.6M  191M   5% /boot/efi
    /dev/mapper/centos-home     180G   29G  152G  16% /home
    /dev/mapper/wdRed-wdRedLV1  110G   33M  110G   1% /mnt
    

## Quieting down selinux

selinux needs 'some' context, lets restore the default:

    restorecon -R /mnt
    

unmount then remount, verify selinux is happy now:

    root@nuc ~ $ df -h
    Filesystem                  Size  Used Avail Use% Mounted on
    /dev/mapper/centos-root      50G   15G   36G  29% /
    devtmpfs                    7.7G     0  7.7G   0% /dev
    tmpfs                       7.8G  364K  7.8G   1% /dev/shm
    tmpfs                       7.8G   18M  7.7G   1% /run
    tmpfs                       7.8G     0  7.8G   0% /sys/fs/cgroup
    /dev/sdb2                   494M  154M  341M  32% /boot
    /dev/sdb1                   200M  9.6M  191M   5% /boot/efi
    /dev/mapper/centos-home     180G   29G  152G  16% /home
    /dev/mapper/wdRed-wdRedLV1  110G   33M  110G   1% /mnt 

    root@nuc ~ $ umount /mnt

    root@nuc ~ $ mount -av
    /                        : ignored
    /boot                    : already mounted
    /boot/efi                : already mounted
    /home                    : already mounted
    swap                     : ignored
    /mnt                     : successfully mounted  

