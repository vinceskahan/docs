# backfilling stats database

Weewx v3 has a more complicated database architecture in which there are a large number of statistics tables (along with the traditional archive table) in the weewx.sdb file.

To do a v2=>v3 conversion, or to regenerate the stats after doing major surgery on your archive data, the command to do so in the foreground is:

    cd /home/weewx
    bin/wee_config_database weewx.conf --backfill-daily

The benefit of doing so in the foreground is that you can watch progress interactively, which can take a while if you have a lot of data and a slow computer.

Backfilling 712,000 records (8+ years) takes:

* 4800 seconds on a Seagate Dockstar (128 MB ram first-generation Pogoplug)
* 180 seconds on a modern i5 Intel NUC with 16 GB ram and centos7, running weewx under debian in a Docker container
* 200 seconds on a fall-2011 Macbook Air (4GB ram) in a 1GB boot2docker VM running a Docker container