
## Fixing AWS Lightsail ssh access and console access

After an upgrade from Ubuntu 20.04 to 22.04 there were a variety of ssh issues due to openssh version breaking changes.

To keep your old ssh key working, assuming you used ssh-rsa in the past, it needs to be added to the accepted key types. To have the Lightsail browser-based console keep working, you need to add several other key types.

Set the following as your accepted key types in /etc/ssh/sshd_config and restart ssh.

```
# ref: https://askubuntu.com/questions/1409105/ubuntu-22-04-ssh-the-rsa-key-isnt-working-since-upgrading-from-20-04
# ref https://repost.aws/questions/QUro1hmox0SmSG-NJknvJnPQ/lightsail-ssh-rdp-browser-log-in-failed-client-unauthorized-769

PubkeyAcceptedKeyTypes +ssh-rsa,ssh-rsa-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,ssh-ed25519

# you might also need
PubkeyAcceptedAlgorithms +ssh-rsa
```

WARNING - don't lock yourself out.  It is very easy to typo this addition and block 'all' access to your VM.

SUGGESTION - work off a snapshotted clone until you figure it out.  For me my original Lightsail instance 'did' permit my normal ssh access in, but the console access didn't work.   Adding the line above and restarting sshd fixed that and both paths in work now.  Have a failsafe window open and keep that window logged in while working the issue.  There's really no way in if both paths are broken.
