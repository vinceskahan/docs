# puppet master and first client setup on Debian Wheezy

This documents the minimum steps to install puppet on a debian master and client system, including some items omitted from the official docs.


## Install and configure the Puppet Master System

### os – install a minimal system

do a netinst image installation, select 1GB RAM, 8GB disk
for packages, just pick ‘ssh server’ and ‘base’
after reboot, set the system to be a static ip address with appropriate DNS settings

    (in /etc/resolv.conf)
    search=local.
    domain=local.
    
    (in /etc/network/interfaces)
    auto eth0
    iface eth0 inet static
    address 192.168.0.178
    netmask 255.255.255.0
    gateway 192.168.0.1

### install puppetmaster software
    
    wget https://apt.puppetlabs.com/puppetlabs-release-wheezy.deb
    dpkg -i puppetlabs-release-wheezy.deb
    apt-get update
    apt-get install puppetmaster-passenger

### do postinstall tasks

    # not documented on Puppetlabs site
     service apache stop
     
    # configure the minimal settings
    # in /etc/puppet/puppet.conf [master] section
    ca=true
    dns_alt_names=puppetmaster.local,puppetmaster,puppet.local,puppet
    
    # create the master's cert
    # (hit ^C when you see the Starting message)
    puppet master --verbose --no-daemonize
   
    # not documented on Puppetlabs site
    service apache2 start


## Install and configure the Puppet Client system

### os – install a minimal system

    follow the same ‘install a minimal system’ procedure as for the master
    
    add ip address for your master as hostname ’’puppet“ and ”puppet.local" in /etc/hosts
    so the name resolves to an address

### install puppet client software

    wget https://apt.puppetlabs.com/puppetlabs-release-wheezy.deb
    dpkg -i puppetlabs-release-wheezy.deb
    apt-get update
    apt-get install puppet
    
    # set puppet agent to start on boot
    edit /etc/default/puppet and set START=yes
    
    # start the puppet agent manually, using puppet itself
    puppet resource service puppet ensure=running enable=true


## Enable the client to be managed by the master

On the Master, sign the client’s cert request

    # get the cert request list
    puppet cert list
    
    # client cert request should be in the list similar to:
    client.local" (SHA256) 51:DB:8E:9F:76:5B:32:3A:AB:E2:03:E2:BD:21:5D:CE:FB:A4:47:DE:8E:6A:0F:6F:38:3B:EB:2D:22:DF:7D:4B
    
    # sign the client’s request
    puppet cert sign client.local
     or
    puppet cert sign --all

at this point, you can Classify the Node per the 
Puppetlabs instructions and start managing the client node with your puppet definitions

## Note: puppet deprecation warnings

on a debian system, you will see lots of whining ala:

    Warning: Setting templatedir is deprecated.
    See http://links.puppetlabs.com/env-settings-deprecations
     (at /usr/lib/ruby/vendor_ruby/puppet/settings.rb:1139:in `issue_deprecation_warning')

The workaround is to manually comment out the templatedir entry in */etc/puppet/puppet.conf*– see [PUP-2566](https://tickets.puppetlabs.com/browse/PUP–2566) for details
