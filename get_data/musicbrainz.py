import argparse
import musicbrainzngs
import os
import csv
import time
import json
from ruamel import yaml
import collections
import pandas as pd

#https://musicbrainz.org/doc/MusicBrainz_API/Search


def load_experiment(path_to_experiment):
    #load experiment
    data = yaml.safe_load(open(path_to_experiment))
    return data


class CollectReplies:
    """Collect replies via twitter api v2."""

    def __init__(self, outputP, outputFile, tag, country, filter_tags):
        '''define the main path'''
       
        self.outputPath = outputP# output path
        self.outputFile = outputFile
        self.tag = tag
        self.country = country
        self.filter_tags = filter_tags

    def search_artist(self, offset):
        """Search music in musicbrainz"""

        #By default the web service returns 25 results per request and you can set a limit of up to 100. You have to use the offset parameter to set how many results you have already seen so the web service doesn’t give you the same results again.
        if self.country is not None:
            result = musicbrainzngs.search_artists(query='', limit=100, offset=offset, strict=False, country=self.country, tag=self.tag)

        else:
            result = musicbrainzngs.search_artists(query='', limit=100, offset=offset, strict=False, tag=self.tag)

        time.sleep(1)

        return result

    def search_song(self, offset):
        """Search music in musicbrainz"""

        #By default the web service returns 25 results per request and you can set a limit of up to 100. You have to use the offset parameter to set how many results you have already seen so the web service doesn’t give you the same results again.

        result = musicbrainzngs.search_recordings(query='', limit=100, offset=offset, strict=False, tag=self.tag, country=self.country)

        time.sleep(1)

        return result


    def store_result_artist(self, offset):

        search_result = self.search_artist(offset)

        file_exists = os.path.isfile(self.outputPath + '{}.csv'.format(self.outputFile))

        if not file_exists:
            f = open(self.outputPath + '{}.csv'.format(self.outputFile), 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer_top.writerow(["artist_id"] + ["artist_type"] + ["name"] + ["gender"] + ["country"] + ['begin'] + ['end'] + ['disambiguation'])
            f.close()

        # query user profile for each handle
        if file_exists:
            # with open(self.outputPath + '{}.json'.format(self.outputFile), 'a') as f:
            #     json.dump(search_result, f)

            f = open(self.outputPath + '{}.csv'.format(self.outputFile), 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            prev_artist = None
            for artist in search_result['artist-list']:
                if 'tag-list' in artist.keys():
                    for tag in artist['tag-list']:      
                        if (tag['name'] in self.filter_tags.split(',')) & (artist['id'] != prev_artist):
                            #print(tag['name'])
            # here store data for each artist
                            try:
                                
                                if ('disambiguation' in artist.keys()) & ('country' not in artist.keys()) & ('gender' not in artist.keys()) & ('life-span' not in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], None, None, None, None, artist['disambiguation']]]

                                elif ('disambiguation' in artist.keys()) & ('country' not in artist.keys()) & ('gender' not in artist.keys()) & ('life-span' in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], None, None, artist['life-span']['begin'], artist['life-span']['ended'], artist['disambiguation']]]


                                elif ('disambiguation' in artist.keys()) & ('country' in artist.keys()) & ('gender' not in artist.keys()) & ('life-span' not in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'],None, artist['country'], None, None, artist['disambiguation']]]

                                elif ('disambiguation' in artist.keys()) & ('country' in artist.keys()) & ('gender' in artist.keys()) & ('life-span' not in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], artist['country'], None, None,artist['life-span']['ended'], artist['disambiguation']]]

                                elif ('disambiguation' in artist.keys()) & ('country' in artist.keys()) & ('gender' not in artist.keys()) & ('life-span' in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], None, artist['country'], artist['life-span']['begin'], artist['life-span']['ended'], artist['disambiguation']]]

                                elif ('disambiguation' in artist.keys()) & ('country' in artist.keys()) & ('gender' in artist.keys()) & ('life-span' in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], artist['country'], artist['life-span']['begin'], artist['life-span']['ended'], artist['disambiguation']]]

                                elif ('disambiguation' in artist.keys()) & ('country' not in artist.keys()) & ('gender' in artist.keys()) & ('life-span' in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], None, artist['life-span']['begin'], artist['life-span']['ended'], artist['disambiguation']]]

                                elif ('disambiguation' in artist.keys()) & ('country' not in artist.keys()) & ('gender' in artist.keys()) & ('life-span' not in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], None, None, None, artist['disambiguation']]]

                                elif ('disambiguation' not in artist.keys()) & ('country' in artist.keys()) & ('gender' in artist.keys()) & ('life-span' in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], None, None, artist['life-span']['begin'], artist['life-span']['ended'], None]]

                                elif ('disambiguation' not in artist.keys()) & ('country' not in artist.keys()) & ('gender' in artist.keys()) & ('life-span' in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], None, artist['life-span']['begin'], artist['life-span']['ended'], None]]

                                elif ('disambiguation' not in artist.keys()) & ('country' in artist.keys()) & ('gender' in artist.keys()) & ('life-span' in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], artist['country'], artist['life-span']['begin'], artist['life-span']['ended'], None]]

                                elif ('disambiguation' not in artist.keys()) & ('country' in artist.keys()) & ('gender' not in artist.keys()) & ('life-span' in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], None, artist['country'], artist['life-span']['begin'], artist['life-span']['ended'], None]]

                                elif ('disambiguation' not in artist.keys()) & ('country' in artist.keys()) & ('gender' in artist.keys()) & ('life-span' not in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], artist['country'], None, None, None]]

                                elif ('disambiguation' not in artist.keys()) & ('country' not in artist.keys()) & ('gender' in artist.keys()) & ('life-span' not in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], None, None, None, None]]

                                elif ('disambiguation' not in artist.keys()) & ('country' in artist.keys()) & ('gender' not in artist.keys()) & ('life-span' not in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], None, artist['country'],  None, None, None, None]]


                                else:
                                    content = [[artist['id'], artist['type'], artist['name'], None, None, None, None, None]]
                            
                                
                                prev_artist = artist['id']
                                
                                writer_top.writerows(content)

                            except KeyError:
                                continue
                          

            return search_result

    def store_result_songs(self, offset):

        search_result = self.search_song(offset)

        file_exists = os.path.isfile(self.outputPath + '{}.csv'.format(self.outputFile))

        if not file_exists:
            f = open(self.outputPath + '{}.csv'.format(self.outputFile), 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer_top.writerow(["song_id"] + ["song_title"] + ["artist_id"] + ["artist_name"] + ["disambiguation"])
            f.close()

        # query user profile for each handle
        if file_exists:
            f = open(self.outputPath + '{}.csv'.format(self.outputFile), 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            for song in search_result['recording-list']:
            #here store data for each song, you can get artist inf by matching artist profile
                try:
                    content = [[song['id'], song['title'], song['artist-credit'][0]['name'], song['artist-credit'][0]['artist']['id'], song['artist-credit'][0]['artist']['disambiguation']]]

                except KeyError:
                    continue

                writer_top.writerows(content)

        return search_result

    def loop_file_artist(self):
    
        # get the artist count
        search_result = self.search_artist(25)

        artist_count = search_result['artist-count']
        print('there are {} artists in the db'.format(artist_count))

        multidicts = []
        for offset in range(0, 10000, 100):
            print('this is loop {}'.format(offset))

            search_result = self.store_result_artist(offset)
            multidicts.append(search_result)

        with open(self.outputPath + '{}.json'.format(self.outputFile), 'a') as f:
                json.dump(multidicts, f)

        return search_result


    def loop_file_songs(self):
    
        # get the artist count
        search_result = self.search_song(25)

        song_count = search_result['recording-count']
        print('there are {} songs in the db'.format(song_count))

        for offset in range(0, song_count, 100):
            print('this is loop {}'.format(offset))

            search_result = self.store_result_songs(offset)

        return search_result

class GetOtherInfo:
    """From here you can retrieve other variables from the json file"""
    def __init__(self, inputP, inputFile, outputP, outputFile_newVar):
        '''define the main path'''
        self.inputP = inputP
        self.inputFile = inputFile
        self.outputPath = outputP# output path
        self.outputFile = outputFile_newVar
    
    def Read_json(self):
        """Read json to dict """

        with open(self.inputP + self.inputFile, encoding="utf8") as f:
            
            data = f.readlines()

            data = [json.loads(line) for line in data] #convert string to dict format

        return data


    def get_tags(self):
        """retrieve tags from the profile doc """

        artists_result = self.Read_json()

        tag_dfs = pd.DataFrame()
        for artists in artists_result[0]:
            if artists is not None:

                tag_dict = collections.defaultdict(dict)
                for art in artists['artist-list']:
                    if 'tag-list' in art.keys():

                        prev_count = 0
                        prev_tag_list = ''
                
                        for each_tag in art['tag-list']:
                            # combine a list of tags
    
                            tags_list = each_tag['name'] + ', ' + prev_tag_list
                            prev_tag_list = tags_list

                            if int(each_tag['count']) > int(prev_count):
                                tag_dict[art['id']]['max_count'] = each_tag['count']
                                tag_dict[art['id']]['max_tag'] = each_tag['name']

                                prev_count = each_tag['count']

                        tag_dict[art['id']]['tags_list'] = tags_list

                        tag_df = pd.DataFrame.from_dict(tag_dict, orient='index')
                        if tag_df is not None:
                            tag_dfs = tag_dfs.append(tag_df)

        #tag_df.columns = ['']
        tag_dfs.to_csv(self.outputPath + self.outputFile, encoding='utf-8-sig')

        return tag_dfs

    def merge_files(self, path, file1_name, file2_name, outputFile):
        """merge other variables with artist list """

        file1 = pd.read_csv(path + file1_name)
        file1.columns = ['artist_id', 'max_count', 'max_tag', 'tags_list']
        file1 = file1.drop_duplicates(subset=['artist_id'])

        file2 = pd.read_csv(path + file2_name)

        all_file = pd.merge(file1, file2, on='artist_id', how='inner')
        all_file = all_file.drop_duplicates(subset=['artist_id'])

        all_file.to_csv(path + outputFile, encoding='utf-8-sig')

        return all_file
        

script_path = '/disk/data/share/s1690903/Lyrics_project_git/get_data/'
outputP = '/disk/data/share/s1690903/Lyrics_project_git/data/'
outputFile = 'artist_list_setting2'


env = load_experiment(script_path + 'parameters.yaml')
musicbrainzngs.set_useragent("Audacious", "0.1", "https://github.com/jonnybarnes/audacious")

cr = CollectReplies(outputP=outputP, outputFile=outputFile, tag=env['settings2']['tag'], country=None, filter_tags=env['settings2']['filter_tags'])

#result = cr.loop_file_artist()
result = musicbrainzngs.search_artists(query='E40', limit=2, offset=20, strict=False, tag='hip hop', country='US')


####get other variables
inputFile_json = 'artist_list_setting2.json'
outputFile_newVar = 'tags.csv'
other = GetOtherInfo(inputP=outputP, outputP=outputP, inputFile=inputFile_json, outputFile_newVar=outputFile_newVar)

#tags = other.get_tags()

#other.merge_files(path=outputP, file1_name='tags.csv', file2_name='artist_list_setting2.csv', outputFile='artist_list_setting2_tags.csv')














