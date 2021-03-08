from rap_stats import *



class Collect_artist_songs:
    def __init__(self, artist_path, billb_path, clean_artist, token):
        '''define the main path'''
        self.path = '/disk/data/share/s1690903/Lyrics_project/'
        self.artist_path = artist_path #where you save the artist file
        self.billb_path = billb_path 
        self.genius_client_access_token = token
        self.clean_artist_path = clean_artist

    def get_authors(self):
        genius = lyricsgenius.Genius(self.genius_client_access_token)
        bill = pd.read_csv(self.path + self.billb_path)
        # drop artist duplicates
        bill = bill.drop_duplicates(subset=['artist'])
        bill["artist_id"] = bill.index + 1
        bill.to_csv(self.path + self.clean_artist_path)

        file_exists = os.path.isfile(self.path + self.artist_path)
        f = open(self.path + self.artist_path, 'a')
        writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer_top.writerow(['title'] + ['artist'])
            f.close()

        for artistid, artist in zip(bill['artist_id'], bill['artist']):
            try:
                artist = genius.search_artist(artist, max_songs=500, sort="title")

                f = open(self.path + self.artist_path, 'a')
                writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

                if artist is not None:
                    num_songs = len(artist)
                    for i in range(0, num_songs-1):
                        print("*********************", artist.songs[i].title)
                        result_row = [[artist.songs[i].title, artist.songs[i].artist]]
                        writer_top.writerows(result_row)

            except TypeError:

                    pass
        f.close()



experiment = load_experiment('/disk/data/share/s1690903/Lyrics_project/' + 'env/experiment.yaml')
# art = Collect_artist_songs(artist_path='data/artist_1980s.csv', billb_path='data/cleaned_hothp_1980s.csv', clean_artist = 'data/clean_artist_1980s.csv', token = experiment['token'][2])
# art.get_authors()



genius = lyricsgenius.Genius(experiment['token'][4])
artist = genius.search_artist("YoungBoy Never Broke Again", max_songs=3, sort="title")
















