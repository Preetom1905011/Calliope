import urllib.request
import bs4 as bs
import re
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from multiprocessing import Pool
import time

total_pages = 50
links_per_page = 20

def UrlExtract(batch_number):
    # Path for Chrome Driver
    path = "/opt/homebrew/bin/chromedriver"
    # Setting up the browser
    driver = webdriver.Chrome(executable_path = path)
    
    page_start = batch_number*total_pages + 1
    urls = []
    for i in range(0,total_pages):
        print(i+page_start) # For testing purposes only.
        
        site = "https://www.poetryfoundation.org/poems/browse#page=" + str(i+page_start) + "&sort_by=recently_added"
        driver.implicitly_wait(300) #the website might not finish loading
        time.sleep(10) #In case the above wait is not sufficient.
        driver.get(site) # Opening the website.
        html_source = driver.page_source # Loaded webpage html.
        
        #Creating beautiful soup object to parse the links.
        soup = bs.BeautifulSoup(html_source, features="html.parser")
    
        count = 0 #There are only 20 useful url links.
        #All the useful poem links have a format /poems/29393/[name]
        
        for aHref in soup.find_all("a",href=re.compile('.*/poems/[0-9]+/.*')):
            urls.append(aHref.get("href"))
            if(count==(links_per_page-1)): # 0 indexing.
                break
            count+=1

    np.savetxt("PoetryFoundationLinks/PoetryFoundationUrls"+str(page_start)+"-"+str(page_start+total_pages-1)+".txt", urls, fmt="%s")



if __name__ == '__main__':

    total_pages = 50 # Total number of pages we want to extract in a single file, each page consists of 20 poem links.
    links_per_page = 20 # After inspecting the webpage element.
    total_batches = 1 # Number of times we want to do the operation.
    start_batch_from = 1 # Because sometimes, I run the program for a small number of batches first.
    batch_iterable = list(range(start_batch_from,total_batches+start_batch_from))

    #multiprocessing with pool.
    print("start")
    p = Pool(processes = 1)
    p.map(UrlExtract,batch_iterable)
    p.terminate()
    print("end")