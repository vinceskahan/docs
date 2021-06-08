### static address reservation in dhcp on raspbian

```

#--------------------------------------
# this is /etc/dhcpd.conf on raspbian
# (example from pi3)
#--------------------------------------
hostname
clientid
persistent
option rapid_commit
option domain_name_servers, domain_name, domain_search, host_name
option classless_static_routes
option interface_mtu
require dhcp_server_identifier
slaac private
interface eth0
        static ip_address=192.168.1.24/24
        static routers=192.168.1.1
        static domain_name_servers=8.8.8.8 8.8.4.4

```
