import pandas as pd 
from collections import defaultdict
import string
from gensim.models import CoherenceModel
import gensim
from pprint import pprint
import spacy, en_core_web_sm
from nltk.stem import PorterStemmer
import os
import json
from gensim.models import Word2Vec
import nltk
import re
import collections
from nltk.tokenize import word_tokenize
from sklearn.metrics import classification_report
import numpy as np
import datetime
from datetime import datetime
import csv
import gc
import os
# type hints
from typing import Dict, Tuple, Sequence
import typing
from ruamel import yaml
import contractions
from gensim.sklearn_api import LdaTransformer
import lda
from itertools import islice
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# -*- encoding: utf-8 -*-


def load_experiment(path_to_experiment):
    """Load experiment."""
    data = yaml.safe_load(open(path_to_experiment))
    return data

def take(n, iterable):
    """Return first n items of the iterable as a list"""

    return list(islice(iterable, n))

# Topic model
class ProcessText:
    """Preprocess text."""

    def __init__(self, path_data, path_result, filename, inputdata):
        """Define varibles."""
        self.path_data = path_data

        if filename is not None:
            self.data = pd.read_csv(self.path_data + filename)
        else:
            self.data = inputdata

        self.path_result = path_result

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

    def data_dict(self):
        """Convert df to dictionary."""
        file = self.data

        file["song_id"] = file.index + 1

        lyric_dict = collections.defaultdict(dict)
        for songid, artist_id, lyrics in zip(file['song_id'], \
            file['artist_id'], file['lyrics']):

            lyric_dict[songid]['artist_id'] = artist_id
            lyric_dict[songid]['lyrics'] = lyrics


        return lyric_dict

    def simple_preprocess(self):
        """Simple text process: lower case, remove punc."""
        data_dict = self.data_dict()
        mydict = lambda: defaultdict(mydict)
        cleaned = mydict()
        words = set(nltk.corpus.words.words())
        count = 0
        for k, v in data_dict.items():
            sent = v['lyrics']            
            # remove non-English words
            sent = " ".join(w for w in nltk.wordpunct_tokenize(str(sent)) \
         if w.lower() in words or not w.isalpha())
            # remove brackets
            sent = re.sub("[\(\[].*?[\)\]]", "", str(sent))
            # remove contractions
            sent = contractions.fix(sent)
            # remove line breaks
            sent = str(sent).replace('\n', ' ')
            # sent = str(sent).replace(' â€™', 'i')
            sent = str(sent).replace('\u200d', ' ')
            # lower case and remove punctuation
            sent = str(sent).lower().translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
            
            # convert contractions
            new_words = []
            for w in sent.split(' '): #convert contractions
                if w in list(self.contractions.keys()):
                    w = self.contractions[w]
                    new_words.append(w)

                elif w not in set(stopwords.words('english')):
                    new_words.append(w)

            sent = ' '.join(new_words)
            cleaned[k]['lyrics'] = sent
            # count = count + 1
            # if count == 1000:
            #     break

        return cleaned

    def extract_entities(self, cleaned_text: typing.Dict[str, str]) -> typing.Dict[str, str]:
        """Get noun, verbs and adj for the lda model,
        change the parts of speech to decide what
        you want to use as input for LDA"""
        ps = PorterStemmer()

        # find nound trunks
        nlp = en_core_web_sm.load()
        all_extracted = {}
        for k, v in cleaned_text.items():
            if bool(v['lyrics']) == True:
                # get noun, verb, adj
                doc = nlp(v['lyrics'])
                nouns = ' '.join(ps.stem(str(v)) for v in doc if v.pos_ is 'NOUN').split()
                verbs = ' '.join(ps.stem(str(v)) for v in doc if v.pos_ is 'VERB').split()
                adj = ' '.join(str(v) for v in doc if v.pos_ is 'ADJ').split()
                # noun_tr = ' '.join(str(v) for v in doc.noun_chunks).split()
                all_w = nouns + adj + verbs
                all_extracted[k] = all_w

        return all_extracted



class LDATopic:
    """Get topics."""

    def __init__(self, path, path_result, processed_text: typing.Dict[str, str], topic_num: int, alpha: int, eta: int):
        """Define varibles."""
        self.path = path
        self.path_result = path_result
        self.text = processed_text
        self.topic_num = topic_num
        self.alpha = alpha
        self.eta = eta

    def get_lda_score_eval(self, dictionary: typing.Dict[str, str], bow_corpus) -> list:
        """LDA model and coherence score."""
        lda_model = gensim.models.ldamodel.LdaModel(bow_corpus, num_topics=self.topic_num, id2word=dictionary, passes=10,  update_every=1, random_state = 300, alpha=self.alpha, eta=self.eta)
        # pprint(lda_model.print_topics())

        # get coherence score
        cm = CoherenceModel(model=lda_model, corpus=bow_corpus, coherence='u_mass')
        coherence = cm.get_coherence()
        print('coherence score is {}'.format(coherence))

        return lda_model, coherence

    def get_lda_score_eval2(self, dictionary: typing.Dict[str, str], bow_corpus) -> list:
        """LDA model and coherence score."""
        # lda_model = gensim.models.ldamodel.LdaModel(bow_corpus, num_topics=self.topic_num, id2word=dictionary, passes=10,  update_every=1, random_state = 300, alpha=self.alpha, eta=self.eta)

        # the trained model
        lda_model = LdaTransformer(num_topics=self.topic_num, id2word=dictionary, iterations=10, random_state=300, alpha=self.alpha, eta=self.eta, scorer= 'mass_u')

        # The topic distribution for each input document.
        docvecs = lda_model.fit_transform(bow_corpus)
        # pprint(lda_model.print_topics())

        return lda_model, docvecs

    def get_score_dict(self, bow_corpus, lda_model_object) -> pd.DataFrame:
        """
        get lda score for each document
        """
        all_lda_score = {}
        for i in range(len(bow_corpus)):
            lda_score = {}
            for index, score in sorted(lda_model_object[bow_corpus[i]], key=lambda tup: -1*tup[1]):
                lda_score[index] = score
                od = collections.OrderedDict(sorted(lda_score.items()))
            all_lda_score[i] = od
        return all_lda_score


    def topic_modeling(self):
        """Get LDA topic modeling."""
        # generate dictionary
        dictionary = gensim.corpora.Dictionary(self.text.values())
        bow_corpus = [dictionary.doc2bow(doc) for doc in self.text.values()]
        # modeling
        model, coherence = self.get_lda_score_eval(dictionary, bow_corpus)

        lda_score_all = self.get_score_dict(bow_corpus, model)

        all_lda_score_df = pd.DataFrame.from_dict(lda_score_all)
        all_lda_score_dfT = all_lda_score_df.T
        all_lda_score_dfT = all_lda_score_dfT.fillna(0)

        return model, coherence, all_lda_score_dfT, bow_corpus

    def topic_modeling2(self):
        """Get LDA topic modeling."""
        # generate dictionary
        dictionary = gensim.corpora.Dictionary(self.text.values())
        bow_corpus = [dictionary.doc2bow(doc) for doc in self.text.values()]
        # modeling
        model = self.get_lda_score_eval2(dictionary, bow_corpus)

        return model

    def format_topics_sentences(self, ldamodel, corpus):
        """Get output, get dominant topic for each document."""
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row_list in enumerate(ldamodel[corpus]):
            row = row_list[0] if ldamodel.per_word_topics else row_list
            # print(row)
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each doc
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
                else:
                    break

        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        return sent_topics_df

    def get_ids_from_selected(self, text: typing.Dict[str, str]):
        """Get unique id from text. """
        id_l = []
        for k, v in text.items():
            id_l.append(k)

        return id_l


def selected_best_LDA(path, outputP, text: typing.Dict[str, str], num_topic:int, outputFile:str):
        """Select the best lda model with extracted text 
        text: entities dictionary
        domTname:file name for the output
        """

        # convert data to dictionary format

        file_exists = os.path.isfile(outputP + 'lda_result_{}.csv'.format(outputFile))
        if not file_exists:
            f = open(outputP + 'lda_result_{}.csv'.format(outputFile), 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            if not file_exists:
                writer_top.writerow(['a'] + ['b'] + ['coherence'] + ['time'] + ['topics'] + ['num_topics'] )
                f.close()

        else:
            f = open(outputP + 'lda_result_{}.csv'.format(outputFile), 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            # alpha = [0.3]
            # beta = [0.9]
            # optimized alpha and beta
            alpha = [0.1, 0.3, 0.5, 0.7, 0.9]
            beta = [0.1, 0.3, 0.5, 0.7, 0.9]

            mydict = lambda: defaultdict(mydict)
            cohere_dict = mydict()
            for a in alpha:
                for b in beta:
                    # lda = LDATopic(text, num_topic, a, b)
                    lda = LDATopic(path=path, path_result=path_result, processed_text=text, topic_num=num_topic, alpha=a, eta=b)
                    model, coherence, scores, corpus = lda.topic_modeling()
                    cohere_dict[coherence]['a'] = a
                    cohere_dict[coherence]['b'] = b


            # sort result dictionary to identify the best a, b
            # select a,b with the largest coherence score
            sort = sorted(cohere_dict.keys())[0]
            a_opti = cohere_dict[sort]['a']
            b_opti = cohere_dict[sort]['b']

            # run LDA with the optimized values
            lda = LDATopic(path=path, path_result=path_result, processed_text=text, topic_num=num_topic, alpha=a_opti, eta=b_opti)
            model, coherence, scores_best, corpus = lda.topic_modeling()

            result_row = [[a, b, coherence, str(datetime.now()), model.print_topics(), num_topic]]
            writer_top.writerows(result_row)

            f.close()
            gc.collect()

            # select merge ids with the LDA topic scores
            # store result model with the best score
            id_l = lda.get_ids_from_selected(text)
            scores_best['song_id'] = id_l

            # get topic dominance
            df_topic_sents_keywords = lda.format_topics_sentences(model, corpus)
            df_dominant_topic = df_topic_sents_keywords.reset_index()

            sent_topics_df = pd.concat([df_dominant_topic, scores_best], axis=1)
            sent_topics_df.to_csv(outputP + 'dominance_{}_{}.csv'.format(outputFile, num_topic), encoding='utf-8-sig')

        return sent_topics_df



def get_dominant_topic(topic_df):
    """Get the most dominant topic."""
    dt = topic_df['Dominant_Topic'].value_counts().to_frame()
    dt['num'] = dt.index
    # get the most dominant topic
    dt_num = int(dt['num'].head(1))

    topic_kw = topic_df['Topic_Keywords'][topic_df['Dominant_Topic'] == dt_num]
    topic_kw = topic_kw.iloc[0]
    return dt_num, topic_kw


def get_topics_dominance(path_result:str, path_data:str, inputfile, num_topic, outputFile) -> pd.DataFrame:
    """Loop get topics."""
    
    sent_topics = selected_best_LDA(path=path_data, outputP=path_result, text=inputfile, num_topic=num_topic, outputFile=outputFile)
    dt_num, topic_kw = get_dominant_topic(sent_topics)

    # save most dominant topics 
    f = open(path_result + 'domance_output_{}_{}.csv'.format(outputFile, num_topic), 'a', encoding='utf-8-sig')
    writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
   # writer_top.writerow(['topic_number'] + ['keywords'])
    result_row = [[dt_num, topic_kw]]
    writer_top.writerows(result_row)
    f.close()
    

def loop_topics(path_result:str, path_data:str, inputfile:str, outputFile):
    """Filter data then loop topics """

    lyrics_file = pd.read_csv(path_data + inputfile)
    male = lyrics_file.loc[lyrics_file['gender'] == 'male']
    female = lyrics_file.loc[lyrics_file['gender'] == 'female']
    # filter file according to year (nan are filtered)
    lyrics_file['song_year'] = lyrics_file['year'].apply(lambda x: 0 if x is np.nan else str(x).split("-", 1)[0])
    lyrics_file['song_year'] = lyrics_file['song_year'].apply(lambda x: int(x))
    year = lyrics_file.loc[lyrics_file['song_year'] > 2019]

    # clean text before lda, input data choose the input data name
    pt = ProcessText(path_result=path_result, path_data=path_data, filename=inputfile, inputdata=year)
    cleaned_text = pt.simple_preprocess()
    entities = pt.extract_entities(cleaned_text)
        # print(take(10, entities.items()))

    for num_topic in evn['lda']['topics']:
        print('generating {} topics'.format(num_topic))
        g = get_topics_dominance(path_result=path_result, path_data=path, inputfile=entities, outputFile=outputFile, num_topic=num_topic)


#if __name__ == "__main__":

    #get_topic_season('Anxiety', 2020, 10) #year, xnum_topiclda_
#again, we can totally loop through a list of subreddit names
path = '/disk/data/share/s1690903/Lyrics_project_git/data/'
path_result = '/disk/data/share/s1690903/Lyrics_project_git/data/result/'
evn_path = '/disk/data/share/s1690903/Lyrics_project_git/get_data/'
evn = load_experiment(evn_path + 'parameters.yaml')
inputfile = 'hiphop_lyrics_partial.csv'
outputFile = 'test_short'

loop_topics(path_result=path_result, path_data=path, inputfile=inputfile, outputFile=outputFile)











