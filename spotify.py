import re
import sys
import subprocess
import urllib.parse
import spotipy
import urllib.parse
import urllib.request
from os.path import expanduser
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials


client_id ='239f993e90b54895a1faebc8b6b2f485'
client_secret ='e70808aa36e540c6b0dc545fbe4e5768'


def runCMD(cmd, timeout=1):
    print ('CMD:', str(cmd))
    return str(subprocess.run(cmd, stdout=subprocess.PIPE))



def show_tracks(results, playlist):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_name = track['name']
        artist = track['artists'][0]['name']
        show_youtube_url(track_name, playlist, artist)
        # print("%d %2.32s / %s" % (i, artist, track_name))


def show_youtube_url(track, playlist, artist):
    url_list = []
    _track = track.split('-')
    print('Track name: ' + _track[0])
    print('Artist name: ' + artist)
    full_search = _track[0] + ' ' + artist + ' audio'
    print('Key words for search: ' + full_search)
    query = urllib.parse.quote(full_search)
    # print(query)
    search_url = "https://www.youtube.com/results?search_query=" + query
    print(search_url)
    with urllib.request.urlopen(search_url) as response:
        the_page = response.read()
        soup = BeautifulSoup(the_page, "html.parser")
        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            url_final = 'https://www.youtube.com' + vid['href']
            test = url_final.split()
            url_list.append(test)
            url = url_list[0][0]
        print(url)
        download_audio_from_youtube(url, track, playlist, artist)

def download_audio_from_youtube(url, track, playlist, artist):
    home = expanduser('~\Desktop')
    path = home + '\\' + playlist.replace(' ', '_')
    print('Path to folder: ' + path)
    artist_ = str(artist).replace('/', '-')
    track_ = str(track).replace('/', '-')
    print("Downloading: " + artist_, track_)
    command = 'youtube-dl --newline --no-post-overwrites --no-playlist -x --audio-format mp3 --audio-quality 0 -o "'
    cmd = command + path + '\\' + track_ + '-' + artist_ + '.%(ext)s" ' + url
    # print(cmd)

    runCMD(cmd, 3)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        print("usage: python spotify.py [URI]")
        sys.exit()
    print("Parsing: " + uri)

    # uri = 'spotify:user:12144157524:playlist:5z6oshhZ24pqDLOrleCbwp'

    playlist_re = re.compile("spotify:user:[\w,.]+:playlist:[\w]+")
    print(playlist_re)
    for playlist_uri in playlist_re.findall(uri):
        segments = playlist_uri.split(":")
        # print(segments)
        user_id = segments[2]
        print('List owner: ' + user_id)
        playlist_id = segments[4]
        print('List ID: ' + playlist_id)


    token = SpotifyClientCredentials(client_id, client_secret)
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
