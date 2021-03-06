# Made by: Jack Stockley

# Program imports
from flask import Flask, request
import subprocess
from pynput.keyboard import Key, Controller
import os
import urllib.request, json

#Setup flask
app = Flask(__name__)

#Global variables
chrome = "chromium-browser"
flags = '--user-agent="Mozilla/5.0 (X11; CrOS armv7l 12371.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"'
currentVersion = 0.4

# Handles all the request for video streaming services
@app.route('/video', methods = ['POST'])
def video():
    service = request.get_json()["service"]
    service = service.lower()
    service = service.replace(" ", "")
    video = request.get_json()["video"]
    if(service == "youtube"):
        if(video.lower() == "subscriptions" or video.lower() == "subscription"):
            url = "https://www.youtube.com/feed/subscriptions"
            subprocess.Popen([chrome, flags, url])
            return "Loading your Youtube Subscriptions!"
        else:
            baseUrl = "https://www.youtube.com/results?search_query="
            url = video.replace(" ", "+")
            processed = baseUrl + url
            subprocess.Popen([chrome, flags, processed])
            return "Searching Youtube for " + video
    elif(service == "xfinity"):
        baseUrl = "https://www.xfinity.com/stream/search?q="
        url = video.replace(" ", "%20")
        processed = baseUrl + url
        subprocess.Popen([chrome, flags, processed])
        return "Searching Xfinity Stream for " + video
    elif(service == "twitch"):
        baseUrl = "https://www.twitch.tv/search?term="
        url = video.replace(" ", "%20")
        processed = baseUrl + url
        subprocess.Popen([chrome, flags, processed])
        return "Searching twitch.tv for " + video
    else:
        baseUrl = "https://www.justwatch.com/us/search?q="
        url = video.replace(" ", "%20")
        processed = baseUrl + url
        subprocess.Popen([chrome, flags, processed])
        return "Searching JustWatch.com for " + video

# Handles all the requests for music streaming services
@app.route('/music', methods = ['POST'])
def music():
    service = request.get_json()["service"]
    service = service.lower()
    service = service.replace(" ", "")
    music = request.get_json()["music"]
    if(service == "applemusic"):
        baseUrl = "https://music.apple.com/us/search?term="
        url = music.replace(" ", "%20")
        processed = baseUrl + url
        subprocess.Popen([chrome, flags, processed])
        return "Searching Apple Music for " + music
    elif(service == "spotify"):
        baseUrl = "https://open.spotify.com/search/"
        url = music.replace(" ", "%20")
        processed = baseUrl + url
        subprocess.Popen([chrome, flags, processed])
        return "Searching Spotify for " + music
    elif(service == "soundcloud"):
        baseUrl = "https://soundcloud.com/search?q="
        url = music.replace(" ", "%20")
        processed = baseUrl + url
        subprocess.Popen([chrome, flags, processed])
        return "Searching Soundcloud for " + music
    elif(service == "youtubemusic"):
        baseUrl = "https://music.youtube.com/search?q="
        url = music.replace(" ", "+")
        processed = baseUrl + url
        subprocess.Popen([chrome, flags, processed])
        return "Searching Youtube Music for " + music
    elif(service == "pandora"):
        baseUrl = "https://www.pandora.com/search/"
        url = music.replace(" ", "%20")
        processed = baseUrl + url + "/all"
        subprocess.Popen([chrome, flags, processed])
        return "Searching Pandora for " + music
    else:
        return "Sorry that service has not been added yet! If you would like it added please submit an issue on the GitHub repository for it to be added!"

# Launches steam link
@app.route('/steam')
def steam():
    subprocess.Popen("steamlink")
    return "Launching Steam Link!"

# Checks to see if there is a newer version of PiTV on the github repository
@app.route('/update')
def test():
    url = 'https://raw.githubusercontent.com/jnstockley/raspberrypi-smart-tv/master/version.txt'
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        latestVersion = data
    if (float(latestVersion) > currentVersion):
        return "Please update Pi TV!", 500
    else:
        return "Up to date!"

# Kills all the tasks that could be launched by PiTV
@app.route('/quit')
def quit():
    keyboard = Controller()
    os.system("pkill chromium-browse")
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)
    return "All tasks closed!"

## Runs the program
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)