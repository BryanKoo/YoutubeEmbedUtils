#-*- coding: utf-8 -*-
# find video urls of given channels
# find screenshot urls as well
import codecs, chardet
import os
import sys
import pdb
reload(sys)
sys.setdefaultencoding('utf-8')

def dedup_searched(vfile):
  videos = []
  videos_hashed = {}
  fp = codecs.open(vfile, 'r', encoding='utf-8')
  while True:
    line = fp.readline()
    if not line: break
    tokens = line.split('\t')
    if len(tokens) == 2:
      line = line.strip() + "\t" + fp.readline()
    tokens = line.split('\t')
    img = tokens[-1]
    if img not in videos_hashed:
      videos.append(line)
      videos_hashed[img] = 1
  fp.close()
  return videos


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "run with 1 arguments for a input channel list file that has channel names and urls"
    sys.exit()
  elif not sys.argv[1].endswith(".tsv") and not sys.argv[1].endswith(".csv") and not sys.argv[1].endswith(".txt"):
    print "input file should be tab separated text file and the extension should be tsv or csv or txt"
    sys.exit()

  outfile = sys.argv[1][:-4] + "_videos.tsv"
  dedupped = dedup_searched(outfile)

  dfile = outfile + '.dedup'
  fp = codecs.open(dfile, 'w', encoding='utf-8')
  for line in dedupped:
    fp.write(line)
  fp.close()
