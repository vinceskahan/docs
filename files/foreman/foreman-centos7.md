
# Installing "The Foreman" under Centos7

Nothing too tricky in this one – follow The Foreman 1.7 [quickstart](http://www.theforeman.org/manuals/1.7/index.html#2.Quickstart) guide section 2


## Install CentOS-7 on the Foreman server

It is simplest to do a server installation with gui, but a minimum server would be good enough:

* set the system up with a static address and a FQDN
* ensure DNS resolution works ok
* run *hostnamectl set-hostname* to ensure the foreman-installer would work (see note below)
* take the reboot at the end, accept terms, normal sequence applies

## Install The Foreman

Follow quickstart section 2.1

```
rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
rpm -ivh http://yum.theforeman.org/releases/1.7/el7/x86_64/foreman-release.rpm
yum install -y git puppet epel-release
yum install -y foreman-installer
foreman-installer
```
 
note: one possible stumbling block is that the server's *‘hostname -f’* must match *‘facter fqdn’* for the foreman installer to succeed. Use *sysctl set-hostname* to fix this issue if it appears.  You might also need to add "192.168.x.x hostname.domainname" in /etc/hosts as a workaround if 'hostname -f' does not resolve.


Transcript should indicate:

* it should have run ok
* foreman should be listening on *http://yourhost.domain*
* it should give you your initial admin account and password
* foreman proxy should be at *http://yourhost.domain:8443*
* puppetmaster should be at port 8140
* full log should be at */var/log/foreman-installer/foreman-installer.log*

##Test the Foreman server

* on the server, connect to *http://localhost* and reset your admin password
* save it in your browser if desired

### Set the server itself as a puppet/foreman client for the *ntp* service

Follow quickstart 2.2 to seed the server’s puppet cert into the foreman data

```puppet agent –test```

####install the puppetlabs ntp module into puppet

    puppet module install -i /etc/puppet/environment/production/modules saz/ntp

#### add the module into a new Puppet class within Foreman
    
in the Foreman gui:

    * go to Configure > Puppet Classes
    * click Import from hostname (top right)
    * verify the newly-added “ntp” is in the puppet class list

next set your hostname (FQDN) to use the ntp class we just updated

    * click on the “ntp” class in the list
    * pick the Smart Class Parameters tab
    * select the server_list parameter on the left
    * Tick the Override checkbox so Foreman manages the “server_list” parameter of the class
    * change the default value if desired
    * submit the page to apply the class to the host

at this point you should see:
    
    * the run succeeded in the foreman gui
    * the /etc/ntp.conf file should have a comment in it saying ‘managed by puppet’.

to re-verify

    * alter ntp.conf manually
    * run ‘puppet agent –test’ again
    * re-verify it put the content back to the puppet-managed content of the file

