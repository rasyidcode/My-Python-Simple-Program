### Youtube Trending

Simple command line tool to show what's currently trending on youtube,
there are only 3 commands right now which is :

Command|Description
------------|-------------
trending|Show 50+ trending on youtube in table format
detail|Show individual trending by it's number
watch|Watch the trending video by given number
find|Find trending video by channel name

### Command Help
**base command** : ```py youtube_trending.py --help```
```
Usage: youtube_trending.py [OPTIONS] COMMAND [ARGS]...

  simple program to check youtube current trending

Options:
  --help  Show this message and exit.

Commands:
  detail    Show individual youtube trending by it's number.
  find      Find what's trending.
  trending  Print out the current trending on youtube in table format.
  watch     Watch the trending video by it's number.
```
**detail command** : ```py youtube_trending.py detail --help```
````
Usage: youtube_trending.py detail [OPTIONS]

  Show individual youtube trending by it's number.

Options:
  -n, --number INTEGER  Number of the trending video.
  --help                Show this message and exit.
````
**find command** : ```py youtube_trending.py find --help```
```
Usage: youtube_trending.py find [OPTIONS]

  Find what's trending.

Options:
  -c, --channel TEXT  Channel name to find.
  --help              Show this message and exit.
```
**trending command** : ```py youtube_trending.py trending --help```
```
Usage: youtube_trending.py trending [OPTIONS]

  Print out the current trending on youtube in table format.

Options:
  -l, --limit INTEGER  Limit the trending video shows in the table.
  --help               Show this message and exit.
```
**watch command** : ```py youtube_trending.py watch --help```
```
Usage: youtube_trending.py watch [OPTIONS]

  Watch the trending video by it's number.

Options:
  -n, --number INTEGER  Number of the trending video.
  --help                Show this message and exit.
```
### TODO Next
- [x] Show trending list in table
- [x] Show individual trending video by number
- [x] Watch individual trending video by number
- [x] Find individual trending video by channel name
- [x] Put limit on trending list table
- [ ] Add option on trending command to input --from and --to number
- [ ] Store list data in database
- [ ] Add datetime when this data trending list fetched