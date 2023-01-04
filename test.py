import time
import re
from parsel import Selector
from selenium import webdriver
import mysql.connector as connector
from selenium.webdriver.firefox.options import Options
import pandas as pd


# main code
'''
keyword = input("Keyword: ")
location = input("Location: ")
title = keyword + "_" + location
'''

DRIVER_PATH = '/home/dipanshudomainsa/data_extractor/Firefox_Geckodriver/geckodriver'
#webdriver.Firefox(executable_path=DRIVER_PATH)

options = Options()
#options.add_argument("--lang=en")
options.add_argument("--headless")
driver = webdriver.Firefox(executable_path=DRIVER_PATH, options=options)


search ="doctor+in+shimla"
link_url = "https://www.google.com/maps/search/" + search

driver.get(link_url)

#time.sleep(2)
page_content = driver.page_source
response = Selector(page_content)
driver.quit()

links = []

for el in response.xpath('//div[contains(@aria-label, "Results for")]/div/div[./a]'):
    links.append(el.xpath('./a/@href').extract_first(''))


results = []
for url in links:
    options = Options()
   # options.add_argument("--lang=en")
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=DRIVER_PATH, options=options)

    driver.get(url)

    time.sleep(3)
    page_content = driver.page_source
    ress = Selector(page_content)
    driver.quit()
    try:
        name = ress.css('h1 > span:nth-child(1)::text').get()
    except:
        name = "--"

   # try:
  #      address = ress.css('div.rogA2c > div.Io6YTe.fontBodyMedium::text').get().replace("'", "_")
 #   except:
#        address = "--"

    print(name)
    #print(address)
    results.append({'name': name})
    
'''
    try:
        rating = ress.xpath('//div[contains(@class, "F7nice mmu3tf")]/span/span/span/text()').extract_first("")
    except:
        rating = "--"

    try:
        reviews = ress.xpath('//div[contains(@class, "F7nice mmu3tf")]/span[2]/span/span/text()').extract_first("")
    except:
        reviews = "--"

    try:
        timings = ress.xpath(
            '//div[contains(@class, "MkV9")]/div/span/span/span/text()').extract_first(
            "") + ress.xpath(
            '//div[contains(@class, "MkV9")]/div/span/span/span[2]/text()').extract_first(
            "")
    except:
        timings = "--"
    try:
        web = ress.xpath(
            '//a[contains(@aria-label, "Website")]/@href').extract_first("")
    except:
        web = "--"

    try:
        phone = ress.xpath('//button[contains(@aria-label, "Phone")]/div/div[2]/div/text()').extract_first("")
    except:
        phone = "--"
    try:
        temp_cid = ress.xpath(
            '//a[contains(@aria-label, "Claim this business")]/@href').extract_first("")
        cid = temp_cid[re.search('fp=', temp_cid).end():re.search('&hl', temp_cid).start()]
    except:
        cid = "--"
    
 '''
     #results.append({'name': name, 'address': address})

print(pd.DataFrame.from_dict(results, orient='columns'))
display.stop()


