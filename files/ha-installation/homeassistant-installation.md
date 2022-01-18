
## Installing Home Assistant Core on top of Raspbian os

### Install HA Core


```
# install home assistant core over Raspbian os
# ref: https://www.home-assistant.io/installation/raspberrypi/#install-home-assistant-core

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-dev python3-venv python3-pip libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf build-essential libopenjp2-7 libtiff5 libturbojpeg0 tzdata
sudo useradd -rm homeassistant
sudo mkdir /srv/homeassistant
sudo chown homeassistant:homeassistant /srv/homeassistant
sudo -u homeassistant -H -s
cd /srv/homeassistant
python3.9 -m venv .
source bin/activate

# install HA within the virtual env
python3 -m pip install wheel
pip3 install homeassistant
hass

# and wait for quite a few minutes....
#   eventually try http://hostname:8123
#   and set the HA username and password
#   then exit

```

### Hook into systemd boot sequence

```
create a new file /etc/systemd/system/home-assistant@homeassistant.service

   #-----------------------------------------
   # ref: https://community.home-assistant.io/t/autostart-using-systemd/199497
   #
   # save as
   # run  'sudo systemctl --system daemon-reload'
   # then 'sudo systemctl start home-assistant@homeassistant'
   # if it is ok, then 'sudo systemctl enable home-assistant@homeassistant'

   [Unit]
   Description=Home Assistant
   After=network-online.target
   [Service]
   Type=simple
   User=%i
   WorkingDirectory=/home/%i/.homeassistant
   ExecStart=/srv/homeassistant/bin/hass -c "/home/%i/.homeassistant"
   
   [Install]
   WantedBy=multi-user.target
   #-----------------------------------------


# start up, check, then enable for subsequent reboots
sudo systemctl --system daemon-reload
sudo systemctl start home-assistant@homeassistant
sudo systemctl status home-assistant@homeassistant
sudo systemctl enable home-assistant@homeassistant

```
