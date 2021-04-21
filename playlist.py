
'''
for i, pla in enumerate(playlists['items']):
    if(pl_request in pla['name'].lower()):
        pl_id = pla['id']
        artist_names = sp.playlist_items(playlist_id=pl_id, fields='items.track.artists.name', additional_types=['track'])['items']
        track_name = sp.playlist_items(playlist_id=pl_id, fields='items.track.name', additional_types=['track'])['items']
        #print(artist_names)
        #print(track_name)

        for song in zip(artist_names,track_name):
            song_name = ""
            len_arts = len(song[0]['track']['artists'])
            for i in range(0,len_arts):
                song_name += song[0]['track']['artists'][i]['name']
                if i+1 != len_arts:
                    song_name += ", "
            song_name += " - " + song[1]['track']['name']
            songs.append(song_name)
#print(len(songs))

    # GET WANTED SPOTIFY PL TRACKS
'''