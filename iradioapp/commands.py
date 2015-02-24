from iradioapp import models
from iradioapp import mpcclient
import urllib.request
import json
import re

CLIENT_ID = "3ace999b30d1885aba027ba93de287ff"

def playpause(request):
	mpcclient.toggle_playing()

def next(request):
	mpcclient.next()

def previous(request):
	mpcclient.prev()

def setVolume(request):
	mpcclient.set_volume(request.POST.get('volume','30'))
	pass

def setSong(request):
	mpcclient.set_song(request.POST.get('songid','1'))
	pass

def parseSoundcloudUrl(url):
	rurl = "http://api.soundcloud.com/resolve.json?client_id=%s&url=%s" % (CLIENT_ID, url)
	resp = urllib.request.urlopen(rurl)
	data = resp.read().decode('utf-8')
	o = json.loads(data)
	return "soundcloud:song/%s.%s" % (o['title'], o['id'])

song_regex = {
	r'https?:\/\/open.spotify.com\/track\/(?P<sid>\S+)': (lambda sid: ("spotify:track:%s" % (sid))),
	r'spotify:track:(?P<sid>\S+)': (lambda sid: ("spotify:track:%s" % (sid))),
	r'(https?:\/\/soundcloud.com/\S+/\S+)': (lambda x: parseSoundcloudUrl(x)),
        r'https?://(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)(\w*)(&(amp;)?[\w\?=]*)?' : (lambda x: ("yt:%s" % x))
}

def addSong(request):
	result = []
	inp = request.POST.get('url', '')
	for regex in song_regex:
		urls = re.findall(regex, inp)
		for r in urls:
			result.append(song_regex[regex](r))
	print(result)
	for r in result:
		mpcclient.add_song(r)
	return { 'songs_added': [ x for x in result ] }

def getState(request):
	return mpcclient.get_status()

def getCurrent(request):
	return mpcclient.get_status()

def getPlaylist(request):
	return { "playlist": mpcclient.get_playlist() }

def searchLocal(request):
	pass

def listLocal(request):
	pass

def setShuffle(request):
	mpcclient.set_shuffle(True if request.POST.get('value','false') == "true" else False)

command_list = {
	'playpause': playpause,
	'next': next,
	'previous': previous,
	'setVolume': setVolume,
	'setSong': setSong,
	'addSong': addSong,
	'getState': getState,
	'getCurrent': getCurrent,
	'getPlaylist': getPlaylist,
	'searchLocal': searchLocal,
	'listLocal': listLocal,
	'setShuffle': setShuffle
}
