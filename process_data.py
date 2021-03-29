import pandas as pd 
import demoji
import string
from pycontractions import Contractions
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
# -*- coding: utf-8 -*-

# path = '/disk/data/share/s1690903/Lyrics_project/data/youtube/comments.csv'
# file = pd.read_csv(path)

class Preprocess:
    """Here we get the videos by searching the key words"""

    def __init__(self, file):
        '''define the main path'''
        self.path = '/disk/data/share/s1690903/Lyrics_project/data/youtube/'
        self.file = pd.read_csv(self.path + file, encoding='utf-8-sig')
        contractions_list = {
        "ain't": "am not / are not / is not / has not / have not",
        "aren't": "are not / am not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he had / he would",
        "he'd've": "he would have",
        "he'll": "he shall / he will",
        "he'll've": "he shall have / he will have",
        "he's": "he has / he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how has / how is / how does",
        "i'd": "i had / i would",
        "i'd've": "i would have",
        "i'll": "i shall / i will",
        "i'll've": "i shall have / i will have",
        "i'm": "i am",
        "i've": "i have",
        "isn't": "is not",
        "it'd": "it had / it would",
        "it'd've": "it would have",
        "it'll": "it shall / it will",
        "it'll've": "it shall have / it will have",
        "it's": "it has / it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she had / she would",
        "she'd've": "she would have",
        "she'll": "she shall / she will",
        "she'll've": "she shall have / she will have",
        "she's": "she has / she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so as / so is",
        "that'd": "that would / that had",
        "that'd've": "that would have",
        "that's": "that has / that is",
        "there'd": "there had / there would",
        "there'd've": "there would have",
        "there's": "there has / there is",
        "they'd": "they had / they would",
        "they'd've": "they would have",
        "they'll": "they shall / they will",
        "they'll've": "they shall have / they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we had / we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what shall / what will",
        "what'll've": "what shall have / what will have",
        "what're": "what are",
        "what's": "what has / what is",
        "what've": "what have",
        "when's": "when has / when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where has / where is",
        "where've": "where have",
        "who'll": "who shall / who will",
        "who'll've": "who shall have / who will have",
        "who's": "who has / who is",
        "who've": "who have",
        "why's": "why has / why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you had / you would",
        "you'd've": "you would have",
        "you'll": "you shall / you will",
        "you'll've": "you shall have / you will have",
        "you're": "you are",
        "you've": "you have"
        }

        self.contractions = contractions_list

    def isEnglish(self, text):
        try:
            text.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True
     
    def convert_dict(self):

        convert = {}
        for vid, text in zip(self.file['commentId'], self.file['text']):
            #filter non english
            if isinstance(text, str) == True:
                convert[vid] = text

        return convert


    def preprocess1(self, sent):
        # convert contraction
        words = str(sent).split()
        new_words = []
        for w in words:#convert contractions
            if w in list(self.contractions.keys()):
                w = self.contractions[w]
                new_words.append(w)
            else:
                new_words.append(w)


        return ' '.join(new_words)

    def covert_emoji_to_text(self):
        """Convert emoji to text."""

        pre_file = self.convert_dict()
        emoji_dict = {}
        for k, v in pre_file.items():
            if isinstance(v, str) == True:
                emoji_text = demoji.replace_with_desc(v.lower())
                emoji_text = self.preprocess1(emoji_text)
                emoji_text2 = str(emoji_text).translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
                if self.isEnglish(emoji_text2) == True:
                    emoji_dict[k] = emoji_text2

        text_df = pd.DataFrame.from_dict(emoji_dict, orient='index')
        text_df['index'] = text_df.index
        text_df.columns = ['clean_comments', 'commentId']
        text_df.to_csv(self.path + 'clean_comments.csv', encoding='utf-8-sig')
        return text_df

p = Preprocess('comments.csv')
text_df = p.covert_emoji_to_text()

video_l = pd.read_csv('/disk/data/share/s1690903/Lyrics_project/data/youtube/video_list.csv', encoding='utf-8-sig')
comments = pd.read_csv('/disk/data/share/s1690903/Lyrics_project/data/youtube/comments.csv', encoding='utf-8-sig')
all_comm = pd.merge(comments, video_l, left_on='videoId', right_on='video_id', how='outer')
all_comments = pd.merge(text_df, all_comm, on='commentId', how='outer')

# merge with video title
all_comments.to_csv('/disk/data/share/s1690903/Lyrics_project/data/youtube/all_comments.csv', encoding='utf-8-sig')












