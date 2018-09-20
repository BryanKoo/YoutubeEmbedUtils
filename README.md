# YoutubeEmbedUtils
Utilities for embedding youtube videos.

This project is created for who want to embed youtube videos in his/her service or app.

There can be multiple videos for a content/book. So it is desirable to find a video of good quality.
Because quality of video is similar within a channel, quality videos can be searched with preferred channel list.  

After getting list of quality videos, it is needed to set a relation between contents and videos.
The relation can be determined by check how much portion of title words are the same for each content and each video.

Then it is needed to check availability of each video to provide stable playback functionality.
Check the article below to understand why it is needed.
https://youtube-eng.googleblog.com/2011/12/understanding-playback-restrictions_28.html
Developer key is needed to use the API.

## Software requirements and solutions
* search videos of preferred channels
  * Youtube provides API for searching videos of a channel
    * https://developers.google.com/youtube/v3/docs/search/list
    * Developer key is needed to use the API
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
* execute search_channel.py to get list of videos for each channel
  * with 1 argument for channel list file
    * it is a tab separated value text file with ANSI windows default encoding. (it is also called CP949 for Korean character encoding.)
    * the first column is serial number, the second column is channel name, the third or the forth column is channel id.
  * videos.tsv will be as the result of searching 
    * it is also a tab separated value text file with ANSI encoding.
    * channel name, channel id, video title, video url, video image urls are listed in the file
    
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
