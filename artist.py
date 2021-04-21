import itertools
import operator
import api as apt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import sys
sys.path.insert(1,'C:/Users/servet/Desktop/twitter-spotifypl/Google-Image-Scraper-master/')

import main as mk

from GoogleImageScrapper import GoogleImageScraper
import os

client_credentials_manager = SpotifyClientCredentials(apt.SPOTIPY_CLIENT_ID, apt.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_most_artists(USER_ID_INPUT):
    #user = '1tk1kfvg55jnrbples7x2884h'
    user = USER_ID_INPUT
    playlists = sp.user_playlists(user)

    # COUNT MOSTLY ACCURING ARTIST
    arts = []
    if(playlists['items']==None):
        return ""
    for i, pla in enumerate(playlists['items']):
        pl_id = pla['id']
        artist_names = sp.playlist_items(playlist_id=pl_id, fields='items.track.artists.name', additional_types=['track'])['items']
        for artist in artist_names:
            if(artist['track'] == None):
                continue
            len_arts = len(artist['track']['artists'])
            for j in range(0, len_arts):
                arts.append(artist['track']['artists'][j]['name'])

    unsorted_count_songs = dict((x,arts.count(x)) for x in set(arts))
    sort_descending = dict(sorted(unsorted_count_songs.items(),key=operator.itemgetter(1),reverse=True))
    get_sum = sum(sort_descending.values())

    for key, val in sort_descending.items():
        sort_descending[key] = round((val*100.0/get_sum),2)
    result = dict(itertools.islice(sort_descending.items(),5))

    i = 1
    user_name = sp.user(user)['display_name']
    status = "Hey " + user_name + "! Here are your top 5 playlist-artists:\n"
    print(status)
    for key in result.keys():
        if i == 1:
            mk.search(key)
        status += str(i) + "-" + key + "- " + str(result[key]) + "%\n"
        i += 1
    return status




def main():
    get_most_artists()

if __name__ == "__main__": main()



