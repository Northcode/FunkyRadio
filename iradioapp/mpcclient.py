from mpd import MPDClient, CommandError, ConnectionError
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'
PASSWORD = False

client = None

def init():
	global client
	if not client:
		client = MPDClient()
		try:
			client.connect(host=HOST, port=PORT)
		except SocketError:
			client = None
			print("Failed to establish connection to mpc server at %s:%s" % (HOST, PORT))
			return
		if PASSWORD:
			try:
				client.password(PASSWORD)
			except CommandError:
				client = None
				print("Failed to authenticate connection to mpc server at %s:%s with password" % (HOST, PORT))
				return

def checkConnection(func, *params):
	global client
	if not client:
		init()
	try:
		return func(*params)
	except ConnectionError:
		client = None
		init()
		try:
			return func(*params)
		except ConnectionError:
			return


def _isPlaying():
	global client
	r = client.status()
	if not r:
		return False
	return r["state"] == "play"

def isPlaying():
	return checkConnection(_isPlaying)

def _playPause():
	global client
	if isPlaying():
		client.pause()
	else:
		client.play()

def playPause():
	checkConnection(_playPause)

def next():
	global client
	checkConnection(client.next)

def previous():
	global client
	checkConnection(client.previous)

def setVolume(vol):
	global client
	checkConnection(client.setvol,vol)

def addSong(url):
	checkConnection(client.add, url)

