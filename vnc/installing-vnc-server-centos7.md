# installing vnc server on centos7

installing and enabling VNC is reasonably straightforward in centos7.  
[(howtoforge reference)](https://www.howtoforge.com/vnc-server-installation-on-centos-7)


## install and configure the software

    yum install tightvnc-server
    cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@:2.service
    edit the file, set USER correctly in both places
    
start the daemon
    
    systemctl daemon-reload
    systemctl enable vncserver@:2.service

as the unprivileged user USER above, start it up

    vncserver (it will prompt you for a vncpasswd)
    'netstat -an' will show it listening on port 5902
    then kill the process it started
    
permit VNC traffic into the system

    firewall-cmd --permanent --zone=public --add-service vnc-server
    firewall-cmd --reload
    
at this point, ‘iptables -L -n -v‘ will show 'IN_public_allow' permitting tcp/5901:5903 into the system, so you should be good to go.