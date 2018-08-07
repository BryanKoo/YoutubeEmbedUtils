#-*- coding: utf-8 -*-
# get video urls of given channel
# get screenshot
import codecs
import os
import sys
import pdb
reload(sys)
sys.setdefaultencoding('utf-8')

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyD7pL0Y_VD2SBN4oJt4_HciNaQcBA6bPeU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def is_hanja(ch):
  if ch >= '一' and ch <= '龥':
    return True
  return False

def has_hanja(text):
  for ch in text:
    if is_hanja(ch):
      return True
  return False

def filter_alpha(string):
  #string = string.encode("utf-8")
  for ch in string:
    if ch > '~':
      string = string.replace(ch, " ")
      string = string.replace("  ", " ")
  return string

def normalize_symbols(string):
  result = string.replace(u"\u2018", "'").replace(u"\u2019", "'")
  result = result.replace(u"\u2013", "-").replace(u"\u2014", "-")
  result = result.replace(u"\u201c", '"').replace(u"\u201d", '"')
  result = result.replace(u"\u2744", '*').replace(u"\u2764", '*')
  result = result.replace(u"\u26fa", '*')
  result = result.replace(u"\ufe0f", '')
  result = filter_alpha(result)
  return result

def youtube_search(ch_name, ch_id):
  titles = []
  ids = []
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

  num_items = 0
  search_response = youtube.search().list(channelId=ch_id, part="snippet", maxResults=50).execute()

  nextToken = search_response.get("nextPageToken")
  pageInfo = search_response.get("pageInfo")
  totalResult = pageInfo["totalResults"]
  count = len(search_response.get("items"))
  num_items += count
  print "got", str(num_items)

  # Add each result to the appropriate list, and then display the lists of matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      titles.append(normalize_symbols(search_result["snippet"]["title"]))
      ids.append(search_result["id"]["videoId"])
  
  while num_items < totalResult:
    search_response = youtube.search().list(channelId=ch_id, part="snippet", maxResults=50, pageToken=nextToken).execute()
    nextToken = search_response.get("nextPageToken")
    pageInfo = search_response.get("pageInfo")
    totalResult = pageInfo["totalResults"]
    count = len(search_response.get("items"))
    num_items += count
    print "got", str(num_items)
    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        titles.append(normalize_symbols(search_result["snippet"]["title"]))
        ids.append(search_result["id"]["videoId"])

  tsv = codecs.open("videos.tsv", 'a', encoding='cp949')
  for i in range(len(titles)):
    if has_hanja(titles[i]):
      print "hanja title"
      continue
    try:
      tsv.write(ch_name + "\t" + ch_id + "\t" + titles[i] + "\t" + "https://www.youtube.com/watch?v=" + ids[i] + "\t" + \
        "https://img.youtube.com/vi/" + ids[i] + "/0.jpg\n")
    except:
      pdb.set_trace()
  tsv.close()

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "run with 1 argument for input filename with CP949, windows default"
    sys.exit()
  ch_names = []
  ch_urls = []
  chf = codecs.open(sys.argv[1], 'r', encoding='cp949')
  while True:
    try:
      line = chf.readline()
    except:
      print "input file should be CP949 or ANSI"
      sys.exit()

    if not line: break
    line = line.strip()
    if line == "":
      continue
    tokens = line.split("\t")
    name = tokens[1]
    if tokens[3].startswith("https"):
      url = tokens[3]
    elif tokens[2].startswith("https"):
      url = tokens[2]
    else:
      print name, "wrong url", url
      continue
    if url.find("channel") < 0:
      print "wrong url", url
      continue
    ch_names.append(name)
    ch_urls.append(url)
  chf.close()

  tsv = codecs.open("videos.tsv", 'w', encoding='cp949')
  tsv.write("channel_name" + "\t" + "channel_id" + "\t" + "video_title" + "\t" + "video_url" + "\t" + "video_image" + "\n")
  tsv.close()

  for i in range(len(ch_names)):  
    ch_url = ch_urls[i]
    if not ch_url.startswith("http"): continue
    try:
      print ch_names[i]
      tokens = ch_url.split("/")
      if tokens[-1].find("videos") >= 0 or tokens[-1].find("featured") >= 0:
        ch_id = tokens[-2]
      else:
        ch_id = tokens[-1]
      youtube_search(ch_names[i], ch_id)
    except HttpError, e:
      print ch_names[i], "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
