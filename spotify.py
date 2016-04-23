import re
import sys
import subprocess
import spotipy
from os.path import expanduser
from spotipy.oauth2 import SpotifyClientCredentials

import credentials


def runCMD(cmd, timeout=1):
    print ('CMD:', str(cmd))
    return str(subprocess.run(cmd, stdout=subprocess.PIPE))


def show_tracks(results, playlist):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_name = track['name']
        artists = []
        for j in range(0, len(track['artists'])):
            artists.append(track['artists'][j]['name'])
        youtube_dl(track_name, playlist, artists)
        # print("%d %2.32s / %s" % (i, artist, track_name))


def youtube_dl(track, playlist, artists):
    path = expanduser('~\Desktop') + '\\' + playlist
    print('Path to folder: ' + path)
    # _track = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', track)
    _track = re.split(r'[-(]', track)
    print('Track name: ' + _track[0])
    print('Artists name: ' + ', '.join(artists))
    full_search = _track[0] + ' ' + ' '.join(artists)
    print('Key words for search: ' + full_search)

    artist_ = ', '.join(artists)
    track_ = str(track).replace('/', ' - ')
    print("Downloading: " + artist_, track_)
    command = 'youtube-dl --newline --no-post-overwrites --no-playlist -x --audio-format mp3 -i --audio-quality 0 "ytsearch1: ' + full_search + '" -o '
    cmd = command + '"' + path + '\\' + track_ + ' - ' + artist_ + '.%(ext)s"'
    # print(cmd)
    runCMD(cmd, 1)


if __name__ == '__main__':

    DEBUG = True

    if not DEBUG:
        if len(sys.argv) > 1:
            uri = sys.argv[1]
        else:
            print("usage: python spotify.py [URI]")
            sys.exit()
        print("Parsing: " + uri)

    else:
        uri = 'spotify:user:d.flucas:playlist:4Kls4WcczUw0Fj5XAx4Jbp'

    playlist_re = re.compile("spotify:user:[\w,.]+:playlist:[\w]+")
    # print(playlist_re)
    for playlist_uri in playlist_re.findall(uri):
        segments = playlist_uri.split(":")
        # print(segments)
        user_id = segments[2]
        print('List owner: ' + user_id)
        playlist_id = segments[4]
        print('List ID: ' + playlist_id)

    token = SpotifyClientCredentials(credentials.client_id, credentials.client_secret)
    if token:
        sp = spotipy.Spotify(client_credentials_manager=token)
        playlist = sp.user_playlist(user_id, playlist_id, fields="tracks, next, name")
        tracks = playlist['tracks']
        name_playlist = playlist['name']
        print('Playlist: ' + name_playlist)
        show_tracks(tracks, name_playlist)
        while tracks['next']:
            tracks = sp.next(tracks)
            show_tracks(tracks, name_playlist)
    else:
        print("Can't get token for", user_id)
