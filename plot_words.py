import pandas as pd 
import collections
import re
import seaborn as sns
import datetime


class Plots:
    """Preprocess text."""

    def __init__(self, inputP, outputP, outputFile, inputdata, word, liwcFile, groupYear):
        """Define varibles."""
        self.inputP = inputP
        self.data = pd.read_csv(self.inputP + inputdata)
        self.liwc = pd.read_csv(self.inputP + liwcFile)
        self.groupYear = groupYear
      
        self.outputP = outputP
        self.word = word

    def data_dict(self):
        """Convert df to dictionary."""
        file = self.data

        file["song_id"] = file.index + 1

        #count = 0
        lyric_dict = collections.defaultdict(dict)
        for songid, artist_id, lyrics, year in zip(file['song_id'], \
            file['artist_id'], file['lyrics'], file['year']):

            lyric_dict[songid]['artist_id'] = artist_id
            lyric_dict[songid]['lyrics'] = lyrics
            lyric_dict[songid]['year'] = year

            # count =  count + 1
            # if count == 10000:
            #     break

        return lyric_dict

    def get_word(self):
        """Count occurrence of certain words in text """

        data = self.data_dict()

        
        word_dict = collections.defaultdict(dict)

        for songid, v in data.items():

            try:

                word_dict[songid]['artist_id'] = v['artist_id']
                word_count = v['lyrics'].split().count(self.word)
                #print(word_count)
                word_dict[songid]['word_count'] = word_count
                word_dict[songid]['year'] = v['year'].split('-')[0]

            except AttributeError:
                continue
    
        word_df = pd.DataFrame.from_dict(word_dict, orient='index')
        word_df['songid'] = word_df.index
        return word_df


    def get_multiple_words(self, phrase):
        """Count occurrence of certain words in text """

        data = self.data_dict()

        
        word_dict = collections.defaultdict(dict)
        
        for songid, v in data.items():

            try:
                word_dict[songid]['artist_id'] = v['artist_id']
                match = re.findall(phrase, str(v['lyrics']))
                #print(match)
                word_dict[songid]['word_count'] = len(match)
                #print(len(match))

                word_dict[songid]['year'] = v['year'].split('-')[0]

            except AttributeError:
                continue
    
        word_df = pd.DataFrame.from_dict(word_dict, orient='index')
        word_df['songid'] = word_df.index
        return word_df



    def group_year(self, file):
        """Group file by year."""

        file['year'] = pd.to_datetime(file['year'], format="%Y/%m/%d", errors= 'coerce')
        file['year'] = pd.DatetimeIndex(file['year']).year
        file = file.loc[file['year'] > 1989]
        group_year = file.groupby(file['year']//self.groupYear).mean()
        #group_year = file.groupby(file['year']).mean()
        group_year['year'] = group_year['year'].astype(int)

        return group_year


    def get_word_plot(self):
        """Plot single word over year."""

        word_count = p.get_word()
        group_year = p.group_year(word_count)
        sns_plot = sns.lineplot(data=group_year, x="year", y="word_count", label=self.word)
        fig = sns_plot.get_figure()
        fig.savefig(self.outputP + "{}.png".format(self.word))

        return group_year

    def get_multiple_word_plot(self, phrase):
        """Plot single word over year."""

        word_count = p.get_multiple_words(phrase)
        group_year = p.group_year(word_count)
        sns_plot = sns.lineplot(data=group_year, x="year", y="word_count", label=phrase)
        fig = sns_plot.get_figure()
        fig.savefig(self.outputP + "{}.png".format(phrase))

        return group_year

    def get_liwc(self):
        """Get liwc file. """

        liwc = self.liwc
        liwc = liwc.rename(columns={"B": "song_title", "C": "artist_name", "D": "lyrics", "E": "year", "F": "artist_id"}, errors="raise")
        liwc['year'] = liwc['year'].apply(lambda x: str(x).split('-')[0])

        return liwc


    def get_liwc_plot(self, liwcVar1, liwcVar2=None, liwcVar3=None):
        """Plot single word over year."""

        liwc = p.get_liwc()
        group_year = p.group_year(liwc)
        sns_plot = sns.lineplot(data=group_year, x="year", y=liwcVar1, label=liwcVar1)
        if liwcVar2 is not None:
            sns_plot = sns.lineplot(data=group_year, x="year", y=liwcVar2, label=liwcVar2)

        if liwcVar3 is not None:
            sns_plot = sns.lineplot(data=group_year, x="year", y=liwcVar3, label=liwcVar3)

        fig = sns_plot.get_figure()

        # save figure
        if (liwcVar2 is not None) & (liwcVar3 is None):
            fig.savefig(self.outputP + "{}_{}_liwc.png".format(liwcVar1, liwcVar2))
        elif liwcVar3 is not None:
            fig.savefig(self.outputP + "{}_{}_{}_liwc.png".format(liwcVar1, liwcVar2, liwcVar3))
        else:
            fig.savefig(self.outputP + "{}_liwc.png".format(liwcVar1))

        return group_year

    def get_lyrics_count(self, phrase=None):
        """Count Lyrics by year."""
        #file = self.data

        # select songs with keywords
        file = self.get_multiple_words(phrase)
        file = file[file['word_count'] > 0]

        # get liwc
        # file = self.get_liwc()
        # file = file[file[phrase] > 0]

        file['year'] = pd.to_datetime(file['year'], format="%Y/%m/%d", errors = 'coerce')
        file['year'] = pd.DatetimeIndex(file['year']).year
        file = file.loc[file['year'] > 1989]
        group_year = file.groupby(file['year']).count()
   
        return group_year



inputP = '/disk/data/share/s1690903/Lyrics_project_git/data/'
outputP = '/disk/data/share/s1690903/Lyrics_project_git/data/result/plots/'
inputdata = 'hiphop_lyrics_partial.csv'
outputFile = 'plot_money.csv'
word = 'suicide'
liwcFile = 'LIWC_lyrics_partial.csv'
groupYear = 1

p = Plots(inputP=inputP, outputP=outputP, outputFile=outputFile, inputdata=inputdata, word=word, liwcFile=liwcFile, groupYear=groupYear)


#liwc = p.get_lyrics_count()
#liwc = p.get_liwc_plot('death')
#word_count = p.get_multiple_word_plot('wanna die')
# word_count = p.get_multiple_word_plot('kill myself')
# word_count = p.get_multiple_word_plot('depression')
# word_count = p.get_word_plot()

wc = p.get_lyrics_count(phrase='broke')





