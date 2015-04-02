

# Partition clearing information
    clearpart --all --initlabel --drives=vda

## example: automatic partitioning
    autopart --type=lvm

## example manually partition

    part /boot --fstype=ext4 --size=500
    part pv.01        --grow --size=1
    volgroup vg1 pv.01
    logvol /           --fstype=xfs --name=lv_root   --vgname=vg1 --grow --size=1024 --maxsize=10240
    logvol swap                     --name=lv_swap   --vgname=vg1 --grow --size=6144 --maxsize=6144
    logvol /opt/puppet --fstype=xfs --name=lv_puppet --vgname=vg1 --grow --size=1024 --maxsize=51200


