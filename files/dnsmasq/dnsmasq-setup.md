
# dnsmasq setup for home

dnsmasq is pretty slick, lets you easily run a quick dns server that reads files ala /etc/hosts, yet serves as a nice efficient caching nameserver for remote lookups (and has many other nice features).


## centos7.1 setup

Centos7.1 out of the box is set up with reasonable defaults, you just need to minimally configure it and enable/start the services

### configuring the server
Create a file /etc/dnsmasq.d/main.conf containing the following:

    # ignore resolv.conf
    no-resolv
    
    # use google servers for internet lookups
    server=8.8.8.8
    server=8.8.4.4
    
    # define our localdomain, answers for this domain will
    #   come from /etc/hosts or static hosts files
    local=/local/
    auth-zone=/local/
    
    # don't require FQDN for local domain hostnames
    expand-hosts
    
    # in addition to entries in /etc/hosts
    # read in all the files in this directory for hosts
    # entries.  All such files should be in /etc/hosts format
    addn-hosts=/etc/dnsmasq.d/static
    

### enabling and starting the service

    systemctl enable dnsmasq.service
    systemctl start  dnsmasq.service

### adding/editing a host

    # create a one-liner file in /etc/dnsmasq.d/static
    # with content ala a host file entry for that host
    echo "192.168.0.123 foo.local foo" > /etc/dnsmasq.d/static/foo
    
    # then sighup the dnsmasq process
    systemctl kill -s HUP dnsmasq.service
    
    # at this point you should be able to resolv 'foo'
    dig foo


