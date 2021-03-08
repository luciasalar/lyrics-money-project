#Collect Lyrics

We are using the lyricsgenius lib to query the API:
https://pypi.org/project/lyricsgenius/
If we don't use a lib, we would have to deal with low-level details with HTTP requests, data serialization, authentication, and rate limits. This could be time-consuming and prone to error. 

lyricsgenus lib allows you to:

1. Search lyrics given an author name (that's why we try to define a list of authors last time, in order to find the authors, we went for billboard)
2. Search for a single song by the same artist:
3. Search album

One of the authors of this lib wrote a blog and mentioned a major problem of the lib:
https://towardsdatascience.com/song-lyrics-genius-api-dcc2819c29

"A clear area for improvement is our process's dependence on a collection of artist names being passed to lyricsgenius.Genius.search_artist(). Manually creating a list of artist names is definitely not scalable. We only used three artists in our example, but to build a large enough dataset to fine-tune a production-caliber model, we'd ideally want dozens of artists and a much higher k variable.

The solution automates the task of creating the list of artists, one way being to scrape the names from one of two sources using bs4. Wikipedia provides several lists of musicians based on music genre and maybe a great, singular source to grab these artist names from."

So I guess the easiest way is to get a list of artist. I think this is the list of artists and songs Becky compiled last time.

https://docs.google.com/spreadsheets/d/1QahDHH0Ls39FWFmDoocXQqkiFMtz2sU_9NoxoqPu3Mk/edit?usp=sharing