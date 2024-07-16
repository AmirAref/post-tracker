# Post Tracker

## Run the program
1. first, **clone** this repository and then go to the project directory.

2. after you cloned the repository, you have to install the **dependencies**, you need to have installed the [poetry](https://python-poetry.org/) dependency manager in your machine, then run the following command :
```bash
poetry install
```
3. run the program :
```bash
./post-tracker.py -h
# or, pass your tracking code
./post-tracker.py -c 123456789101111213
```



## TODO:
- [x] create models to better parsing the data.
- [x] create dmenu (or fzf menu) to save tracking codes in local cache and select in future program's runs.
- [x] add installer script as a CLI tool in linux machines.
- [x] create [python telegram bot](https://github.com/amiraref/post-tracker-bot).
- [ ] re-write cli using click library
- [ ] check installed external dependencies : `fzf`
- [ ] make and test compatibily with windows os
- [ ] make output result prettiy.
- [ ] write README.md in persian
- [ ] write tests
- [ ] publish on pypi.org
- [ ] add CI/CD
