#import modules and set up
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import time
import re
from bs4 import BeautifulSoup
import pprint
import os

searchkey = input('Search term: ')
library = input('which library? ')

browser = webdriver.Chrome()
browser.maximize_window() # Max the browser
wait = WebDriverWait(browser, 10)   # Wait for 10

#login LAVA Radio
browser.get('http://music.lavaradio.com/')
openlogin = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'loginP')))
openlogin.click() #click login
input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@class="accountInput"]')))
input.send_keys('********@*****.com')
input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@class="accountPsd"]')))
input.send_keys('**********')
submit = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="loginInButton telBtn"]')))
submit.click() #submit and login LAVA Radio
time.sleep(1)

#select library
if library == 'q':
    changelibrary = wait.until(EC.presence_of_element_located((By.XPATH, '//p[@class="libraryType"]'))).click()
    qlibrary = wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="libraryUl"]/li[2]'))).click()
    
#search first artist
input = browser.find_element_by_class_name('searchCriteria')
input.send_keys(searchkey)
searchsubmit = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="search"]'))).click()
time.sleep(1)
artist = wait.until(EC.presence_of_element_located((By.XPATH, '//li[@data-id="3"]'))).click()
time.sleep(1)
firstartist = wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="artistList"]/li[@class="artlistLi"]/p[@class="AlbumsNumber"]'))).click()
time.sleep(3)

#open album and parse
artistinfo = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/div/p[2]/span[1]'))).text
albumamount = re.findall(r"\d+\.?\d*", artistinfo)
limit = int(albumamount.pop())
index = 1
while index <= limit:
    openalbum = wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="artistDetalisList"]/li[{}]/p[@class="artistDetalis_nameInfo"]'.format(index)))).click()
    pagesource = browser.page_source
    soup = BeautifulSoup(pagesource, 'html.parser')
    links = soup.select('.play-Albumsinfo')
    export = []

    #filter function (still needs to debug)
    def filter(links):
        usable = []
        for ii, item in enumerate(links):
            ii = ii
            title = item.getText()
            u = '可用'
            if u in title:
                count = item.get('AblumsDetalisCount') 
                c = "-"
                if c in count:
                    usable.append({'title': title})      
        return usable

    flt = filter(links)
    if len(flt) > 0:
        export.append(browser.current_url)
    index += 1
    browser.back()
    time.sleep(2)
 
#export the links to a txt file
if len(export) > 0:
    expt = open('album.txt','w+')
    pprint.pprint(export, stream=expt)
    expt.close()
else:
    expt = open('album.txt','w+')
    pprint.pprint('nothing', stream=expt)
    expt.close()