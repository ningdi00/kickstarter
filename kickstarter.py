from selenium import webdriver
import re
import pandas as pd
import time
from collections import OrderedDict

driver = webdriver.Chrome()
driver.get('https://www.kickstarter.com/discover/advanced?state=successful&sort=popularity&seed=2657647&page=1')

data_set = []
cat_id = []
pro_href = []
pages = list(range(201))

category = driver.find_elements_by_xpath('//ul[@class="js-categories columns2-sm relative z1 inline-block block-sm w50-sm"]/li')

for cat in category:
    cat_id.append(cat.get_attribute('data-category')) 

cat_id = list(map(int,map(lambda x: re.findall('\d+',x)[0], cat_id[1:])))
cat_urls = [f'https://www.kickstarter.com/discover/advanced?state=successful&category_id={i}&sort=popularity&seed=2654646&page={n}' for i in cat_id for n in pages[1:]]

for sub_page in cat_urls[0:501]:
  pass

driver.quit()
