# Introduction

This repo contains data collection and data analysis for the lyrics project.

**Step 1**: We collected artist names from the website **Musicbrainz** (an open music encyclopedia that collects music metadata) and **Wikipedia** hip-hop artist list. Then we collected lyrics from **Genius.com**

**Step 2**: Data analysis
Topic analysis

## Artist List Source

* we retrieve artist lists from MusicBrainz (two search criteria) (N = 3787)

* Wikipedia hip-hop artist list https://en.wikipedia.org/wiki/List_of_hip_hop_musicians  (N = 1455, 943 different from MusicBrainz)

* merge two lists (N = 4726)

* list of artists and songs Becky compiled last time.
https://docs.google.com/spreadsheets/d/1QahDHH0Ls39FWFmDoocXQqkiFMtz2sU_9NoxoqPu3Mk/edit?usp=sharing

## Lyrics Source

We are using the *lyricsgenius* lib to query the API: https://pypi.org/project/lyricsgenius/

If we don't use a library, we would have to deal with low-level details with HTTP requests, data serialization, authentication, and rate limits. This could be time-consuming and prone to error. 

*lyricsgenus* lib allows us to:

1. Search lyrics given an author name (that's why we tried to define a list of authors last time, in order to find the authors, we went for billboard)
2. Search for a single song by the same artist
3. Search albums

One of the authors of this lib wrote a blog and mentioned a major problem of the lib:
https://towardsdatascience.com/song-lyrics-genius-api-dcc2819c29

we can get a list of artist names with this method lyricsgenius.Genius.search_artist(). 

# Files and folders

### script
musicbrainz.py search author list on *musicbrainz*

get_lyrics_by_author.py search lyrics by author using *LyricsGenus*

### parameters

all the parameters (search criteria) we used are in parameters.yaml

# DATA 

artist_list_all_tags.csv: artist list, max count (the most frequent tag of an artist), max_count(the number of the most frequent tag), begin (birthday)

### artist list 

rapper list from music brainz:

hiphop_rap.csv

wikipedia artist list:

wikipedia_hiphop_artists.csv


### lyrics file
hiphop_lyrics_partial.csv

hip_hop_artist_manysongs_lyrics.csv  (artists with many songs)

hip_hop_artist_all_lyrics.csv  (lyrics from all hiphop artists)

hip_hop_artist_all_lyrics3.csv (lyrics from hiphop artists on wikipedia, this list contain 944 artists, but we only manage to retrieve songs from 330 artists)


# Notes for Musicbrainz

Documentation: https://python-musicbrainzngs.readthedocs.io/en/latest/api/

Musicbrainz allows us to search the database according to tags and many other variables. Check the tags and search combination in https://musicbrainz.org/tags

**However, the filter function doesn't seem to work well in musicbrainz**

For example:

* Tag search doesn't work well in search_recordings

I added a filter list to refilter artist tags because I found the filter function in the api has a lot of missing cases, rock singers are often included in the list when I try to retrieve rap singers only.

* Filter country also has lots of missing cases

* Depending on what variables we want to get, we can retrieve more data if we do not filter out born year. (Need to discuss)


# Data Analysis 

## plot word count

plot_words.py: plot occurence of single/multiple words over years

plots stored in: data/result/plots

## TOPICS

getting topics with lyrics: topic_model2.py

We can filter lyrics according to artist gender, year ...

We obtain N topics from the lyrics, what information we have for topic?

lda_result_test.csv (result file: data/result) *coherence score measures how coherence the cluster is*

* We obtain values to represent the topics in each song. For example, song 1 contain: 0.01 Topic1...0.3 Topic 2

dominance_test.csv

* We obtain the dominant topic for each song

domance_output_test.csv   (result file: data/result)













