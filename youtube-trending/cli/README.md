# Youtube Trending CLI Application

Simple command line tool to show what's currently trending on youtube,
built-in using click module that helps to simplify createing cli application
there are only 4 commands right now which is :

Command|Description
------------|-------------
trending|Show 50+ trending on youtube in table format
detail|Show individual trending by it's number
watch|Watch the trending video by given number
find|Find trending video by channel name

### Example Command

Do | Command | Description
---|---------|------------------------------------------------
get all trending list| ```py youtube_trending.py trending``` | Will return list of all trending video in table format
get only 5 trending list| ```py youtube_trending.py trending --limit 5``` | Will return list of 5 trending video in table format
get trending detail by trending number| ```py youtube_trending.py detail --number 5``` | will return the detail of inserted number that user input
watch a trending video by it's number| ```py youtube_trending.py watch --number 5``` | will open your default browser and play the video
find a trending video by channel name | ```py youtube_trending.py find --channel "PewDiePie"``` | will return the detail of related channel

### TODO Next
- [x] Show trending list in table
- [x] Show individual trending video by number
- [x] Watch individual trending video by number
- [x] Find individual trending video by channel name
- [x] Put limit on trending list table
- [ ] Add option on trending command to input --from and --to number
- [ ] Store list data in database
- [ ] Add datetime when this data trending list fetched
- [x] Separete ytrending core and click cli-app
- [x] Views should return an integer
<!-- - [ ] Uploaded should return a date -->
- [ ] Create command to generate the list into json file
- [ ] Put cron on this app
- [ ] Upload the data to spreadsheet everyday at 9 a clock
