from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pdb
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(3)

#driver.get("https://www.youtube.com/results?search_query=fly+guy+there%27s+a+fly+guy+in+my+soup")  
channel_id = "UCjqpjyVqqR20JMTMv1D1eYg"
channel_videos_url = "https://www.youtube.com/channel/" + channel_id + "/videos"
driver.get(channel_videos_url)  

# send END key while scrollHeight is increasing 
height_n1 = 0
for i in range(20):
  height = driver.execute_script("return document.documentElement.scrollHeight")
  if height == height_n1:
    break
  height_n1 = height
  #print "sending END at height", height, "counter", i, "length", len(driver.page_source)
  driver.find_element_by_tag_name('body').send_keys(Keys.END)
  time.sleep(3)

html = driver.page_source
with open("searched/videos1.html", "w") as fp:
  fp.write(html.encode("utf-8"))

driver.quit()
