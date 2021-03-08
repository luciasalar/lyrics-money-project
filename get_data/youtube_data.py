from youtube_api import YouTubeDataAPI
import pandas as pd
from apiclient.discovery import build
import csv
import os
from ruamel import yaml


def load_experiment(path_to_experiment):
    #load experiment 
    data = yaml.safe_load(open(path_to_experiment))
    return data


class GetComments:
    """Here we get video comments according to video id """
    def __init__(self, api_key):
        '''define the main path'''
        self.path = '/disk/data/share/s1690903/Lyrics_project/data/youtube/comments.csv'
        self.api_key = api_key


    def build_service(self):

        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        return build(YOUTUBE_API_SERVICE_NAME,
                     YOUTUBE_API_VERSION,
                     developerKey=self.api_key)

    def get_comment_obj(self, videoId):
        """Retrieve comments from API"""
        response = self.build_service()

        # you only need to build the service once
        # collect all comments
  
        response2 = response.commentThreads().list(
                part='snippet',
                maxResults=100,
                textFormat='plainText',
                order='time',
                videoId=videoId,

        ).execute()

        return response2

    def save_comments(self, videoId):
        """Save comments to file."""
        comm_obj = self.get_comment_obj(videoId)# need to get the id 

        file_exists = os.path.isfile(self.path)
        f = open(self.path, 'a', encoding='utf-8-sig')
        writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer_top.writerow(['etag'] + ['videoId'] + ['commentId'] + ['text'] + ['author'] + ['like'] + ['time'])
            f.close()

        f = open(self.path, 'a', encoding='utf-8-sig')
        writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        for i in comm_obj['items']:

            result_row = [[i['etag'], i['snippet']['videoId'], i['snippet']['topLevelComment']['id'], i['snippet']['topLevelComment']['snippet']['textDisplay'], i['snippet']['topLevelComment']['snippet']['authorDisplayName'], i['snippet']['topLevelComment']['snippet']['likeCount'], i['snippet']['topLevelComment']['snippet']['publishedAt']]]
            writer_top.writerows(result_row)
        f.close()


class GetVideo:
    """Here we get the videos by searching the key words"""

    def __init__(self, api_key):
        '''define the main path'''
        self.path = '/disk/data/share/s1690903/Lyrics_project/data/youtube/video_list_hiphot_money.csv'
        self.api_key = api_key

    def search_kw(self, keywords):
        """Search videos by keywords """
        yt = YouTubeDataAPI(self.api_key)
        searches = yt.search(q=keywords,
                         max_results=1000)
        df_search = pd.DataFrame(searches)
        df_search.to_csv(self.path)

        return df_search

def get_video_comments(api_key, df_search):
    comm = GetComments(api_key)
    for vid in df_search.video_id:
        comm.save_comments(vid)



experiment = load_experiment('/disk/data/share/s1690903/Lyrics_project/' + 'env/experiment.yaml')

gv = GetVideo(experiment['youtube'][1])
df_search = gv.search_kw('hip hot money')
#get_video_comments(experiment['youtube'][1], df_search)











