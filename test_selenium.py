from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pdb
import time

#browser = webdriver.Firefox()
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(3)

#driver.get("https://www.youtube.com/results?search_query=fly+guy+there%27s+a+fly+guy+in+my+soup")  
driver.get("https://www.youtube.com/channel/UCjqpjyVqqR20JMTMv1D1eYg/videos")  

# height will be increasing until the end
for i in range(20):
  height = driver.execute_script("return document.documentElement.scrollHeight")
  print "sending END at height", height, "counter", i, "length", len(driver.page_source)
  driver.find_element_by_tag_name('body').send_keys(Keys.END)
  time.sleep(3)

html = driver.page_source
with open("searched/videos1.html", "w") as fp:
  fp.write(html.encode("utf-8"))
driver.quit()
