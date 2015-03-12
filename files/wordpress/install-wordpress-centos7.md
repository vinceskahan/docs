# Installing WordPress on CentOS-7

Installing WordPress on CentOS-7 is straightforward thanks to a couple of great howto posts on [installing the LAMP stack](http://www.unixmen.com/install-lamp-server-apache-mariadb-php-centosrhelscientific-linux-7/) and then [installing Word Press itself](http://www.unixmen.com/install-configure-wordpress-4-0-benny-centos-7/) on CentOS-7, which are essentially replicated here just in case the upstream sites disappear someday.




## 1. Install LAMP Stack

### install
    yum install -y httpd
    systemctl start httpd
    systemctl enable httpd
    firewall-cmd --permanent --add-service=http
    systemctl restart firewalld

### verify apache works
    connect to http://x.x.x.x and see test page



## 2. Install MariaDB

### install
    yum install -y mariadb-server mariadb
    systemctl start mariadb
    systemctl enable mariadb

### configure
    mysql_secure_installation
     - hit 'return' at the first root password prompt (you don't have one yet)
     - hit 'Y' for everything to install the most secure setup
     - enter your desired mariadb root password



## 3. Install PHP

### install
    yum install -y php php-mysql php-gd php-pear

### test
create a /var/www/phpinfo.php file containing:

        <?php
        phpinfo(); 
        ?>

restart apache

        sysctl restart http

verify php is being interpreted

    open http://x.x.x.x/phpinfo.php
 

## 4. Install phpMyAdmin (optional)

– I skipped this part


## 5. Install WordPress

### get and install into web document root
    wget http://WordPress.org/latest.zip
    unzip latest.zip
    cp -R wordpress/. /var/www/html

### keep selinux out of the way
I did not get 403 errors, so I skipped these next steps

    setsebool -P httpd_enable_homedirs true
    chcon -R -t httpd_sys_content_t /var/www/html
    
### Set up WordPress database
these examples create a 'wpdb' database with 'wpuser' account having 'centos' password

    mysql -u root -p
    MariaDB [(none)]> create database wpdb;
    Query OK, 1 row affected (0.00 sec)
        
    MariaDB [(none)]> GRANT ALL ON wpdb.* TO wpuser@localhost IDENTIFIED BY 'centos';
    Query OK, 0 rows affected (0.03 sec)
        
    MariaDB [(none)]> flush privileges;
    Query OK, 0 rows affected (0.01 sec)
        
    MariaDB [(none)]> exit
    Bye

## 6. Configure WordPress

### put the sample WordPress config.php into place
    cp /var/www/html/wp-config-sample.php /var/www/html/wp-config.php

### edit it
    match your values above for DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

### Install WordPress itself

    * open http://x.x.x.x/ and see the WordPress welcome page
    * enter your site name/username/password/email
    * click 'Install WordPress', see the Success! page
    * click 'Log In' and see the WordPress dashboard

at this point WordPress is ready for you to create content

## About permissions

You need HTML_ROOT/wp-content with group apache:apache to have plugins/themes installable within the wordpress administrative gui. If you get a prompt for ftp user/pass, that is the problem. Mine are mode 775 currently, but it’s unclear what the most restrictive permissions that would work actually are.