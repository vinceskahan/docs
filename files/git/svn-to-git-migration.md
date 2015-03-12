# migrating from svn to git


Volunteered to do the sourceforge (svn) to github (git) migration of the 5+ years and 2900+ checkins of weewx.  Interesting finding so many old howtos that either didn’t work or were error-laden.

This documents how it was done…


## Goals

Goals were simply to move from svn=>git and maintain all the old history, including all checkins, logs, branches, and tags.

## Creating the ‘authors’ file

Started with Scott Chacon’s [instructions](http://git-scm.com/book/en/v2/Git-and-Other-Systems-Migrating-to-Git) and created an authors file with the names of everybody who had checked in during the weewx history and ran the following command:

```
svn log --xml | grep author | sort -u | perl -pe 's/.*>(.*?)<.*/$1 = /'
```
and then manually edited the output into a minimal acceptable format ala:
```
userxyz = User Xyz <userxyz> 
userabc = User Abc <userabc>
```

I was uncertain if folks wanted their email addresses exposed on github, so I just used the username (not fully qualified) that their checkins used in svn historically.

## Importing svn=>git

The normal ‘git svn clone’ command was both deathly slow (sourceforge bouncing, I think) and generated very incomplete output.

After a number of attempts, I gave up and used a different tool that worked far better.  Fortunately weewx had a very traditional svn structure, so I didn’t need to add any optional parameters.

    # install the gem
    gem install svn2git --source http://gemcutter.org
    # run it
    svn2git svn://svn.code.sf.net/p/weewx/code --authors /root/weewx-import/authors --verbose

The result was a good git repo, with ‘all’ the tags and branches correctly imported from svn as expected.

## git cleanup

The resulting tree had ‘many’ old branches that had never been deleted, as well as some dangling branches with unmerged checkins. Cleanup was relatively straightforward, generally I used ‘*gitk –all’* to quickly surf the checkins visually to speed up things.

1. deleted any branches that had been fully merged
2. deleted any branches that had a tag at the last unmerged checkin
3. added a tag at the end of each branch with unmerged checkins, and 'then' deleted the branch

Result was what was hoped for – a clean git tree with just active branches on it, and tags for all past releases and unmerged branches that had names good enough to figure out what was on them (for someday in the distant future perhaps).

## Import into github

Simply created the repo in github, set the remote per the instructions, and did a ‘*git push*’ and it imported quickly and successfully.
