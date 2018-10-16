#! usr/bin/env python3
#zhan4158
import re
import csv
import time
import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def getTopYT100(search):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get("https://www.youtube.com/")
    searchBox = driver.find_element_by_css_selector("#search")
    searchBox.send_keys(search)
    searchBox.send_keys(Keys.ENTER)
    
    #search youtube for the stuff

    current_page_height = driver.execute_script("return document.documentElement.scrollHeight;")
    elems = []
    descr = []
    
    #get >100 elements

    while len(elems) <= 100:
        #scroll page to find 100 elements
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1) #pauses for a little to let it load
        new_height = driver.execute_script("return document.documentElement.scrollHeight;")
        elems = driver.find_elements_by_css_selector("#video-title.yt-simple-endpoint.style-scope.ytd-video-renderer")
        descr = driver.find_elements_by_css_selector("#description-text.style-scope.ytd-video-renderer")
        if new_height == current_page_height:
            break
        current_page_height = new_height
        
    #unable to find 100
    if len(elems) <= 100:
        print("unable to find 100 results using search queries")
        return None
    
    
    #parse elements for data using regex
    
    algorithm = re.compile(r'(.*) by (\w+) (.*) (\d+) views')
    list = []
    for i in range(0, 100):
        algorithm = re.compile(r'(.*) by (.*?) \d* [year|years|month|months|day|days|hour|hours|minute|minutes|second|seconds].* ([\d|,]*) views?')
        extract = algorithm.search(elems[i].get_attribute("aria-label"))
        if extract==None: #flag to help debug
            print("whoops i="+str(i)+" is where it failed. " +elems[i].get_attribute("aria-label"))
        list.append({'Title': extract.group(1), \
                     'Author': extract.group(2), \
                     'Views': extract.group(3), \
                     'Description': descr[i].text})
    #returning list of dictionaries as top 100 as output 
    return list

def writeToCSV(string, dicts):
    with open(string+'.csv','w') as filename:
        keys = dicts[0].keys()
        writer = csv.DictWriter(filename,fieldnames = keys,extrasaction='ignore',delimiter=',')
        writer.writerows(dicts)
        
#search and write AA speaker
AASpeakerList = getTopYT100("AA Speaker")
writeToCSV("AASpeakerFile", AASpeakerList)
#search motivational speaker
motivationalSpeakerList = getTopYT100("Motivational Speaker")
writeToCSV("motivationalSpeakerFile", motivationalSpeakerList)



