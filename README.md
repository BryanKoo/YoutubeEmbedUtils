# YoutubeEmbedUtils
Utilities for embedding youtube videos.

This project is created for who want to embed youtube videos in his/her service or app.

There can be multiple videos for a topic and it is desirable to find a video of good quality.
Because quality of video is similar within a channel, 
quality videos can be searched with preferred channel list.  

After getting list of videos, it is needed to set a relation between topics and videos.
The relation can be determined by check how much portion of title words are the same for topic and video.

Is is needed to check availability of each video to provide stable playback functionality.
Check the article below to understand why it is needed.
https://youtube-eng.googleblog.com/2011/12/understanding-playback-restrictions_28.html
Developer key is needed to use the API.

## Software requirements and solutions
* check a video cab be playbok (available, embeddable, region allowed, syndicated)
  * Youtube provides API for checking status of videos
    * https://developers.google.com/youtube/v3/docs/videos/list
* search videos of preferred channels
  * Youtube provides API for searching videos of a channel
    * https://developers.google.com/youtube/v3/docs/search/list
* match book and videos by comparing book titles and video titles
  * title matching algorithm should consider many exceptions. 
  * both titles can have writer name in it.
  * video titles can have additional marketing words as below.
    * A Read Aloud of "Fresh Fall Leaves" by Shari Halpern WITH SOUND ETTECTS - HD

## How to use
* execute search_channel.py to get list of videos for each channel
  * with 1 argument for channel list file
    * it is a tab separated value text file with ANSI windows default encoding. (it is also called CP949 for Korean character encoding.)
    * the first column is serial number, the second column is channel name, the third or the forth column is channel id.
  * videos.tsv will be as the result of searching 
    * it is also a tab separated value text file with ANSI encoding.
    * channel name, channel id, video title, video url, video image urls are listed in the file
* execute match_title.py to get mapping between books and videos
  * with 1 argument for book list file
  * it is a tab separated value text file with ANSI windows default encoding.
    * the first column is series title, the second column is book title
  * videos_book.tsv will be created as the result of matching
    * channel name, channel id, bideo title, video url, video image url, book title, match percentage are listed in the file
