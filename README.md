# YoutubeEmbedUtils
Utilities for embedding youtube videos.

This project is created for who wants to embed youtube videos in his/her service or app.
When a service needs to provide a youtube video related to some contents of the service, it is needed to selec a video with goodl quality among multiple videos for each content and it is time consuming and difficult.
To make this selection simple, it is better to know good channels because quality of videos is uniform within a channel.
Good channels can be found by searching youtube and watching videos and then checking videos of channels that is found in searched results.
It is assumed that good channels are already determined manually before using this utilities.

The first utility is for getting video list of channels. (titles and urls)

After getting list of videos from channels, it is needed to map relations between contents and videos.
The relation can be determined by check how much portion of title words are the same for each content and each video.

The second utility is for setting relation between titles of contents and videos.

Though videos related to the contents of the service is found, they can be disappeared from Youtube by some reason.
Any video is possible to be failed to play.

The third utility is for checking availability of each video.

It is done by checking 3 properties of a video: embeddable, regionRestriction, syndicated
Check the article below to understand why it is needed.
https://youtube-eng.googleblog.com/2011/12/understanding-playback-restrictions_28.html

## Software requirements and solutions
* search videos of preferred channels
  * Youtube provides API for searching videos of a channel
    * https://developers.google.com/youtube/v3/docs/search/list
    * Developer key is needed to use the API
  * If it is hard to gt a developer key then use scrape_channel.py
* match content and videos by comparing content/book titles and video titles
  * title matching algorithm should consider many exceptions. 
  * both titles can have writer/publisher name in it.
  * video titles can have additional marketing words as below.
    * A Read Aloud of "Fresh Fall Leaves" by Shari Halpern WITH SOUND ETTECTS - HD
* check a youtube video can be playbok (available, embeddable, region allowed, syndicated)
  * Youtube provides API for checking status of videos
    * https://developers.google.com/youtube/v3/docs/videos/list
    * Developer key is needed to use the API

## How to use
### Search channels for videos
* create /channel subdirectory where input file will be read and output file will be writed
  * /channel/ch.tsv can be an example of input file name
* execute search_channel.py to get list of videos for each channel if developer key is available, execute scrape_channel.py to get list of videos for each channel if developer key is not available
  * with 1 argument for channel list file
    * it is a tab separated value text file with ANSI (windows default) encoding.
    * ANSI encoding is also called CP949 for Korean character encoding.
    * the first column is serial number, the second column is channel name, the third or the forth column is channel id.
  * /channel/ch_videos.tsv will be as the result of searching (when input file was /channel/ch.tsv) 
    * it is also a tab separated value text file with utf-8 encoding.
    * utf-8 is the standard encoding of web resources nowadays and may be transcoded into ANSI manually.
    * channel name, channel id, video title, video url, video image url are listed in the file for search_channel.py
    * channel name, channel id, video title, video url, video length are listed in the file for scrape_channel.py
    
### Set relation between content/book and video by comparing titles
* execute match_title.py to get mapping between contents and videos
  * with 1 argument for content list file
  * it is a tab separated value text file with ANSI windows default encoding.
    * the first column is series title, the second column is content title
  * videos_book.tsv will be created as the result of matching
    * channel name, channel id, video title, video url, video image url, content/book title, match percentage are listed in the file
    
### Check availability of youtube videos
* execute check_video.py
  * with no argument or 1 argument for video list file
    * File selection GUI will be presented when no argument is given
