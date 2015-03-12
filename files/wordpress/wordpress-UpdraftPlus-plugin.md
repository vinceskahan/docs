# Configuring UpdraftPlus – Backup/Restore plugin


Putting data ‘into’ a WordPress database without a way to ensure I can’t lose data if a disk crash etc. happens isn’t a great plan, so I needed to work the backup/restore scenario.

This plugin has > 1.5M downloads, and almost universally 5-star reviews, so I gave it a try.

# permissions issues preventing one-click installation

Painful process due (I think) to the permissions of the wp-content document root for apache vs. the user/group my web login into WordPress’s admin interface resolves to on the server side.

Could not successfully use the WP gui to install it, as it kept asking me for FTP credentials (ugh), and of course FTP is not installed here, and the system is sufficiently firewalled from Internet so it wouldn’t matter anyway.

Right-clicked to download it, and failed to upload to the WP computer due to it being over the 2M max upload size in php.ini – updated that to 5M and restarted apache, and it uploaded to /var/www/html/wp-content/uploads/YYYY/MM/filename.zip this time, but I could not get it to install via the gui.

### low-tech workaround
Low-tech’d it and simply did a unzip of the file while in the /var/www/html/wp-content/plugins directory, at which time the WP admin interface let me activate/enable/run the plugin ok.

### later found the likely solution
It was indeed permissions - the web server (apache) did not have permissions to write into the wp-content/plugins directory under the web root.

# centos systemd 'feature'
lastly – CentOS-7 has a strange ‘feature’ where if I configure the plugin to backup to /tmp/wordpress-backups, the files are actually put in /tmp/systemd-private-SOME_ID_HERE/tmp/wordpress-backups and owner/group=apache. – just beyond ugly. 

What is going on seems to be similar to the issue reported on [here](http://help.directadmin.com/item.php?id=561).