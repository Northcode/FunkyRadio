from iradioapp import models
from iradioapp import mpcclient
import re

def playpause(request):
	mpcclient.playPause()

def next(request):
	mpcclient.next()

def previous(request):
	mpcclient.previous()

def setVolume(request):
	mpcclient.setVolume(50)
	pass

def setSong(request):
	pass

song_regex = {
	r'http:\/\/open.spotify.com\/track\/(?P<sid>\S+)': (lambda sid: ("spotify:track:%s" % (sid))),
	r'spotify:track:(?P<sid>\S+)': (lambda sid: ("spotify:track:%s" % (sid))),
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
	pass

def getState(request):
	return { "playing": mpcclient.isPlaying(), "shuffeling": mpcclient.isShuffeling(), "consuming": mpcclient.isConsuming() }

def getCurrent(request):
	return mpcclient.getCurrent()

def getPlaylist(request):
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
