#-*- coding: utf-8 -*-
# match title of video and book
import codecs
import os
import sys
import pdb
reload(sys)
sys.setdefaultencoding('utf-8')

def normalize_symbol(line):
  line = line.replace("." , " ")
  line = line.replace("-" , " ")
  line = line.replace("/" , " ")
  line = line.replace("   " , " ")
  line = line.replace("  " , " ")
  return line

def get_same_word_score(vtext, btext):
  num_same = 0
  vtext = normalize_symbol(vtext)
  btext = normalize_symbol(btext)
  swords = {}
  vwords = vtext.split(" ")
  bwords = btext.split(" ")
  for bword in bwords:
    bword = bword.lower()
    for vword in vwords:
      vword = vword.lower()
      if bword == vword and bword not in swords:
        swords[bword] = 1
        num_same += 1
        break
  return num_same, len(bwords)

def find_book(vtitle):
  max_score = 0
  max_total = 0
  matched_book = ""
  for book in books:
    score, total = get_same_word_score(vtitle, book)
    if score > max_score:
      max_score = score
      max_total = total
      matched_book = book
  return max_score, max_total, matched_book

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "run with 1 argument for book list filename"
    sys.exit()
  books = []
  series = []
  blf = codecs.open(sys.argv[1], 'r', encoding='cp949')
  while True:
    line = blf.readline()
    if not line: break
    line = line.lower().strip()
    if line == "":
      continue
    tokens = line.split("\t")
    books.append(tokens[1])
    series.append(tokens[2])
  blf.close()

  count = 0
  vlf = codecs.open("videos.tsv", 'r', encoding='cp949')
  vbf = codecs.open("videos_books.tsv", 'w', encoding='cp949')
  line = vlf.readline()
  vbf.write("channel_name" + "\t" + "channel_id" + "\t" + "video_title" + "\t" + "video_url" + "\t" + "video_image" + "\t" + "book_title" + "\t" + "percentage" + "\n")
  while True:
    line_org = vlf.readline()
    if not line_org: break
    line = line_org.lower().strip()
    if line == "":
      continue
    tokens = line.split("\t")
    vtitle = tokens[2]
    count += 1
    score, total, book = find_book(vtitle)
    if total == 0:
      print "!", count, vtitle
      vbf.write(line_org.strip() + "\t" + book + "\t" + "0" + "\n")
    else:
      print count, vtitle
      vbf.write(line_org.strip() + "\t" + book + "\t" + str(score * 100 / total) + "\n")
  vlf.close()
  vbf.close()
