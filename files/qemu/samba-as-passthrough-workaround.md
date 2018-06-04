# Samba as a workaround for no qemu-kvm passthrough

Unfortunately, centos7 does not support device passthrough, making installing software from physical media 'within' a VM somewhat painful.  This documents how to use a samba export of the DVD mountpoint as one possible workaround

## Install samba

Nothing too special here, install the rpms, set the firewall, enable and start the services

    yum install samba samba-client samba-common
    firewall-cmd --permanent --zone=public --add-service=samba
    firewall-cmd --reload
    systemctl enable smb.service
    systemctl enable nmb.service
    systemctl start smb.service
    systemctl start nmb.service

### Edit /etc/samba/smb.conf

Simplest configuration to create for a Windows client is to ensure that your workgroup on the client side matches the workgroup on the samba server.  This example just shares the /media/cdrom directory that we will mount the DVD to as needed.

    [global]
       workgroup = WORKGROUP
       server string = Samba Server Version %v
       hosts allow = 127. 192.168.0.
       log file = /var/log/samba/log.%m
       max log size = 50
       security = user
       passdb backend = tdbsam
       map to guest = Bad User
       security = user
    [dvd]
       comment = DVD drive on the host
       path = /media/cdrom
       guest ok = Yes
       read only = yes
       browsable = yes

## Test your configuration

testparm should return the following:

    root@nuc $ testparm
    Load smb config files from /etc/samba/smb.conf
    rlimit_max: increasing rlimit_max (1024) to minimum Windows limit (16384)
    Processing section "[dvd]"
    Loaded services file OK.
    Server role: ROLE_STANDALONE
    Press enter to see a dump of your service definitions
    
    [global]
    	server string = Samba Server Version %v
    	map to guest = Bad User
    	log file = /var/log/samba/log.%m
    	max log size = 50
    	idmap config * : backend = tdb
    	hosts allow = 127., 192.168.0.
    
    [dvd]
    	comment = DVD drive on the host
    	path = /media/cdrom
    	guest ok = Yes

## Configure selinux

Default selinux policy will block the client from seeing anything you export unless you configure selinux to permit a more traditional access control mechanism simply according to the settings in /etc/samba/smb.conf

### get selinux out of the way
`setsebool -P samba_export_all_rw 1`

This is explained further in the [RHEL Documentation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Managing_Confined_Services/sect-Managing_Confined_Services-Samba-Booleans.html).

    samba_export_all_rw
    Export any file or directory, allowing read and write permissions.
    This allows files and directories that are not labeled with the samba_share_t
    type to be exported through Samba. Permissions in /etc/samba/smb.conf and
    Linux permissions must be configured to allow write access.
    
## navigate to the share on the client

At this point, you should be able to navigate to the Samba shared DVD contents on the client VM and install your software to the client.

## unmounting the DVD from the server

Windows seems to have some keepalives set, so to unmount the DVD from the server, you might need to manually detach from it on the client side. Knowing a little old-1985-vintage MS-DOS command-line helps.

(on the client open a command window)

#### view the network resources the client is using
`net use
`
#### detach from it manually
`net use \\hostname\resourcename /d`

At this point you should be able to unmount the DVD from the host.
