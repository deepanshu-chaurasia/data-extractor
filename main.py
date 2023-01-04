import time
import re
from parsel import Selector
from selenium import webdriver
import mysql.connector as connector
from selenium.webdriver.firefox.options import Options
import pandas as pd


# Database Creation
class DBase:
    def __init__(self):
        self.conn = connector.connect(host='localhost', port='3306', user='dipanshudomainsa_da', password='#Dadc.23551',
                                      database='dipanshudomainsa_domain_an')

        query = "CREATE TABLE if not exists {}(CompanyName varchar(200) UNIQUE, Address varchar(600), Ratings varchar(" \
                "20), Total_Reviews varchar(20), Timings varchar(100), Website varchar(500), Phone_number varchar(" \
                "100), CID varchar(50))".format(title)
        cur = self.conn.cursor()
        cur.execute(query)
        print("Table Created")

    # Insert Data
    def insert_data(self, name, address, ratings, reviews, timings, link, phone, cid):
        query = "INSERT IGNORE INTO {}(CompanyName, Address, Ratings, Total_Reviews, Timings, Website, Phone_number, CID)" \
                "VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(title, name, address, ratings, reviews,
                                                                         timings, link,
                                                                         phone, cid)
        print(query)
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        print("Data added to DB")

    # Fetch Data
    def fetch_data(self):
        cur = self.conn.cursor()
        query = 'SELECT * FROM {}'.format(title)
        cur.execute(query)
        df = pd.DataFrame(cur.fetchall(),
                          columns=['CompanyName', 'Address', 'Ratings', ' Total_Reviews', 'Timings', 'Website',
                                   'Phone_number', 'CID'])
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df)

    # Drop Table
    def del_table(self):
        query = "DROP TABLE {}".format(title)
        cur = self.conn.cursor()
        cur.execute(query)
        print("Table {} Deleted".format(title))


# main code
keyword = input("Keyword: ")
location = input("Location: ")
title = keyword + "_" + location

db = DBase()
DRIVER_PATH = '/home/dipanshudomainsa/data_extractor/Firefox_Geckodriver/geckodriver'

options = Options()
options.add_argument("--lang=en")
options.add_argument("--headless")
driver = webdriver.Firefox(executable_path=DRIVER_PATH, options=options)


search = keyword + "+in+" + location
link_url = "https://www.google.com/maps/search/" + search

driver.get(link_url)

#time.sleep(3)
page_content = driver.page_source
response = Selector(page_content)
driver.quit()

links = []

for el in response.xpath('//div[contains(@aria-label, "Results for")]/div/div[./a]'):
    links.append(el.xpath('./a/@href').extract_first(''))

for url in links:
    options = Options()
    options.add_argument("--lang=en")
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=DRIVER_PATH, options=options)
    
    driver.get(url)

    time.sleep(3)
    page_content = driver.page_source
    ress = Selector(page_content)
    driver.quit()

    
    try:
        name = ress.xpath('//h1[contains(@class, "fontHeadlineLarge")]/span/text()').extract_first("").replace("'", "_")
    except:
        name = " "

    try:
        address = ress.xpath(
            '//button[contains(@aria-label, "Address")]/div/div[2]/div/text()').extract_first("").replace("'", "_")
    except:
        address = " "

    try:
        rating = ress.xpath('//div[contains(@class, "F7nice mmu3tf")]/span/span/span/text()').extract_first("")
    except:
        rating = " "

    try:
        reviews = ress.xpath('//div[contains(@class, "F7nice mmu3tf")]/span[2]/span/span/text()').extract_first("")
    except:
        reviews = " "

    try:
        timings = ress.xpath(
            '//div[contains(@class, "MkV9")]/div/span/span/span/text()').extract_first(
            "") + ress.xpath(
            '//div[contains(@class, "MkV9")]/div/span/span/span[2]/text()').extract_first(
            "").replace("⋅", "-")
    except:
        timings = " "


    try:
        web = ress.xpath(
            '//a[contains(@aria-label, "Website")]/@href').extract_first("")
    except:
        web = " "

    try:
        phone = ress.xpath('//button[contains(@aria-label, "Phone")]/div/div[2]/div/text()').extract_first("")
    except:
        phone = " "

    try:
        temp_cid = ress.xpath(
            '//a[contains(@aria-label, "Claim this business")]/@href').extract_first("")
        cid = temp_cid[re.search('fp=', temp_cid).end():re.search('&hl', temp_cid).start()]
    except:
        cid = " "

    db.insert_data(name, address, rating, reviews, timings, web, phone, cid)

db.fetch_data()
db.del_table()

