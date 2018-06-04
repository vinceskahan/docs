
# virt-install command for a puppetmaster vm

 * bridge it out to the local LAN
 * one virtual cpu
 * use the 'spinning' virt-pool, disk in raw format, 100GB
 * no graphics
 * inject a kickstart config into the top of the initrd
 * enable serial console, and kickstart off that (internal) toplevel config
 * from a iso image mounted locally on the host
 * and specify the qemu-kvm domain name



		  virt-install  --network bridge=br0  --ram=6144  --vcpus=1  \
		      --disk pool=spinning,format=raw,size=100  --graphics none  \
		      --initrd-inject=/var/www/html/ks-puppet.cfg  \
		      --extra-args="console=tty0 console=ttyS0,115200 ks=file:/ks-puppet.cfg"  \
		      --location=/iso/CentOS-7.0-1406-x86_64-DVD/CentOS-7.0-1406-x86_64-DVD.iso  \
		      --name puppet

