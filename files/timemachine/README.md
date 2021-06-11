## Mac Time Machine

Initial setup of a new time machine backup disk takes seemingly forever after the first backup to reach the state where the disk is encrypted.  Here are some gory details.


### To check your encryption status

This is a SSD that is not quite through encryption after many hours....

```
$ diskutil cs list
CoreStorage logical volume groups (1 found)
|
+-- Logical Volume Group DD6A920A-899F-4DFB-9EC2-1AAD4153D89C
    =========================================================
    Name:         Time Machine Backup SSD 1
    Status:       Online
    Size:         249715376128 B (249.7 GB)
    Free Space:   18890752 B (18.9 MB)
    |
    +-< Physical Volume 67F1A033-2C59-4BC5-A00F-31A3AE7FE4E7
    |   ----------------------------------------------------
    |   Index:    0
    |   Disk:     disk2s2
    |   Status:   Online
    |   Size:     249715376128 B (249.7 GB)
    |
    +-> Logical Volume Family 9B778F8F-AA0E-4D30-B9BD-E466BDD251F5
        ----------------------------------------------------------
        Encryption Type:         AES-XTS
        Encryption Status:       Unlocked
        Conversion Status:       Converting (forward)
        High Level Queries:      Not Fully Secure
        |                        Passphrase Required
        |                        Accepts New Users
        |                        Has Visible Users
        |                        Has Volume Key
        |
        +-> Logical Volume 5C2678FC-47C8-498A-8C9C-6B1D80A07AF4
            ---------------------------------------------------
            Disk:                  disk3
            Status:                Online
            Size (Total):          249344163840 B (249.3 GB)
            Conversion Progress:   91%
            Revertible:            Yes (unlock and decryption required)
            LV Name:               Time Machine Backup SSD 1
            Volume Name:           Time Machine Backup SSD 1
            Content Hint:          Apple_HFS
```

This is what it looks like when complete

```
$ diskutil cs list
CoreStorage logical volume groups (2 found)
|
+-- Logical Volume Group DD6A920A-899F-4DFB-9EC2-1AAD4153D89C
|   =========================================================
|   Name:         Time Machine Backup SSD 1
|   Status:       Online
|   Size:         249715376128 B (249.7 GB)
|   Free Space:   18890752 B (18.9 MB)
|   |
|   +-< Physical Volume 67F1A033-2C59-4BC5-A00F-31A3AE7FE4E7
|   |   ----------------------------------------------------
|   |   Index:    0
|   |   Disk:     disk2s2
|   |   Status:   Online
|   |   Size:     249715376128 B (249.7 GB)
|   |
|   +-> Logical Volume Family 9B778F8F-AA0E-4D30-B9BD-E466BDD251F5
|       ----------------------------------------------------------
|       Encryption Type:         AES-XTS
|       Encryption Status:       Unlocked
|       Conversion Status:       Complete
|       High Level Queries:      Fully Secure
|       |                        Passphrase Required
|       |                        Accepts New Users
|       |                        Has Visible Users
|       |                        Has Volume Key
|       |
|       +-> Logical Volume 5C2678FC-47C8-498A-8C9C-6B1D80A07AF4
|           ---------------------------------------------------
|           Disk:                  disk3
|           Status:                Online
|           Size (Total):          249344163840 B (249.3 GB)
|           Conversion Progress:   Complete
|           Revertible:            Yes (unlock and decryption required)
|           LV Name:               Time Machine Backup SSD 1
|           Volume Name:           Time Machine Backup SSD 1
|           Content Hint:          Apple_HFS
|
```

### Speeding up the encryption step

You can 'temporarily' set it to grab whatever resources it can, although this will back out other things and your fan will likely spin up to max in a few minutes.

```
sudo sysctl debug.lowpri_throttle_enabled=0
```

IMPORTANT - remember to set it back to throttled afterward !!!!

```
sudo sysctl debug.lowpri_throttle_enabled=1
```

### A better way to quicken the first backup

Simply format the disk as encrypted in Disk Utility 'before' running Time Machine.   Formatting/encrypting in Disk Utility is 'very' fast especially since you're essentially encrypting all zeroes that way.

