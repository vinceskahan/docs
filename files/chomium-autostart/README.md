
## chromium autostart on a pi

Put this in /etc/xdg/lxsession/LXDE-pi/autostart

```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash

# or use --kiosk
/usr/bin/chromium-browser --start-fullscreen http://192.168.1.171:8123/local/tileboard/index.html
```
