from subprocess import *

def send(args):
	if type(args) is str:
		args = [args]
	proc = Popen(["mpc"] + args,stdout=PIPE,stderr=PIPE)
	out,ret = proc.communicate()
	decoded = out.decode('utf-8')
	err = ret.decode("utf-8")
	if not err == "":
		# todo: error handling
		raise Exception("Error executing command: " + err)
		pass
	return decoded

def get_volume():
	vol = send("volume")
	return vol.split(':')[1].strip()

def get_status():
	trackinfo = send(['status','-f','%title%{(.}%album%{(.}%artist%']).split('\n')
	current_song = ""
	playing_status = ""
	flags_proto = ""
	if len(trackinfo) > 2:
		current_song = trackinfo[0].split('{(.}')
		current_song = { "title": current_song[0], "album": current_song[1], "artist": current_song[2] }
		playing_status_proto = [x for x in trackinfo[1].split(' ') if not x == '']
		playing_status = { "playing": (playing_status_proto[0] == "[playing]"), "tracknr": playing_status_proto[1][2:].split('/'), "time": playing_status_proto[2], "percent": playing_status_proto[3] }
		flags_proto = trackinfo[2]
	else:
		current_song = None
		playing_status = { "playing": False, "tracknr": 0, "time": "0:00/0:00", "percent": "0" }
		flags_proto = trackinfo[0]
	flags_proto = [x for x in flags_proto.replace(':',' ').split(' ') if not x == '']
	flags_proto = [(True if x == 'on' else False if x == 'off' else x) for x in flags_proto]
	flags = dict(zip(flags_proto[0::2],flags_proto[1::2]))
	return { "current_song": current_song, "playing_status": playing_status, "flags": flags }

def set_volume(vol):
	send(["volume",vol]) # maybe this is not safe.... should do some typechecks, oh well
	pass

def get_track():
	return get_status()["current_song"]

def get_playlist():
	playlist = send(['playlist','-f','%title%{(.}%album%{(.}%artist%']).split('\n')
	xplaylist = []
	for song in playlist:
		if song == '':
			continue
		songinfo = song.split('{(.}')
		xplaylist.append({ "title": songinfo[0], "album": songinfo[1], "artist": songinfo[2] })
	return xplaylist

def add_song(url):
	send(["add",url])
	pass

def set_song(songindex):
	send(["play",songindex])
	pass

def toggle_playing():
	status = get_status()["playing_status"]
	if status["playing"] == True:
		send("pause")
	else:
		send("play")

def set_shuffle(val):
	send(["random",('on' if val else 'off')])
	pass

def next():
	send("next")

def prev():
	send("prev")
