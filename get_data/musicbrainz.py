import argparse
import musicbrainzngs
import os
import csv
import time
import json

#https://musicbrainz.org/doc/MusicBrainz_API/Search


# parser = argparse.ArgumentParser()
# parser.add_argument("--cdrom", help="provide the source of the cd", default="/dev/cdrom")
# args = parser.parse_args()

# device = args.cdrom

# print("device: %s" % device)
# disc = discid.read(device)
# print("id: %s" % disc.id)

# result = musicbrainzngs.get_releases_by_discid(disc.id, includes=["artists"])




class CollectReplies:
    """Collect replies via twitter api v2."""

    def __init__(self, inputP, outputP, outputFile, tag, country, filter_tags):
        '''define the main path'''
        self.inputP = inputP# input path
        self.outputPath = outputP# output path
        self.outputFile = outputFile
        self.tag = tag
        self.country = country
        self.filter_tags = filter_tags

    def search_artist(self, offset):
        """Search music in musicbrainz"""

        #By default the web service returns 25 results per request and you can set a limit of up to 100. You have to use the offset parameter to set how many results you have already seen so the web service doesn’t give you the same results again.

        result = musicbrainzngs.search_artists(query='', limit=100, offset=offset, strict=False, tag=self.tag, country=self.country)

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
            with open(self.outputPath + '{}.json'.format(self.outputFile), 'a') as f:
                json.dump(search_result, f)

            f = open(self.outputPath + '{}.csv'.format(self.outputFile), 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)



            for artist in search_result['artist-list']:
                if 'tag-list' in artist.keys():
                    for tag in artist['tag-list']:
                        if tag['name'] in self.filter_tags:
                # here store data for each artist
                            try:
                                if ('disambiguation' in artist.keys()) & ('country' not in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], None, artist['life-span']['begin'], artist['life-span']['ended'], artist['disambiguation']]]

                                if ('disambiguation' not in artist.keys()) & ('country' in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], artist['country'], artist['life-span']['begin'], artist['life-span']['ended'], None]]

                                if ('disambiguation' in artist.keys()) & ('country' in artist.keys()):
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], artist['country'], artist['life-span']['begin'], artist['life-span']['ended'], artist['disambiguation']]]

                                else:
                                    content = [[artist['id'], artist['type'], artist['name'], artist['gender'], None, artist['life-span']['begin'], artist['life-span']['ended'], None]]
                            except KeyError:
                                continue

                            writer_top.writerows(content)

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
            with open(self.outputPath + '{}.json'.format(self.outputFile), 'a') as f:
                json.dump(search_result, f)

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

        for offset in range(0, artist_count, 100):
            print('this is loop {}'.format(offset))

            search_result = self.store_result_artist(offset)

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


inputP = '/disk/data/share/s1690903/Lyrics_project_git/data/'
outputP = '/disk/data/share/s1690903/Lyrics_project_git/data/'
outputFile = 'artist_list_rap_US_filtered3'
tag = 'rap'# search by tags
country = 'US'
filter_tags = 'rap, r&b, hip hot, hip-hot, rnb'# filter out tags

musicbrainzngs.set_useragent("Audacious", "0.1", "https://github.com/jonnybarnes/audacious")

cr = CollectReplies(inputP=inputP, outputP=outputP, outputFile=outputFile, tag=tag, country=country, filter_tags=filter_tags)
#result = cr.store_result(100)
result = cr.loop_file_artist()
# result = musicbrainzngs.search_artists(query='', limit=100, offset=200, strict=False, tag='hip hot', country='US')

#result = cr.loop_file_songs()
# result = musicbrainzngs.search_recordings(query='', limit=10, offset=20, strict=False, tag='hip hot', country='US')















