
The debian-12 based raspi uses NetworkManager so the way of seeding the network configuration for wifi is different.   A two step one-time command is needed to set up the box.


## for network manager manually configure wifi

credits:  https://forums.raspberrypi.com/viewtopic.php?p=2150305#p2148962 

```
# create the wpa stanza with the encrypted password
rpdom@raspberrypi:~ $ wpa_passphrase MYSSID MYPASSPHRASE
network={
	ssid="MYSSID"
	#psk="MYPASSPHRASE"
	psk=ENCRYPTED_PSK_IS_HERE
}


# if interactive with keyboard, use that info to create the NetworkManager config file
rpdom@raspberrypi:~ $ sudo nmcli con add con-name MYSSID type wifi ssid MYSSID wifi-sec.key-mgmt wpa-psk wifi-sec.psk ENCRYPTED_PSK_IS_HERE
Connection 'MYSSID' (ed602d46-0a2b-4094-a2c3-79652a47d612) successfully added.
sudo nmcli con up MYSSID

```

## alternate - headless install

Alternately You can later simply seed your boot partition with the appropriate output file(s) for your os.

### wpa_supplicant.conf - for debian-11 raspi os and before
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
	ssid="my first ssid"
	psk="its psk"
}

network={
	ssid="my second ssid"
	psk="its psk"
}
```

### or for debian-12 based raspi os multiple files are needed

#### cmdline.txt - add the options after the 'quiet' word below
be sure to match the image's root=PARTUUID=nnnnnnnn-nn value

```
# 32bit desktop
console=serial0,115200 console=tty1 root=PARTUUID=7550d926-02 rootfstype=ext4 fsck.repair=yes rootwait quiet init=/usr/lib/raspberrypi-sys-mods/firstboot systemd.run=/boot/firstrun.sh systemd.run_success_action=reboot systemd.unit=kernel-command-line.target

# 64bit lite
console=serial0,115200 console=tty1 root=PARTUUID=7788c428-02 rootfstype=ext4 fsck.repair=yes rootwait quiet init=/usr/lib/raspberrypi-sys-mods/firstboot systemd.run=/boot/firstrun.sh systemd.run_success_action=reboot systemd.unit=kernel-command-line.target

```

#### firstrun.sh - this is removed after firstboot automatically

this example sets up the default user, its encrypted password (raspberry, here), and timezone and keyboard.  You can alternately just use the wifi portion to get your pi onto the network and use 'sudo raspi-config' to manually set locale, location, timezone, keyboard, and other options...

```

#!/bin/bash

set +e

FIRSTUSER=`getent passwd 1000 | cut -d: -f1`
FIRSTUSERHOME=`getent passwd 1000 | cut -d: -f6`
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom enable_ssh
else
   systemctl enable ssh
fi
if [ -f /usr/lib/userconf-pi/userconf ]; then
   /usr/lib/userconf-pi/userconf 'pi' '$5$l29xjtROuA$Vm9ZMb7eeEy50HyM0qM6OMGPVEQWzvL0kUtBIEAVUP5'
else
   echo "$FIRSTUSER:"'$5$l29xjtROuA$Vm9ZMb7eeEy50HyM0qM6OMGPVEQWzvL0kUtBIEAVUP5' | chpasswd -e
   if [ "$FIRSTUSER" != "pi" ]; then
      usermod -l "pi" "$FIRSTUSER"
      usermod -m -d "/home/pi" "pi"
      groupmod -n "pi" "$FIRSTUSER"
      if grep -q "^autologin-user=" /etc/lightdm/lightdm.conf ; then
         sed /etc/lightdm/lightdm.conf -i -e "s/^autologin-user=.*/autologin-user=pi/"
      fi
      if [ -f /etc/systemd/system/getty@tty1.service.d/autologin.conf ]; then
         sed /etc/systemd/system/getty@tty1.service.d/autologin.conf -i -e "s/$FIRSTUSER/pi/"
      fi
      if [ -f /etc/sudoers.d/010_pi-nopasswd ]; then
         sed -i "s/^$FIRSTUSER /pi /" /etc/sudoers.d/010_pi-nopasswd
      fi
   fi
fi
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   #/usr/lib/raspberrypi-sys-mods/imager_custom set_wlan 'mysskd' 'mypsk' 'US'
else
cat >/etc/wpa_supplicant/wpa_supplicant.conf <<'WPAEOF'
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
ap_scan=1

update_config=1
network={
	ssid="myssid"
	psk="mypsk"
}

WPAEOF
   chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf
   rfkill unblock wifi
   for filename in /var/lib/systemd/rfkill/*:wlan ; do
       echo 0 > $filename
   done
fi
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom set_keymap 'us'
   /usr/lib/raspberrypi-sys-mods/imager_custom set_timezone 'America/Los_Angeles'
else
   rm -f /etc/localtime
   echo "America/Los_Angeles" >/etc/timezone
   dpkg-reconfigure -f noninteractive tzdata
cat >/etc/default/keyboard <<'KBEOF'
XKBMODEL="pc105"
XKBLAYOUT="us"
XKBVARIANT=""
XKBOPTIONS=""

KBEOF
   dpkg-reconfigure -f noninteractive keyboard-configuration
fi
rm -f /boot/firstrun.sh
sed -i 's| systemd.run.*||g' /boot/cmdline.txt
exit 0

```
