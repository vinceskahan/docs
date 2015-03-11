#adding .ssh/authorized_keys in kickstart

Adding your public key in *ks.cfg* is just a matter of putting the right shell commands in *%post*, being certain to restore the selinux context with *restorecon* if you have selinux enabled and enforcing.

Note - centos7 uses *authorized_keys*, not *authorized_keys2*, in its default *sshd.config*, so be sure to match your server-side ssh configuration.

## Example

```%post

#---- Install our SSH key ----
mkdir -m0700 /root/.ssh/

cat <<EOF >/root/.ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDVmQ5REEZM
nCfznsDgE0ak+oiv1e9sdH6xxGvFhkTlcT7AJonluxPrtskU
8rc2Jhz6MpL6w84xXF8qGswG75V/QYA6qUdFRTtwIur0CgMk
DbCW+OP2v65DX3pwPYnw/Z5Wzl5jJ9gtIsX0HH9W4KKm5030
xxaMFkYBrU67uXATnXeiPUtwO7XjIgnuTotXtdZkLmUi9Pm1
51SglvrWFKRl9zSgp0K10HKK+pDhKewVeJjAp6gRO7kkp8U4
by2+pVeXJlSgx9qevsZ/16DeAizYIas7aTz+X61ICRqS0EAR
pHlm2LXxU4voc4WgIPxKl2MLzDJupqa7IAvbO9WVZFwR vince@VinceAir.local
EOF

### set permissions
chmod 0600 /root/.ssh/authorized_keys

### fix up selinux context
restorecon -R /root/.ssh/

```
