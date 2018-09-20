<<<<<<< HEAD
#-*- coding: utf-8 -*-
# match title of youtube video and leedovoca books
# matching logic is primitive as of 2018/09
import codecs, chardet
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
  if len(sys.argv) < 3:
    print "run with 2 arguments for a book list and a video list"
    sys.exit()
  books = []
  series = []

  fp = open(sys.argv[1], 'rb')
  data = fp.read()
  fp.close()
  result = chardet.detect(data)
  print "book list input is ", result['encoding']
  if result['encoding'].startswith("UTF-8"):
    encoding_type = 'utf-8'
  else:
    encoding_type = 'cp949'

  blf = codecs.open(sys.argv[1], 'r', encoding=encoding_type)   # read book list of leedo
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

  fp = open(sys.argv[2], 'rb')
  data = fp.read()
  fp.close()
  result = chardet.detect(data)
  print "video list input is ", result['encoding']
  if result['encoding'].startswith("UTF-8"):
    encoding_type = 'utf-8'
  else:
    encoding_type = 'cp949'

  count = 0
  vlf = codecs.open(sys.argv[2], 'r', encoding=encoding_type)   # read video list (search result of the pre-defined channels)
  slash_pos = sys.argv[2].find("/")
  outfile = sys.argv[1][:-4] + sys.argv[2][slash_pos+1:-4] + ".tsv"
  vbf = codecs.open(outfile, 'w', encoding='cp949') # video-book match list
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
  print outfile, "created"
=======
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
>>>>>>> 2048b0a4d02cba6cb79750c2bca4350b84cc7343
