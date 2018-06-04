
# unattended(ish) zoneminder setup over minimal debian-7.8 image

This is a quick howto for installing and configuring zoneminder on top of a minimal debian image

(note - this is old, and restoring this reference db backup will 'likely' not work unattended on a modern version of the database software.   My recollection is that the restore fails unattended.  Manually running the steps did the right thing with prompting when last tried (circa 2016)).

 
## update the apt cache

    apt-get update


## preseed the prompts for mysql root password


Unfortunately this requires you to know which precise version identifier you will be using, which (to me) is a major debian annoyance.   If you are instead prompted for the mysql user/pass combination, enter your desired values.

    # note - this sets the mysql password to 'root' which you probably want to not do.
    mysqlpass=root
    export DEBIAN_FRONTEND=noninteractive
    debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password '$mysqlpass''
    debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password '$mysqlpass''
    apt-get install -y mysql-server
    
install zoneminder itself and hook it into the apache web

    apt-get install -y zoneminder
    ln -s /etc/zm/apache.conf /etc/apache2/sites-enabled/001-zm
    service apache2 restart


fix dns up to point at our local dnsmasq server

    echo "nameserver 192.168.0.138">/etc/resolv.conf

## restore a skeletal zoneminder database dump from a known good system

This in general comes from configuring a clean system with your desired Monitor(s), Zone(s), and Filter(s) and dumping the database with *mysqldump -uroot -pPASSHERE zm > zm.dump* and then gzipping for size if needed.

Transfer the file to your target system via ssh so it's there to unzip and restore to quickly define everything for your new system.

    scp zm:/root/zm.dump.gz .


## then restore the database dump and restart zoneminder

Of course, use the user/pass combination you set above

    gunzip zm.dump.gz
    mysql -uroot -proot zm < zm.dump
    rm zm.dump
    service zoneminder restart

## test your new installation

    open http://x.x.x.x/zm in a browser and verify the database load worked
    
    verify you can view your camera in realtime, by clicking its name
    
    trigger an event, verify the event is detected and saved and viewable

