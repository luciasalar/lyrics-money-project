import lyricsgenius
import billboard
import datetime
import os
import csv
import pandas as pd
from ruamel import yaml



#from datetime import datetime

#https://github.com/johnwmillr/LyricsGenius

def load_experiment(path_to_experiment):
    #load experiment 
    data = yaml.safe_load(open(path_to_experiment))
    return data


class Collect_billboard:
    def __init__(self, gap, numdays, year_to_days, chart, start_day):
        '''define the main path'''
        self.path = '/disk/data/share/s1690903/Lyrics_project/'
        self.billboard_result_path = 'data/billboard_list_hothp_1970s.csv'
        self.lyrics_path = 'data/lyrics_hothp_1970s.csv'
        self.gap = gap
        self.numdays = numdays
        self.year_to_days = year_to_days
        self.chart = chart
        self.base = datetime.datetime.today() - datetime.timedelta(days=start_day)


    def get_dates(self):
        '''get list of dates that goes back every 7 days, set how many days you want'''
        x = self.numdays
        d_list = []
        
        date_list = [self.base - datetime.timedelta(days=x) for x in range(1, self.year_to_days, self.gap)]
        for day in date_list:
            dt_object = day.strftime("%Y-%m-%d")
            d_list.append(dt_object)

        return d_list


    def get_billboard_list(self):
        """Get list of billboard songs. """

        date_list = self.get_dates()
        file_exists = os.path.isfile(self.path + self.billboard_result_path)
        f = open(self.path + self.billboard_result_path, 'a')
        writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer_top.writerow(['title'] + ['artist'] + ['retrieve_date'] + ['rank'] + ['weeks'])
            f.close()

        for d in date_list:
            print(d)
            chart = billboard.ChartData(self.chart, date=d)
            f = open(self.path + self.billboard_result_path, 'a')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            chart_len = len(chart)
            for rank in range(0, chart_len-1):
                result_row = [[chart.entries[rank].title, chart.entries[rank].artist, d, chart.entries[rank].rank, chart.entries[rank].weeks]]
                writer_top.writerows(result_row)

    def get_lyrics(self, billboard, genius_client_access_token):
        genius = lyricsgenius.Genius(genius_client_access_token)

        file_exists = os.path.isfile(self.path + self.lyrics_path)
        f = open(self.path + self.lyrics_path, 'a')
        writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer_top.writerow(['title'] + ['artist'] + ['lyrics'] + ['album'] + ['year'])
            f.close()

        for title, artist, songid in zip(billboard['title'], billboard['artist'], billboard['song_id']):

            try:

                song = genius.search_song(title, artist)

                f = open(self.path + self.lyrics_path, 'a')
                writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

                if song is not None:
                    result_row = [[songid, title, artist, song.lyrics, song.album, song.year]]
                    writer_top.writerows(result_row)
            except TypeError:

                print("{} is not found".format(title))
        f.close()


if __name__ == "__main__":
    bill = Collect_billboard(gap=7, numdays=521, year_to_days=3650, chart='r-b-hip-hop-songs', start_day = 14600)

    #'rap streaming songs'
    #bill.get_billboard_list()

    billboard = pd.read_csv(bill.path + '/data/billboard_list_hothp_1970s.csv')
    clean_b = billboard.drop_duplicates(subset=['title'])
    # assign song id 
    clean_b["song_id"] = clean_b.index + 1
    clean_b.to_csv(bill.path + "/data/cleaned_hothp_1970s.csv")

    #clean_b = pd.read_csv(bill.path + '/data/cleaned_hothp_2000s_1990s.csv')

    experiment = load_experiment(bill.path + 'env/experiment.yaml')
    bill.get_lyrics(clean_b, experiment['token'][3])















