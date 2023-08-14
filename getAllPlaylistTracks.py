import spotipy
from spotipy.oauth2 import  SpotifyOAuth
import cred
import time
import random
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

# print('Current top tracks - medium term')
# displayList(sp.current_user_top_tracks(time_range='medium_term')['items'])

def trackQuery ():
    query = input("Type search query: ")
    res = sp.search(query)
    print(res['tracks']['items'][0].keys())
    displayList(res['tracks']['items'])

def insertIntoTop(arr, item):
    start = 0
    end = len(arr) - 1
    mid = (start + end) // 2
    while start <= end:
        mid = (start + end) // 2
        
        if item[0] > arr[mid][0]:
            end = mid - 1
        elif item[0] < arr[mid][0]:
            start = mid + 1
        else:
            arr.insert(mid, item)
            arr.pop()
            return
    if item[0] > arr[mid][0]:
        arr.insert(mid, item)
    elif item[0] < arr[mid][0]:
        arr.insert(mid+1, item)
    arr.pop()
    return 

plstObj_list = []
offsetVar = 0
getAllPlaylistsRes = sp.current_user_playlists(limit=50, offset=offsetVar)
print(getAllPlaylistsRes['limit'], getAllPlaylistsRes['total'], getAllPlaylistsRes['items'][0].keys())
while getAllPlaylistsRes['items']:
    # print(getAllPlaylistsRes['href'], getAllPlaylistsRes['previous'], getAllPlaylistsRes['next'])
    plstObj_list.extend(getAllPlaylistsRes['items'])
    offsetVar += 50
    getAllPlaylistsRes = sp.current_user_playlists(limit=50, offset=offsetVar)

playlistIDs = []

for i in range(len(plstObj_list)):
    plstObj = plstObj_list[i]
    if plstObj['owner']['id'] == 'timothycheung80':
        # print(plstObj['name'], plstObj['owner']['id'])
        playlistIDs.append(plstObj['id'])
# playlist = sp.playlist_items(playlistIDs[0])
# print(playlist.keys())
# print(playlist['total'], playlist['limit'], playlist['offset'], playlist['next'])
sortAtEnd = False
print(len(playlistIDs))
# playlistIDs = playlistIDs[:]
allTracksList = []

for playlistID in playlistIDs:
    pn = sp.playlist(playlistID)
    offsetVar = 0
    playlistItems = sp.playlist_items(playlistID, limit=100, offset=offsetVar)
    print(f"Processing {playlistID} : {pn['name']} length: {playlistItems['total']}")
    while playlistItems['items']:
        for t in playlistItems['items']:
            allTracksList.append(t)
        offsetVar += 100
        playlistItems = sp.playlist_items(playlistID, limit=100, offset=offsetVar)

print(len(allTracksList))

        



# getAllPlaylistsRes = sp.current_user_playlists() # limit and offset

# print(getAllPlaylistsRes.keys())
# print(getAllPlaylistsRes['limit'], getAllPlaylistsRes['total'], getAllPlaylistsRes['next'], getAllPlaylistsRes['items'][0].keys())
# playlists = getAllPlaylistsRes['items']
# print(getAllPlaylistsRes['items'][0]['owner']['display_name'])
# for i in range(len(playlists)):
#     playlistObject = playlists[i]
#     if playlistObject['owner']['id'] == "timothycheung80":
#         print(playlists[i]['name'], playlists[i]['owner']['id'], playlists[i]['owner']['display_name'])
    
    


