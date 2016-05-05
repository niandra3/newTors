import bs4
import configparser
import json
import os
import re
import urllib.request
import webbrowser

# Load config file (keep in same directory as this file)
cwd = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(cwd, 'config.ini'))

# Load data from data.json with all favorite shows (see EpisodeMover.py)
data = {}
if os.path.exists(os.path.join(config['DIRS']['data_directory'], 'data.json')):
    with open(os.path.join(config['DIRS']['data_directory'], 'data.json'), 'r') as f:
        data = json.load(f)

# If not using EpisodeMover.py and data.json, enter your shows manually in
# config.ini
else:
    for show in config['SHOWS']:
        data[config['SHOWS'][show]] = 0

with urllib.request.urlopen("http://www.tvmuse.com/schedule.html") as f:
    soup = bs4.BeautifulSoup(f, 'html.parser')

# Find all references of a show in form 'a href=/tv-shows/Show-Name_####/season_##/episode_##'
p = re.compile('a href="\/tv-shows\/([A-Za-z\-]+)_(\d+)\/season_(\d+)\/episode_(\d+)')
m = re.findall(p, str(soup))
s = set(m)

# If any shows found above are in my list of shows, save for later
searches = []
for show in s:
    for myshow in data:
        if all(word in show[0].lower() for word in myshow.split()):
            search = "{} S{:0>2}E{:0>2}".format(show[0], show[2], show[3]).replace("-", " ")
            print("Available today: {}".format(search))
            searches.append(search.lower())

# Determine if I have already downloaded any episodes on the list
stillneed = searches[:]
for search in searches:
    for filename in os.listdir(config['DIRS']['video_directory']):
        if all(word in filename.lower() for word in search.split()):
            if search in stillneed:
                print("Already got it: {}".format(search))
                stillneed.remove(search)

# If I still need the show, open browser and search in selected engines
for search in stillneed:
    print("Searching for: {}".format(search))
    for engine in config['SEARCHENGINES']:
        webbrowser.open_new_tab(config['SEARCHENGINES'][engine].format(search))

    

