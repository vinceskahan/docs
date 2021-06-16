
## Downloading all your repos via the Github CLI 'gh' command

```
# install the Github CLI 'gh' and prerequisites
# brew install jq gh

# run gh once to set up your auth
# gh auth login

# this helps as I have 2FA set and need
# to ok this api access via my yubikey

gh repo list --json name --limit 100 | jq '.[].name' | xargs -n1 gh repo clone

# if you want to log out afterward
#   gh auth logout

# gh saves your config in ~/.config/gh/ including your token
# so be sure to ensure there's no world read

```


---
---
---


## older answer - doesn't with for private repos
This excellent script came from https://stackoverflow.com/a/32833411/3285738
which is an answer to [a question](https://stackoverflow.com/questions/19576742/how-to-clone-all-repos-at-once-from-github?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa) regarding how to do this exact task.

The only thing I can think of that might help for keeping a local editable copy of the repos would be a step to change your 'git remote' for each repo to your desired setting.   Works great on my Macbook Air as of June 2018.

Answer copied verbatim here just in case the Stack Overflow link somehow disappears.

### from the SO answer link above...

On Windows and all UNIX/LINUX systems, using Git Bash or any other Terminal, replace YOURUSERNAME by your username and use:

```
CNTX={users|orgs}; NAME={username|orgname}; PAGE=1
curl "https://api.github.com/$CNTX/$NAME/repos?page=$PAGE&per_page=100" |
  grep -e 'git_url*' |
  cut -d \" -f 4 |
  xargs -L1 git clone
```

Set CNTX=users and NAME=yourusername, to download all your repositories. Set CNTX=orgs and NAME=yourorgname, to download all repositories of your organisation.

The maximum page-size is 100, so you have to call this several times with the right page number to get all your repositories (set PAGE to the desired page number you want to download).

(question answered Sep 28 '15 at 23:36 by user Erdinc Ay)

```

