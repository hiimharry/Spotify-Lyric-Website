import os
import spotipy
import spotipy.util as util
import requests
from bs4 import BeautifulSoup
import re
from secret import cid, secret, headers

base_url = "http://api.genius.com/search"

scope = 'user-read-currently-playing'
	
username = ""

token = util.prompt_for_user_token(username, scope, client_id=cid,
                           client_secret=secret,
                           redirect_uri='https://google.com')
                           
def updateSong():
    return sp.current_user_playing_track()
                           
if token:
    sp = spotipy.Spotify(auth=token)  
    results = sp.current_user_playing_track()



    
def mstotime(ms):
	min = int((ms/1000)/60)
	sec = str(int(ms/1000) - min*60).zfill(2)
	return str(min) + ":" + str(sec)

def lyrics_from_song_path(path):
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.unwrap() for h in html('a')]
    lyrics = None
    lyrics = html.find_all("div", class_=re.compile(r'^Lyrics__Container'))
    if lyrics == None:
        return "Loading..."
    return "".join([(str(x) + "<br>") for x in lyrics])

def getSong():
    results = updateSong()
    if token:
        if results != None:
            return results['item']['name'];
    return "No song playing right now"

def getArtists():
    results = updateSong()
    if token:
        if results != None:
            artists = []
            for artist in results['item']['artists']:
                artists.append(artist['name'])
            return artists
    return ""

def getSongID(artists, search):
    for hit in search.json()['response']['hits']:
        songArtist = hit['result']['primary_artist']['name'].lower().replace("’", "'")
		#genius randomly appends a blank character infront of artist names for some reason?
        if songArtist[0] == '\u200b':
            songArtist = songArtist[1:]
        for artist in artists:
            if artist in songArtist:
                return str(hit['result']['path'])
    return ""
	#print(mstotime(results['progress_ms']))
	#print(results['item']['name'])
	
def getLyrics():
    results = updateSong()
    if results != None:
        song = results['item']['name']
        #for some reason having feat. messes up the genius query
        song = song.replace("feat.", "")
        #for items in results['item']['artists']:
            #print(items['name'])
        artists = [x.lower() for x in getArtists()]
        data = {'q': song}
        search = requests.get(base_url, params=data, headers=headers)
        song_id = getSongID(artists, search)
        if song_id:
            return "<br>" + lyrics_from_song_path(song_id)
        else:
            query = song
            for artist in artists: 
                query += " " + artist
            data = {'q' : query}
            search = requests.get(base_url, params=data, headers=headers)
            song_id = getSongID(artists, search)
            if song_id:
                return "<br>" + lyrics_from_song_path(song_id)
            else:
                return "Song too obscure :("