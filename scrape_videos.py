# search url, title, length of videos with a channel url
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os, pdb
import time

def parse_video_info(html):
  urls, titles, lengths = [], [], []
  soup = BeautifulSoup(html, 'html.parser')
  contents = soup.find("div", id="contents")
  if not contents:
    return [], [], []
  items = contents.find("div", id="items")
  if not items:
    return [], [], []
  videos = items.find_all("div", id="dismissable")
  for video in videos:
    urls.append("https://youtube.com" + video.h3.a['href'].strip())
    titles.append(video.h3.a['title'].strip())
    lengths.append(video.span.text.strip())
  return urls, titles, lengths

def scrape_videos_channel(ch_url):
  tokens = ch_url.split("/")
  ch_id = tokens[-1].strip()
  ch_videos_url = ch_url + "/videos"
  ch_videos_path = "searched/ch_videos_" + ch_id + ".html"

  if os.path.isfile(ch_videos_path):
    with open(ch_videos_path, "r") as fp:
      html = fp.read()
  else:
    print("crawl", ch_videos_url)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(3)

    driver.get(ch_videos_url)  

    # send END key while scrollHeight is increasing 
    height_n1 = 0
    for i in range(200):
      height = driver.execute_script("return document.documentElement.scrollHeight")
      if height == height_n1:
        break
      height_n1 = height
      #print "sending END at height", height, "counter", i, "length", len(driver.page_source)
      driver.find_element_by_tag_name('body').send_keys(Keys.END)
      time.sleep(3)

    html = driver.page_source
    with open(ch_videos_path, "w") as fp:
      fp.write(html)

    driver.quit()

  return parse_video_info(html)

if __name__ == "__main__":
  channel_id = "UCjqpjyVqqR20JMTMv1D1eYg"
  ch_url = "https://www.youtube.com/channel/" + channel_id
  urls, titles, lengths = scrape_videos_channel(ch_url)
  for i in range(len(urls)):
    print(i, lengths[i], titles[i], urls[i])
