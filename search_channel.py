#-*- coding: utf-8 -*-
# find video urls of given channels
# find screenshot urls as well
import codecs, chardet
import os
import sys
import pdb
reload(sys)
sys.setdefaultencoding('utf-8')

# install libary if not installed
# pip install --upgrade google-api-python-client
# pip install --upgrade oauth2client

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

with open("youtube_api.key") as fp:
  DEVELOPER_KEY = fp.readline().strip()
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
  result = result.replace(u"\u2605", '*')
  result = result.replace(u"\u30fb", '-')
  result = result.replace(u"\ufe0f", '')
  result = result.replace(u'\xa0', '')
  #result = filter_alpha(result)
  return result

def youtube_search(outfile, ch_name, ch_id):
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

  #tsv = codecs.open(outfile, 'a', encoding='cp949')
  tsv = codecs.open(outfile, 'a', encoding='utf-8')
  for i in range(len(titles)):
    if has_hanja(titles[i]):
      print "hanja title"
      continue
    try:
      tsv.write(ch_name + "\t" + ch_id + "\t" + titles[i] + "\t" + "https://www.youtube.com/watch?v=" + ids[i] + "\t" + \
        "https://img.youtube.com/vi/" + ids[i] + "/0.jpg\n")  # 0 is the original-sized image
    except:
      pdb.set_trace()
  tsv.close()

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "run with 1 arguments for a input channel list file that has channel names and urls"
    sys.exit()
  elif not sys.argv[1].startswith("channel") and not sys.argv[1].startwith("./channel"):
    print "input file should be located in ./channel/"
    sys.exit()
  elif not sys.argv[1].endswith(".tsv") and not sys.argv[1].endswith(".csv") and not sys.argv[1].endswith(".txt"):
    print "input file should be tab separated text file and the extension should be tsv or csv or txt"
    sys.exit()
  ch_names = []
  ch_urls = []

  fp = open(sys.argv[1], 'rb')
  data = fp.read()
  fp.close()
  result = chardet.detect(data)
  print "input is ", result['encoding']
  if result['encoding'].startswith("UTF-8"):
    encoding_type = 'utf-8'
  else:
    encoding_type = 'cp949'

  chf = codecs.open(sys.argv[1], 'r', encoding=encoding_type)   # read channel file
  while True:
    try:
      line = chf.readline()
    except:
      print "input file should be windows file (CP949 or or EUC-KR or ANSI encoding) or Unicode(utf-8)"
      sys.exit()

    if not line: break
    line = line.strip()
    if line == "":
      continue
    tokens = line.split("\t")
    ch_name = tokens[1]
    if tokens[3].startswith("https"):
      ch_url = tokens[3]
    elif tokens[2].startswith("https"):
      ch_url = tokens[2]
    else:
      print ch_name, "wrong url", ch_url
      continue
    if ch_url.find("channel") < 0:
      print "wrong url", ch_url
      continue
    ch_names.append(ch_name)
    ch_urls.append(ch_url)
  chf.close()

  outfile = sys.argv[1][:-4] + "_videos.tsv"
  #tsv = codecs.open(outfile, 'w', encoding='cp949')
  tsv = codecs.open(outfile, 'w', encoding='utf-8')
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
      youtube_search(outfile, ch_names[i], ch_id)
    except HttpError, e:
      print ch_names[i], "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
  print outfile, "created"
