import time 
import os
import csv
import pandas as pd
from ruamel import yaml
import lyricsgenius
import json
import collections
import requests


def load_experiment(path_to_experiment):
    #load experiment 
    data = yaml.safe_load(open(path_to_experiment))
    return data

class Collect_artist_songs:
    def __init__(self, path, outputfile, artist_list_path, token):
        '''define the main path'''
        self.path = path
        self.outputfile = outputfile #where you save the artist file
        self.artist_list_path = artist_list_path
        self.genius_client_access_token = token
        #self.clean_artist_path = clean_artist

    def get_authors(self):
        genius = lyricsgenius.Genius(self.genius_client_access_token)
        artists = pd.read_csv(self.path + self.artist_list_path)
        # drop artist duplicates
        artists = artists.drop_duplicates(subset=['artist_id'])
        #artists = artists.iloc[68::]

        #artists["artist_id"] = artists.index + 1
        #bill.to_csv(self.path + self.clean_artist_path)

        file_exists = os.path.isfile(self.path + self.outputfile)
        f = open(self.path + self.outputfile, 'a', encoding='utf-8-sig')
        writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)


        if not file_exists:
            writer_top.writerow(['title'] + ['artist_name'] + ['lyrics'] + ['year'] + ['artistid'])
            f.close()

        else:

            lyric_dict = collections.defaultdict(dict)

            for artistid, artist in zip(artists['artist_id'], artists['name']):

                # get max 200 songs from each artist
                try:
                    artist_songs = genius.search_artist(artist, max_songs=500, sort="title")
                    #time.sleep()

                except (requests.exceptions.ChunkedEncodingError, requests.ReadTimeout, requests.exceptions.ConnectionError, TypeError) as err:

                    time.sleep(5 * 60)
                    continue


                if artist_songs is not None:# check if object is empty

                    # store ids in dict
                    lyric_dict[artistid]['name'] = artist
                    #lyric_dict['artist_id']['artist_name'] = [artist]

                    # store info in csv
                    f = open(self.path + self.outputfile, 'a', encoding='utf-8-sig')
                    writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

                    try:
                        # store search as csv
                        # store all the songs from artist object
                        
                        for i in artist_songs.songs:

                            lyric_dict[artistid]['song_title'] = i.title
                
                            song_lyrics = artist_songs.song(i.title)
                            print(song_lyrics.lyrics)

                            lyric_dict[artistid]['song_lyrics'] = song_lyrics.lyrics

                            if song_lyrics.year is not None:
                                print('year exists')

                                lyric_dict[artistid]['year'] = song_lyrics.year
                                #print ('this is result', lyric_dict)

                            result_row = [[i.title, i.artist, song_lyrics.lyrics, song_lyrics.year, artistid]]
                            writer_top.writerows(result_row)
                            
                            # store result to json
                            with open(self.path + '{}.json'.format(self.outputfile), 'a', encoding='utf-8-sig') as fjson:
                                json.dump(lyric_dict, fjson)
                                fjson.close()

                    except TypeError:
                        continue

                    f.close()

    def get_authors_many_songs(self):
        genius = lyricsgenius.Genius(self.genius_client_access_token)
        artists = pd.read_csv(self.path + self.artist_list_path)
        # drop artist duplicates
        #artists = artists.drop_duplicates(subset=['artist_id'])
        #artists = artists.iloc[68::]

        #artists["artist_id"] = artists.index + 1
        #bill.to_csv(self.path + self.clean_artist_path)

        file_exists = os.path.isfile(self.path + self.outputfile)
        f = open(self.path + self.outputfile, 'a', encoding='utf-8-sig')
        writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)


        if not file_exists:
            writer_top.writerow(['title'] + ['artist_name'] + ['lyrics'] + ['year'])
            f.close()

        else:

            lyric_dict = collections.defaultdict(dict)

            for artist in artists['name']:

                # get max 200 songs from each artist
                try:
                    artist_songs = genius.search_artist(artist, max_songs=50000, sort="title")
                    #time.sleep()

                except (requests.exceptions.ChunkedEncodingError, requests.ReadTimeout, requests.exceptions.ConnectionError, TypeError) as err:

                    time.sleep(5 * 60)
                    continue


                if artist_songs is not None:# check if object is empty

                   
                    # store info in csv
                    f = open(self.path + self.outputfile, 'a', encoding='utf-8-sig')
                    writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

                    try:
                        # store search as csv
                        # store all the songs from artist object
                        multidicts = []
                        for i in artist_songs.songs:

                            lyric_dict[artist]['song_title'] = i.title
                
                            song_lyrics = artist_songs.song(i.title)
                            print(song_lyrics.lyrics)

                            lyric_dict[artist]['song_lyrics'] = song_lyrics.lyrics

                            if song_lyrics.year is not None:
                                print('year exists')

                                lyric_dict['year'] = song_lyrics.year
                                #print ('this is result', lyric_dict)

                            result_row = [[i.title, i.artist, song_lyrics.lyrics, song_lyrics.year]]
                            writer_top.writerows(result_row)
                            multidicts.append(lyric_dict)

                            
                            # store result to json
                            with open(self.path + '{}.json'.format(self.outputfile), 'a', encoding='utf-8-sig') as fjson:
                                json.dump(multidicts, fjson)
                                fjson.close()

                    except TypeError:
                        continue

                    f.close()


experiment = load_experiment('/disk/data/share/s1690903/Lyrics_project/' + 'env/experiment.yaml')
path = '/disk/data/share/s1690903/Lyrics_project_git/data/'
outputfile = 'hip_hop_artist_all_lyrics.csv'#name of the song file
#artist_list_path = 'artist_list_rap_US_filtered3.csv'
artist_list_path = 'not_collected.csv'
genius_client_access_token = experiment['token'][1]


art = Collect_artist_songs(artist_list_path=artist_list_path, outputfile=outputfile, path=path, token = genius_client_access_token)
# art.get_authors()
art.get_authors_many_songs()

# genius = lyricsgenius.Genius(experiment['token'][4])
# artist = genius.search_artist("YoungBoy Never Broke Again", max_songs=1, sort="title")
















