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
./post-tracker.py 123456789101111213
```



## TODO:
- [ ] create models to better parsing the data.
- [ ] use dataframes (or another way) to strucure the data.
- [ ] create dmenu (or fzf menu) to save tracking codes in local cache and select in future program's runs.
- [ ] create python telegram bot.
