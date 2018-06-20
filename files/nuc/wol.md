## wake on lan for the NUC

My Intel NUC supports WOL - too cool !

### download a mac cli client

see https://www.depicus.com/wake-on-lan/wake-on-lan-for-apple-mac

### try it out

substitute in the mac address and ip address of the NUC below

```
./wolcmd c03fd1234567 192.168.1.21 255.255.255.0 4343
```

### notes

My NUC conveniently comes up booting off of whatever the last selected boot media was (if you have picked something other than the saved default).   This means that if you have manually selected a different boot disk and the system hasn't lost power completely, it will use that last selection.  Works great.


