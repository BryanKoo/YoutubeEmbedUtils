# BookTube
Find read-along video in youtube

It is very nice way of education for children to listen to storybook read-along.
This project is created for who has storybook list and want to find videos for it.
There can be multiple read-along videos for a book and it is desirable to find a video of good quality.
Preferred channel list should be prepared first by searching youtube for some books.

## Software requirements
* search videos of preferred channels
  * Google provides API for searching videos of a channel.
  * https://developers.google.com/youtube/v3/docs/search/list?hl=ko
  * developer key is needed to use the API
* match book and videos by comparing book titles and video titles
  * both titles may have writer name in it.
  * video titles may have additional marketing words.
    * A Read Aloud of "Fresh Fall Leaves" by Shari Halpern WITH SOUND ETTECTS - HD

## How to use
* prepare a text file where preferred channel's name and id are listed
  * channel name is not need for the search but need for easy recognition
  * channel id is the last part of a channel's home url
  * For example, UCpIFBuCpJRJeYTrB2sGGGqw is the id of the channel named Animated Children's Book whose home url is  https://www.youtube.com/channel/UCpIFBuCpJRJeYTrB2sGGGqw
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
    * matching 
