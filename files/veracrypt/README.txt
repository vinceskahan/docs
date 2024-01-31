Veracrypt howto for deb12 vm
 - this is a truecrypt fork with a cli version that works on linux still

wget https://launchpad.net/veracrypt/trunk/1.25.9/+download/veracrypt-console-1.25.9-Debian-11-amd64.deb
sudo apt install ./veracrypt-console-1.25.9-Debian-11-amd64.deb

mkdir -p /mnt/mymountpoint
veracrypt -tc --verbose --text --mount encrypted_filename /mnt/mymountpoint

#----------------------------------------------------------------------------
# note the -tc option above which is needed for truecrypt legacy volumes
# this worked for me 2024-0130 mounting trucrypt volumes built 2013-1213
# once I remembered which password the file was encrypted with :-)
#----------------------------------------------------------------------------


