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
count = 0
cat_count = 0

category = driver.find_elements_by_xpath('//ul[@class="js-categories columns2-sm relative z1 inline-block block-sm w50-sm"]/li')

for cat in category:
    cat_id.append(cat.get_attribute('data-category')) 

cat_id = list(map(int,map(lambda x: re.findall('\d+',x)[0], cat_id[1:])))
cat_urls = [f'https://www.kickstarter.com/discover/advanced?state=successful&category_id={i}&sort=popularity&seed=2654646&page={n}' for i in cat_id for n in pages[1:]]

for sub_page in cat_urls:
    time.sleep(0.5)
    driver.get(sub_page)
    pro_urls = driver.find_elements_by_xpath('//div[@class="clamp-5 navy-500 mb3 hover-target"]/a')
    cat_count+=1
    print("No of category page parsed: %i" %(cat_count))

    for url in pro_urls:
        pro_href.append(url.get_attribute('href'))

for project in pro_href:
  pro_data = OrderedDict()
  time.sleep(1)
  driver.get(project)

  try:
    try:
      pro_data['project_Name'] = driver.find_element_by_xpath('//span[@class="relative"]/a').text
    except:
      pro_data['project_Name'] = driver.find_element_by_xpath('//div[@class="grid-col-10 grid-col-10-lg grid-col-offset-1-md block-md order2-md type-center"]/h2').text
  except:
    pro_data['project_Name'] = ""

  try:  
    try:
      pro_data['category_name'] = driver.find_elements_by_xpath('//div[@class="NS_projects__category_location ratio-16-9 flex items-center"]//a')[-1].text.strip('\n')
    except:
      pro_data['category_name'] = driver.find_elements_by_xpath('//div[@class="py2 py3-lg flex items-center auto-scroll-x"]/a/span')[-5].text
  except:
    pro_data['category_name'] = ""

  try:
    pro_data['funding_period_start'] = driver.find_elements_by_xpath('//div[@class="NS_campaigns__funding_period"]/p/time')[0].text
  except:
    pro_data['funding_period_start'] = "On Going Project"

  try:
    pro_data['funding_period_end'] = driver.find_elements_by_xpath('//div[@class="NS_campaigns__funding_period"]/p/time')[1].text
  except:
    pro_data['funding_period_end'] = "On Going Project"

  try:  
    pro_data['no_days'] = int(''.join(re.findall('\d+', "".join(re.findall('\(\d+', driver.find_elements_by_xpath('//div[@class="NS_campaigns__funding_period"]/p')[0].text)))))
  except:
    pro_data['no_days'] = "On Going Project"

  try:
    try:
      pro_data['starter_location'] = driver.find_elements_by_xpath('//div[@class="NS_projects__category_location ratio-16-9 flex items-center"]//a')[-2].text.strip('\n')
    except:
      pro_data['starter_location'] = driver.find_elements_by_xpath('//div[@class="py2 py3-lg flex items-center auto-scroll-x"]/a/span')[-4].text
  except:
    pro_data['starter_location'] = ""


  try:
    try:
      pro_data['currency'] = ''.join(re.findall('[^(\d|\s|,)]', driver.find_element_by_xpath('//div[@class="NS_campaigns__spotlight_stats"]/span').text))
    except:
      pro_data['currency'] = ''.join(re.findall('[^(\d|\s|,)]', driver.find_element_by_xpath('//span[@class="ksr-green-700 inline-block bold type-16 type-28-md"]/span').text))
  except:
    pro_data['currency'] = ""

  try:
    try:
      pro_data['money_pledged'] = int(''.join(re.findall('\d+', driver.find_element_by_xpath('//div[@class="NS_campaigns__spotlight_stats"]/span').text)))
    except:
      pro_data['money_pledged'] = int(''.join(re.findall('\d+', driver.find_element_by_xpath('//span[@class="ksr-green-700 inline-block bold type-16 type-28-md"]/span').text)))
  except:
    pro_data['money_pledged'] = ""

  try:
    try:
      pro_data['goal'] = int(''.join(re.findall('\d+', driver.find_element_by_xpath('//div[@class="type-12 medium navy-500"]/span[@class="money"]').text)))
    except:  
      pro_data['goal'] = int(''.join(re.findall('\d+', driver.find_element_by_xpath('//span[@class="block dark-grey-500 type-12 type-14-md lh3-lg"]/span[@class="inline-block-sm hide"]/span').text)))
  except:
    pro_data['goal'] = ""

  try:
    try:
      pro_data['no_backers'] = int(''.join(re.findall('\d+', driver.find_element_by_xpath('//div[@class="NS_campaigns__spotlight_stats"]/b').text)))
    except:
      pro_data['no_backers'] = int(''.join(re.findall('\d+', driver.find_element_by_xpath('//div[@class="block type-16 type-28-md bold dark-grey-500"]/span').text)))
  except:
    pro_data['no_backers'] = ""

  data_set.append(pro_data)
  count+=1
  print("No of page parsed: %i" %(count))

  if count%1000 == 0:
    df = pd.DataFrame(data_set)
    df.to_csv('kickstarter.txt')

print('Job Completed!')
df = pd.DataFrame(data_set)
df.to_csv('kickstarter.txt')

driver.quit()
