## Enabling ipv6 for an opnsense LAN and Lightsail VM

To enable ipv6 with Opnsense consult their docs.  Here is a quick list of what I changed to make it work here.

### Verify the opnsense box has ipv6 enabled for itself

ssh into the opnsense box, run "ping6 google.com" and see if it works


### Enable ipv6 locally on your LAN network

#### enable ipv6 on the interface
* in Interfaces:[LAN] check 'manual configuration'
* in Interfaces:[LAN] set ipv6 configuration to 'Track Interface'

#### ensure ipv6 routes
* in Services:RouteAdvertisements:[LAN] set RouterAdvertisements = Assisted

### Try again to 'ping6 google.com'

## Enable Lightsail ipv6

### Enable it in the VM
In the Lightsail console for your VM, simply enable ipv6.  The console will display your persistent ipv6 address which will remain valid as long as you leave ipv6 enabled

### Check your ipv6 packet filters
Likely add a ICMP ping rule to the ipv6 ruleset to enable ping6 to work

### Again, ping6 your ipv6 address from another host


## Optionally - update DNS
Add a AAAA record for your how so DNS lookups work






