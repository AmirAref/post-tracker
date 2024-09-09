# Post Tracker
Post-Tacker is a command-line tool to get information about parcel's tracking from https://tracking.post.ir.

## Install the program :
install the post-tracker iusing pip :
```bash
pip install post-tracker
```

## Usage
after install, just write `post-tracker` command to access to program :
```bash
# get help
post-tracker -h
# or, pass your tracking code
post-tracker -c 123456789101111213
```


## TODO:
- [x] create models to better parsing the data.
- [x] create dmenu (or fzf menu) to save tracking codes in local cache and select in future program's runs.
- [x] add installer script as a CLI tool in linux machines.
- [x] create [python telegram bot](https://github.com/amiraref/post-tracker-bot).
- [x] make output result prettiy.
- [ ] write README.md in persian
- [ ] publish on pypi.org
- [ ] re-write cli using click library
- [ ] write tests
- [ ] add CI/CD
- [ ] check installed external dependencies : `fzf`
- [ ] make and test compatibily with windows os
