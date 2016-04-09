import re
import sys
import subprocess
import spotipy
import urllib.parse
import urllib.request
from os.path import expanduser
from spotipy.oauth2 import SpotifyClientCredentials

client_id ='239f993e90b54895a1faebc8b6b2f485'
client_secret ='e70808aa36e540c6b0dc545fbe4e5768'
# redirect_uri ='http://listparser.com/callback'
# username = 'd.flucas'
username = '12144157524'
# list_ = '4Kls4WcczUw0Fj5XAx4Jbp'
list_ = '1UmF20zPbew2OHOiZfWwUA'

uri = 'spotify:user:spotify:playlist:5ILSWr90l2Bgk89xuhsysy'



def runCMD(cmd, timeout=1):
    print ('CMD:', str(cmd))
    return str(subprocess.run(cmd, stdout=subprocess.PIPE))



def show_tracks(results, playlist):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        show_youtube_url(track['name'], playlist, track['artists'][0]['name'])
        print("%d %2.32s / %s" % (i, track['artists'][0]['name'], track['name']))


def show_youtube_url(track, playlist, artist):
    full_search = track+ ' ' + artist
    print(full_search)
    query_string = urllib.parse.urlencode({"search_query": full_search})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    url = "http://www.youtube.com/watch?v=" + search_results[0]
    download_audio_from_youtube(url, track, playlist, artist)
    print("http://www.youtube.com/watch?v=" + search_results[0])


def download_audio_from_youtube(url, track, playlist, artist):
    home = expanduser('~\Desktop')
    path = home + '\\' + playlist.replace(' ', '_')
    print(path)
    artist_ = str(artist).replace(' ', '_')
    track_ = str(track).replace(' ', '_')
    command = "youtube-dl --newline --no-post-overwrites --no-playlist -x --audio-format mp3 --audio-quality 0 -o "
    cmd = command + path + "\\" + artist_ + "-" + track_ + ".%(ext)s " + url

    runCMD(cmd, 3)


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     username = sys.argv[1]
    #     list_ = sys.argv[2]
    # else:
    #     print ("Whoops, need your username!")
    #     print ("usage: python user_playlists.py [username] [list_id]")
    #     sys.exit()
    # # runCMD("youtube-dl -U")
    token = SpotifyClientCredentials(client_id, client_secret)
    if token:
        sp = spotipy.Spotify(client_credentials_manager=token)
        playlist = sp.user_playlist(username,list_,fields="tracks, next, name")
        tracks = playlist['tracks']
        name_playlist = playlist['name']
        print('Playlist: ' + name_playlist)
        show_tracks(tracks, name_playlist)
        while tracks['next']:
            tracks = sp.next(tracks)
            show_tracks(tracks, name_playlist)
    else:
        print ("Can't get token for", username)