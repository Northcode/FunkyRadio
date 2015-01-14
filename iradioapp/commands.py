from iradioapp import models
from iradioapp.mpcclient import client, isPlaying

def playpause():
	if isPlaying():
		client.pause()
	else:
		client.play()

def next():
	client.next()

def previous():
	client.previous()

def setVolume():
	pass

def setSong():
	pass

def addSong():
	pass

def getPlaying():
	pass

def getCurrent():
	pass

def getPlaylist():
	pass

def searchLocal():
	pass

def listLocal():
	pass

command_list = {
	'playpause': playpause,
	'next': next,
	'previous': previous,
	'setVolume': setVolume,
	'setSong': setSong,
	'addSong': addSong,
	'getPlaying': getPlaying,
	'getCurrent': getCurrent,
	'getPlaylist': getPlaylist,
	'searchLocal': searchLocal,
	'listLocal': listLocal
}
