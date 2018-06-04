
Setting timezones is ugly. There are many ways to do it non-interactively.

## systemd

```
# systemd is taking over the world step by step, inch by inch...
TIMEZONE="US/Pacific-New"
sudo timedatectl set-timezone ${TIMEZONE}
```

## old school debian

```
TIMEZONE="US/Pacific"
rm -f /etc/timezone  2>/dev/null
rm -f /etc/localtime 2>/dev/null
echo $TIMEZONE > /etc/timezone
dpkg-reconfigure --frontend noninteractive tzdata
```


# old school centos7

```
# (if no systemd installed ala if you're in a docker container)
TIMEZONE="US/Pacific"
rm -f /etc/localtime
ln -s /usr/share/zoneinfo/${TIMEZONE} /etc/localtime
```

