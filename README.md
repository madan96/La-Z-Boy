# La-Z-Boy

The end result of extreme boredom and the sufferings after watching some really low-rated movies on TV.

This script is really helpful when you want to know the the Movies that are to be telecasted on TV 
along with their `"Timing"` and `"IMDb Rating"`, so you never miss out a good watch right when you sit
on your La-Z-Boy.

This project is still under development.

### Usage
-----------------

**Commandline Interface**

```
$ python main.py [channel name]
```
`channel name` : Name of the movie channel

For example,
```
$ python main.py star movies
```
Output:
```
Movie: Dawn of the Planet of the Apes  Time: 21:00 - 23:45  Rating: 7.6
```

And it's done! You have the name of the movie, timings and most importantly, the IMDb rating for the movie
right in front of you on the Terminal.

### Dependencies
-----------------

Install all the dependencies before using this scrapper.
```
pip install BeautifulSoup
pip install mechanize
````


### Features

Currently supported:

- [x] Provides IMDb ratings for movies

**TODOs**:

- [ ] Print output in `Prettytable` format
- [ ] Allow search for Entertainment Channels
- [ ] Provide option to save details as PDF
- [ ] Send notification to the user

### Contribute

Have any suggestions? Please feel free to report as issues/pull requests.
