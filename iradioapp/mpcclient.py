from mpd import MPDClient, CommandError
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'
PASSWORD = False

client = None

def init():
	global client
	if client == None:
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

