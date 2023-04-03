import urllib.request
import bs4 as bs
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


url = "https://www.poetryfoundation.org/poems/150097"
hdr = {'User-Agent':'Mozilla/5.0'}
req = urllib.request.Request(url,headers=hdr)
sauce = urllib.request.urlopen(req).read()
soup = bs.BeautifulSoup(sauce,'html.parser') #Beautiful Soup object

# Reformats the string into readable text.
def pretty_text(text):
    final = (((text).replace(u'\xa0', u' ')).replace(u'\r ',u'\n'))
    return final

def parse(url):
    # Data Extraction from the url.
    poem = (pretty_text(soup.find_all('div', class_="o-poem")[0].text))

    title = soup.find_all('h1')[0].text

    poet = soup.find_all('a', href=re.compile('.*poets/.*'))[0].text

    tags = soup.find_all('a', href=re.compile('.*topics.*'))
    tags = [tag.text for tag in tags]
    tags = ",".join(tags)

    return (title, poem, poet, tags)

print(parse(url))
