# BookTube
Find read-along video in youtube

It is very nice way of education for children to listen to storybook read-along.
This project is created for who has storybook list and want to find videos for it.
There can be multiple read-along videos for a book and it is desirable to find a video of good quality.
Preferred channel list should be prepared first by searching youtube for some books.

## Software requirements
* search videos of preferred channel
* match book and videos by compareing book titles and video titles

## How to use
* input a text file where preferred channel's id are listed
  * channel id is the last part of a channel's home url
  * For example, UCpIFBuCpJRJeYTrB2sGGGqw is the id of the channel named Animated Children's Book whose home url is  https://www.youtube.com/channel/UCpIFBuCpJRJeYTrB2sGGGqw

## Youtube Data API
Google provides API for searching videos of a channel.
https://developers.google.com/youtube/v3/docs/search/list?hl=ko
