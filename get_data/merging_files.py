import pandas as pd 

path = '/disk/data/share/s1690903/Lyrics_project_git/data/'
rap = pd.read_csv(path + 'artist_list_setting1_tags.csv')
hiphop = pd.read_csv(path + 'artist_list_setting2_tags.csv')

hiphop_rap = rap.append(hiphop)

hiphop_rap = hiphop_rap.drop_duplicates(subset=['artist_id'])
# rapper list from music brainz
hiphop_rap.to_csv(path + 'hiphop_rap.csv')

# combine with lyrics 

lyrics = pd.read_csv(path + 'songs_year.csv')

lyrics2 = pd.read_csv(path + 'hip_hop_artist_all_lyrics2.csv', error_bad_lines=False)

lyrics3 = lyrics.append(lyrics2)

lyrics3 = lyrics3.rename({'artistid': 'artist_id'}, axis=1)
lyrics_id = lyrics3.drop_duplicates(subset=['artist_id'])

# get collected lyrics id
#collected = pd.merge(lyrics_id, hiphop_rap, on='artist_id', how='inner')
hiphop_lyrics_partial = pd.merge(lyrics3, hiphop_rap, on='artist_id', how='inner')
hiphop_lyrics_partial.to_csv(path + 'hiphop_lyrics_partial.csv')

# get not collect lyrics list
not_collected = hiphop_rap[(~hiphop_rap.artist_id.isin(lyrics_id.artist_id))]

# you might want to filter some ids then save it

#not_collected.to_csv(path + 'not_collected.csv')

#hip hop artist list from wikipedia

hiphop_rap_name_only = hiphop_rap[['name', 'artist_id']]
wiki = pd.read_csv(path + 'wikipedia_hiphop_artists.csv')

hiphop_rap_wiki = wiki.append(hiphop_rap_name_only) # 
# drop duplicated
hiphop_rap_wiki2 = hiphop_rap_wiki.drop_duplicates(subset=['name'], keep='first') #4726

# not yet collected
hiphop_rap_wiki_not_collected = pd.merge(hiphop_rap_wiki2, hiphop_rap_name_only, on='name', how='inner')

