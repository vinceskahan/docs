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

----
----

## Enable Lightsail ipv6

### Enable it in the VM
In the Lightsail console for your VM, simply enable ipv6.  The console will display your persistent ipv6 address which will remain valid as long as you leave ipv6 enabled

### Check your ipv6 packet filters
Likely add a ICMP ping rule to the ipv6 ruleset to enable ping6 to work

### Again, ping6 your ipv6 address from another host


## Optionally - update DNS
Add a AAAA record for your how so DNS lookups work


----
----

## Diffs in opnsense configs with ipv4-only vs. ipv6-enabled


```
--- ipv4-lan-config-OPNsense.localdomain-20230801091913.xml	2023-08-01 09:19:16
+++ ipv6-lan-enabled-config-OPNsense.localdomain-20230801091347.xml	2023-08-01 09:13:55
@@ -388,6 +388,10 @@
       <spoofmac/>
       <ipaddr>192.168.1.1</ipaddr>
       <subnet>24</subnet>
+      <ipaddrv6>track6</ipaddrv6>
+      <track6-interface>wan</track6-interface>
+      <track6-prefix-id>0</track6-prefix-id>
+      <dhcpd6track6allowoverride>1</dhcpd6track6allowoverride>
     </lan>
     <lo0>
       <internal_dynamic>1</internal_dynamic>
@@ -1100,8 +1104,8 @@
   </widgets>
   <revision>
     <username>vince@192.168.1.51</username>
-    <time>1690906728.8854</time>
-    <description>/interfaces.php made changes</description>
+    <time>1690906266.5845</time>
+    <description>/services_router_advertisements.php made changes</description>
   </revision>
   <OPNsense>
     <Firewall>
@@ -1614,7 +1618,7 @@
   </wireless>
   <dhcpdv6>
     <lan>
-      <ramode>disabled</ramode>
+      <ramode>assist</ramode>
       <rapriority>medium</rapriority>
       <ramininterval>200</ramininterval>
       <ramaxinterval>600</ramaxinterval>
```
