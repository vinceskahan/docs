#!/usr/bin/python
#
# text mode program to print out a bunch of info from the stats db
# in different ways.  Very similar to what the NOAA reports contain,
# just organized per-category
#
# vince@skahan.net 1/30/2011
#
# FWIW, I call this from a shell script ala:
#
#       export PYTHONPATH=$PYTHONPATH:/home/weewx:/home/weewx/bin
#       python /home/weewx/bin/examples/thisfile.py  /home/weewx/weewx.conf
#

import string
import weeutil.weeutil
import weewx.stats

import sys

if __name__ == '__main__':

    # get the min/max timestamp from the archive
    import weewx.archive
    archive = weewx.archive.Archive('/home/weewx/archive/weewx.sdb')
    myMinStamp = archive.firstGoodStamp()
    myMaxStamp = archive.lastGoodStamp()

    timeSpan = weeutil.weeutil.TimeSpan(myMinStamp,myMaxStamp)

    statsdb = weewx.stats.StatsReadonlyDb('/tmp/stats.sdb')
    spanStats = weewx.stats.TimeSpanStats(statsdb, timeSpan)
       
    # Print maximum temperature for each month in the year:
    print "========================="
    print "outTemp max/min per month"
    print "========================="
    for monthStats in spanStats.months:
        m = monthStats.outTemp.maxtime.format("%Y-%m")
        print "%s : %s %s" % (m,monthStats.outTemp.max,monthStats.outTemp.min)

    print "========================="
    print "outTemp max/min per year"
    print "========================="
    for yearStats in spanStats.years:
        y = yearStats.outTemp.maxtime.format("%Y")
        print "%s : %s %s" % (y,yearStats.outTemp.max,yearStats.outTemp.min)

    print "========================="
    print "rain totals per year"
    print "========================="
    for yearStats in spanStats.years:
        y = yearStats.outTemp.maxtime.format("%Y")
        tot = yearStats.rain.sum
        print "%s: %s" % (y,tot)

    print "========================="
    print "max rain/day in a particular year"
    print "========================="
    for yearStats in spanStats.years:
        y = yearStats.rain.maxsumtime.format("%Y-%m-%d")
        if (y == "   N/A"):
            True
        else:
            tot = yearStats.rain.maxsum
            print "%s: %s" % (y,tot)


    print "========================="
    print "rain totals in a month"
    print "========================="
    for monthStats in spanStats.months:
        m = monthStats.rain.maxtime.format("%Y-%m")
        tot = monthStats.rain.sum
        # my database has no values for rain time
        # so weewx reports maxtime as "   N/A"
        # unfortunately
        if (m == "   N/A"):
            True
        else:
            print "%s : %s " % (m,tot)


