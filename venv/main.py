from ytm import YouTubeMusic
from flask import Flask, request, render_template, jsonify, make_response
from flask_cors import CORS


import itertools

# APP INIT

app = Flask(__name__, template_folder="template")

# Middleware

CORS(app)

# API SERVICE

yt = YouTubeMusic()


# Home Router for render template

@app.route('/')
def Home():
    return render_template('index.html')


# API endpoinds

@app.route('/songs', methods=["GET"])
def Songs():
    query = request.args.get('name')

    songs = yt.search_songs(query)

    toJSON = make_response(jsonify(songs, {"type": 'songs'}), 200)

    return toJSON


@app.route('/nextsongs')
def NextSongs():
    queryKey = request.args.get('key')
    songsNext = yt.search_songs(continuation=queryKey)

    queryKey = songsNext['continuation']

    if queryKey is songsNext['continuation']:
        songsNext = yt.search_songs(continuation=queryKey)
        s = ""

        s.replace(songsNext['continuation'], " ")
        queryKey = s

    toJSON = make_response(jsonify(songsNext), 200)

    return toJSON



# running app with flask backend
if __name__ == "__main__":
    app.run('localhost', 5000, True)
