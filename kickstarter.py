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
    time.sleep(1)
    driver.get(sub_page)
    pro_urls = driver.find_elements_by_xpath('//div[@class="clamp-5 navy-500 mb3 hover-target"]/a')

    for url in pro_urls:
        pro_href.append(url.get_attribute('href'))

for project in pro_href:
  pro_data = OrderedDict()
  time.sleep(1)
  driver.get(project)

   pro_data['project_Name'] = driver.find_element_by_xpath('//span[@class="relative"]/a').text
   pro_data['category_name'] = driver.find_elements_by_xpath('//div[@class="NS_projects__category_location ratio-16-9 flex items-center"]//a')[-1].text.strip('\n')
   pro_data['funding_period_start'] = driver.find_elements_by_xpath('//div[@class="NS_campaigns__funding_period"]/p/time')[0].text
   pro_data['funding_period_end'] = driver.find_elements_by_xpath('//div[@class="NS_campaigns__funding_period"]/p/time')[1].text
   pro_data['no_days'] = int(''.join(re.findall('\d+', "".join(re.findall('\(\d+', driver.find_elements_by_xpath('//div[@class="NS_campaigns__funding_period"]/p')[0].text)))))
   pro_data['starter_location'] = driver.find_elements_by_xpath('//div[@class="NS_projects__category_location ratio-16-9 flex items-center"]//a')[-2].text.strip('\n')
   pro_data['currency'] = ''.join(re.findall('[^(\d|\s|,)]', driver.find_element_by_xpath('//div[@class="NS_campaigns__spotlight_stats"]/span').text))
   pro_data['money_pledged'] = int(''.join(re.findall('\d+', driver.find_element_by_xpath('//div[@class="NS_campaigns__spotlight_stats"]/span').text)))
   pro_data['goal'] = int(''.join(re.findall('\d+', driver.find_element_by_xpath('//div[@class="type-12 medium navy-500"]/span[@class="money"]').text)))
   pro_data['no_backers'] = int(''.join(re.findall('\d+', driver.find_element_by_xpath('//div[@class="NS_campaigns__spotlight_stats"]/b').text)))
  
  data_set.append(pro_data)

df = pd.DataFrame(data_set)
df.to_csv('kickstarter_1.txt')

driver.quit()
