from iradioapp import models
from iradioapp import mpcclient
import urllib.request
import json
import re

CLIENT_ID = "3ace999b30d1885aba027ba93de287ff"

def playpause(request):
	mpcclient.playPause()

def next(request):
	mpcclient.next()

def previous(request):
	mpcclient.previous()

def setVolume(request):
	mpcclient.setVolume(request.POST.get('volume','30'))
	pass

def setSong(request):
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
	r'(https?:\/\/soundcloud.com/\S+/\S+)': (lambda x: parseSoundcloudUrl(x))
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
		mpcclient.addSong(r)
	return { 'songs_added': [ x for x in result ] }

def getState(request):
	return { "playing": mpcclient.isPlaying(), "shuffeling": mpcclient.isShuffeling(), "consuming": mpcclient.isConsuming() }

def getCurrent(request):
	return mpcclient.getCurrent()

def getPlaylist(request):
	list = mpcclient.getPlaylist()
	if list is None:
		return { 'error': 'could not fetch playlist' }
	else:
		return { 'playlist': [ { 'id':x['id'], 'pos':x['pos'], 'file':x['file'], 'title':x['title'] } for x in mpcclient.getPlaylist() ]}

def searchLocal(request):
	pass

def listLocal(request):
	pass

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
	'listLocal': listLocal
}
