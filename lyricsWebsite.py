from flask import Flask, jsonify, render_template
import spotify
app = Flask(__name__)

@app.route('/')
def main():
	return render_template('lyrics.html')
    
@app.route('/lyrics', methods= ['GET'])
def lyrics():
    return jsonify(lyrics = spotify.getLyrics())

@app.route('/song', methods= ['GET'])
def song():
    return jsonify(song = spotify.getSong())
  
@app.route('/artists', methods= ['GET'])
def artists():
    return jsonify(artists = spotify.getArtists())