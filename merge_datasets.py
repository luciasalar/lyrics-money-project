import pandas as pd 
import glob


"""Here we create dataset 1 and dataset 2"""
# Dataset1 contains:
#1. hiphop songs from billboard top 100 hip hop songs (weekly charts from 70s to 2020)
#2. top 500 songs with keywords "rap money", "hip hop money"

# one problem is that youtube song titles are messy, Genuis lyrics won't have an exact match of these songs, so we need to consider only using YouTube dataset to study comments

#Dataset 2 contains dataset 1.1 with "money" in lyrics

class CleanData:
    def __init__(self):
        '''define the main path'''
        self.input_path = '/disk/data/share/s1690903/Lyrics_project/data/lyrics_hothp/'
        self.output_path = '/disk/data/share/s1690903/Lyrics_project/data/billboard_hothp_all.csv'
        
    def read_all_files(self) -> pd.DataFrame:
        """ Read all the billboard files. """
        all_files = []
        for file in glob.glob(self.input_path + "*.csv"):
            file_pd = pd.read_csv(file)
            all_files.append(file_pd)

        all_files_pd = pd.concat(all_files)
        all_files_pd.to_csv(self.output_path, encoding='utf-8-sig')

        return all_files_pd
       

    def clean_data(self, lyricsfile):
        """We only retain songs with publication year."""
        file = lyricsfile.dropna(subset=['year'])
        clean_file = file.dropna(subset=['lyrics'])

        return clean_file

class FilterKeywords:
    """Here we want to filter lyrics containing money."""
    def __init__(self, file):
        '''define the main path'''
        self.path = '/disk/data/share/s1690903/Lyrics_project/data/'
        self.file = pd.read_csv(self.path + file, encoding='utf-8-sig')
        self.filter_path = '/disk/data/share/s1690903/Lyrics_project/data/filter_lyrics/'
        self.output_path = '/disk/data/share/s1690903/Lyrics_project/data/filtered_lyrics.csv'

    def filter_lyrics(self, keywords):
        '''filter song lyrics according to list of keywords'''
        for k in keywords.split(','):
            fil_songs = self.file[self.file['lyrics'].str.contains(k)]
            fil_songs.to_csv(self.filter_path + 'filter_{}.csv'.format(k))
        return fil_songs
    

    def read_all_files(self) -> pd.DataFrame:
        """ Read all the billboard files. """
        all_files = []
        for file in glob.glob(self.filter_path + "*.csv"):
            file_pd = pd.read_csv(file)
            all_files.append(file_pd)

        all_files_pd = pd.concat(all_files)
        all_files_pd.to_csv(self.output_path, encoding='utf-8-sig')


        return all_files_pd



#dataset 1.1
#cle = CleanData()
#allfiles = cle.read_all_files()
# cleaned = cle.clean_data(allfiles)

#dataset 1.2
f = FilterKeywords('billboard_hothp_all.csv')
money_songs = f.filter_lyrics('money, cash, paperbacks')
all_filtered = f.read_all_files()
titles = all_filtered[['title','artist','year']]
titles.to_csv('/disk/data/share/s1690903/Lyrics_project/data/filtered_lyrics_title.csv')
#all_filtered.























