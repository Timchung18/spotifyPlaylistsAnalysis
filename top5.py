import spotipy
from spotipy.oauth2 import  SpotifyOAuth
import cred
import requests
import webbrowser
import urllib
import base64

scope = "playlist-read-private user-library-read user-top-read user-follow-read user-read-recently-played"


authorization_manager = SpotifyOAuth(client_id=cred.client_id, client_secret= cred.client_secret, redirect_uri=cred.redirect_url, scope=scope)
sp = spotipy.Spotify(auth_manager=authorization_manager)


def displayList(results):
   # results is a list of 'track' objects (each 'item' in 'items' is a 'track' object)
   # doesn't work with playlists because each 'item' in 'items' is a 'playlist track' object
   #    which contains playlist related info of the track and then the track object itself

    for idx, item in enumerate(results):
        # print(idx, ":", item['album'], item['artists'], item['name'], item['popularity'], item['id'])
        songName = item['name']
        artist = item['artists']
        album = item['album']
        pop = item['popularity']
        songId = item['id']
        print(idx, ":", songName)
        print(songId)
        print(album['name'])
        artists = ""
        for i in range(len(artist)):
            artists += artist[i]['name'] + "("  + artist[i]['id'] + ") , " 
        print(artists)
        
    return

def useSpotipy():
    print('Current top tracks - medium term')
    displayList(sp.current_user_top_tracks(time_range='medium_term')['items'])

    print('\nCurrent top tracks - short term')
    displayList(sp.current_user_top_tracks(time_range='short_term')['items'])

    # getAllPlaylists(50,0)
    getAllPlaylists(50,50)

    # get info on a specific playlist
    res = sp.playlist('0qTqyhbLcSJXNGfQBRqc9f')
    print('\nInfpo on playlist named: ' + res['name'])
    print(res['tracks']['items'][0].keys())
    for i in res['tracks']['items']:
        track = i['track']
        print(track['name'], track['id'])
    print()
    
    getTopEnergySongsInList('2Ho8mkqd0pKGEiOc8yEUPV')
    # res = sp.current_user_saved_tracks()
    # resList = [i['track'] for i in res['items']]
    # displayList(resList)

def getAllPlaylists(limit, offset):
    print('\nAll my playlists')
    # getting all my playlists
    res = sp.current_user_playlists(limit, offset)
    print(res.keys())           
    print(res["total"], res["limit"], res["next"])
    print(res['items'][0].keys())
    for i in res['items']:
        print(i['name'] , i['id'])
    print()

def getTopEnergySongsInList(playlistID):
    res = sp.playlist(playlistID)
    print('\nHigh Energy Songs of : ' + res['name'])

    top5 = []
    other = []
    track = res['tracks']['items'][0]['track']
    print(track['name'], track['id'])
    features = sp.audio_features(track['id'])
    print(features[0].keys())
    print(features[0]['energy'])
    for i in res['tracks']['items']:
        track = i['track']
        # print(track['name'], track['id'])
        features = sp.audio_features(track['id'])
        if features[0] is not None:
            top5.append((features[0]['energy'], track['id'], track['name']))
        # other.append((features[0]['tempo'], track['id'], track['name']))
    top5.sort(reverse=True)
    other.sort(reverse=True)
    for i in range(8):
        print(top5[i])
    # for i in range(5):
    #     print(other[i])

    trackIds = []
    for i in res['tracks']['items']:
        track = i['track']
        trackIds.append(track['id'])
    

        
    print()


useSpotipy()



"""
# attempting to authorize without use of Spotipy
async def callbackAuth(resp, *args, **kwargs):
    print(resp.text)
    return 

def foo():
    with requests.Session() as s:
        ## authorize
        auth_url = 'https://accounts.spotify.com/authorize'
        auth_params = {'client_id' : cred.client_id, 'response_type' : 'code', 'redirect_uri' : cred.redirect_url, 'scope': scope}
        auth_response = s.get(auth_url, params=auth_params)
        print(auth_response.text)
        print()
        print(auth_response.url)


    get_url = "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=10"
    
foo()
"""

"""
# scope = "playlist-read-private%20user-library-read%20user-top-read%20user-follow-read%20user-read-recently-played"
auth_url = 'https://accounts.spotify.com/authorize?'
auth_params = {'client_id' : cred.client_id, 'response_type' : 'code', 'redirect_uri' : cred.redirect_url, 'scope': scope}
res = webbrowser.open(auth_url + urllib.parse.urlencode(auth_params))
print(auth_url + urllib.parse.urlencode(auth_params))

print(type(res))

"""
