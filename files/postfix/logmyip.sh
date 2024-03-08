#!/bin/bash
#
# check your external ip, saving it to a file and emailing a recipient as needed
# see the main.cf for postfix for details
#
# tested on raspios based on debian 11.8
#

RECIPIENT="myname@here.com"
IPFILE="/home/pi/myip.txt"

# this looks for a timestamp ala yyyymmdd.hhmm then the whatsmyip outside address of the LAN
OLDIP=`tail -n 1 ${IPFILE} | awk '{print $2}'`

NOW=`date +%Y%m%d.%H%m`
MYIP=`curl https://ipinfo.io/ip -s`

if [ "x${OLDIP}" = "x${MYIP}" ]
then
	logger -t "[MYIP]" "ip unchanged - ${MYIP}"
	echo "no changes needed...still ${MYIP}"  | mail -s "home ip unchanged today" ${RECIPIENT}
	echo "$NOW ${MYIP}" >> ${IPFILE}
else
	logger -t "[MYIP]" "IP HAS CHANGED FROM ${OLDIP} to ${MYIP}"
	echo "update lightsail ssh rules..."  | mail -s "home ip has CHANGED from ${OLDIP} to ${MYIP}" ${RECIPIENT}
	echo "${NOW} ${MYIP}" >> ~/myip.txt
fi

