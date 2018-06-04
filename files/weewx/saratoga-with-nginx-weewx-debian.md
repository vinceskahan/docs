# install saratoga templates with nginx and weewx

The php-based saratoga templates have a lot of corequisites.  This documents how to bring them up quickly using nginx as the webserver on a debian system.

---

## install php5-fpm support for nginx

install the packages

    # php support for nginx
    apt-get update
    apt-get install php5-fpm
    
    # added packages needed for saratoga functionality
    apt-get install php5-curl
    apt-get install php5-gd

add a block as follows in /etc/nginx/sites-enabled/weewx

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    location ~ \.php$ {
           fastcgi_split_path_info ^(.+\.php)(/.+)$;
    #       # NOTE: You should have "cgi.fix_pathinfo = 0;" in php.ini
    #
    #       # With php5-cgi alone:
    #       fastcgi_pass 127.0.0.1:9000;
    #       # With php5-fpm:
           fastcgi_pass unix:/var/run/php5-fpm.sock;
           fastcgi_index index.php;
           include fastcgi_params;
    }
create a $HTML_ROOT/phptest.php script

    <?php
    phpinfo();
    ?>

verify php is installed and executing correctly

    service restart nginx
    open http://localhost:/phptest.php in your web browser
            (you should see it executes ok and returns the php configuration)

---

## install saratoga

This section is a streamlined version of the somewhat cryptic [saratoga instructions](http://saratoga-weather.org/wxtemplates/install.php), assuming a default installation using USA base templates. See the saratoga instructions link for more options.

### download the base files, Weather Display plugin, and default icons

    cd /tmp
    wget http://saratoga-weather.org/wxtemplates/Base-USA.zip
    wget http://saratoga-weather.org/wxtemplates/WD-plugin.zip
    wget http://saratoga-weather.org/saratoga-icons.zip
install them:

    mkdir $HTML_ROOT/saratoga
    unzip /tmp/Base-USA.zip
    unzip /tmp/WD-plugin.zip
    unzip /tmp/saratoga-icons.zip
    at this point, you should be able to open http://localhost/saratoga/wxindex.php and see the default saratoga pages

---
## customize your site

    edit your Settings.php to taste
    edit your wxindex.php to taste
    mv wxindex.php index.php to activate your default page
    open http://localhost/saratoga/ and you should see your customized page
And continue to tuning your site to your desired look and feel !!!

### Settings.php

    set SITE['variable'] values for organ, copyr, location, email, latitude, longitude, cityname
    set Site['WDdataMDY']=false, WXSIM=false
    set SITE['variable] values to point to my city, lat/lon, NWSforecasts, noaazone, noaaradar, WUreguin, GR3radar, 
    set SITE['NOAAdir'] to point to the weewx NOAA tree

### Settings-weather.php

    set HistoryStartYear
    set HistoryFilesDir to point to my weewx NOAA tree
    set UV=false
    set SOLAR=false
    set WXsoftwareURL=http://www.weewx.com

### WD-trends-inc.php

I do not have UV nor solar sensors, so I set their variables to false

### flyout-menu.xml

I comment out the WXSIM line to not have the unused menu appear. 
I do not have the rather expensive WXSIM software installed here.

### menubar.php

I add a 'other formats' menu and a few sub-bullets
to crosslink my saratoga site to my other skins (weewx, bootstrap, etc)

### nws-alerts-config.php

edit in the correct location for your site

### wxabout.php

edit in whatever description of your site you'd like

### wxmetar.php

edit in the site(s) you are close to by looking the location
up at http://saratoga-weather.org/wxtemplates/find-metar.php

### wxstatus.php

my Seagate Dockstart reports free memory strangely so I needed to patch this file to add the && ($freememory < 9888) case

    <?php if ( (isset($freememory) && ($freememory < 9888)) ) { ?>
