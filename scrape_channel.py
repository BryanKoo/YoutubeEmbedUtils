#-*- coding: utf-8 -*-
# find video urls and title of given channels from youtube
# find screenshot urls as well when using api
# find length when scraping
import codecs, chardet
import os
import sys
import pdb
from scrape_videos import scrape_videos_channel

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

# found duplication of video >> dedup with video id
def youtube_search(outfile, ch_name, ch_id, ch_url):

  urls, titles, lengths = scrape_videos_channel(ch_url)
  print("\t found", len(urls))
  tsv = codecs.open(outfile, 'a', encoding='utf-8')
  for i in range(len(titles)):
    if has_hanja(titles[i]):
      print("hanja title")
      continue
    try:
      tsv.write(ch_name + "\t" + ch_id + "\t" + titles[i] + "\t" + urls[i] + "\t" + lengths[i] + "\n")
    except:
      pdb.set_trace()
  tsv.close()

def read_channel_list(chfile):
  ch_names = []
  ch_urls = []

  fp = open(sys.argv[1], 'rb')
  data = fp.read()
  fp.close()
  result = chardet.detect(data)
  print("input is ", result['encoding'])
  if result['encoding'].startswith("UTF-8") or result['encoding'].startswith("utf-8"):
    encoding_type = 'utf-8'
  else:
    encoding_type = 'cp949'

  chf = codecs.open(sys.argv[1], 'r', encoding=encoding_type)   # read channel file
  while True:
    try:
      line = chf.readline()
    except:
      print("input file should be windows file (CP949 or or EUC-KR or ANSI encoding) or Unicode(utf-8)")
      sys.exit()

    if not line: break
    if line.strip() == "":
      continue
    tokens = line.split("\t")
    if len(tokens) < 4:
      print(len(tokens), "tokens:", line)
    ch_name = tokens[1].strip()
    if ch_name == "":
      ch_name = "Name Not Given"
    if tokens[2].startswith("https"):
      ch_url = tokens[2].strip()
    elif tokens[3].startswith("https"):
      ch_url = tokens[3].strip()
    else:
      print(ch_name, "wrong url", ch_url)
      continue
    if ch_url.find("channel") < 0:
      print("wrong url", ch_url)
      continue
    ch_names.append(ch_name)
    ch_urls.append(ch_url)
  chf.close()
  return ch_names, ch_urls

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("run with 1 arguments for a input channel list file that has channel names and urls")
    sys.exit()
  elif not sys.argv[1].endswith(".tsv") and not sys.argv[1].endswith(".csv") and not sys.argv[1].endswith(".txt"):
    print("input file should be tab separated text file and the extension should be tsv or csv or txt")
    sys.exit()

  ch_names, ch_urls = read_channel_list(sys.argv[1])

  outfile = sys.argv[1][:-4] + "_videos.tsv"

  for i in range(len(ch_names)):  
    ch_url = ch_urls[i]
    if not ch_url.startswith("http"): continue

    tokens = ch_url.split("/")
    if tokens[-1].find("videos") >= 0 or tokens[-1].find("featured") >= 0:
      ch_id = tokens[-2].strip()
    else:
      ch_id = tokens[-1].strip()
    print("search", i, len(ch_names), ch_names[i])
    youtube_search(outfile, ch_names[i], ch_id, ch_url)

  print(outfile, "created")
