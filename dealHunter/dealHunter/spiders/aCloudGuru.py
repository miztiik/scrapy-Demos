#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from scrapy.item import Item, Field

# from scrapy.http import FormRequest
# from scrapy import log
# from scrapy.selector import HtmlXPathSelector
 
import pdb

# Imports for Scrapy spider
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field

# Imports for virtual display
from xvfbwrapper import Xvfb
from pprint import pprint

import time

# Imports for virtual browser  & wait conditions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class tspidy(Spider):
    name = "tspidy"
    allowed_domains = [ "acloud.guru" ]

    def __init__(self, filename=None):
        #self.start_urls = [ "https://acloud.guru/forums/all/s3" ]
        self.start_urls = [ "http://www.google.co.in# " ]

    def parse(self, response):

        self.setUpBrowser()

        queryLnks = []

        self.urlMetadata = {}

        self.urlMetadata['s3'] = { "url": "https://acloud.guru/forums/all/rds" ,"crawled": True, "pgCrawled" : 0 }
 
        queryLnks = self.collectUrls()

        print "\n===========Printing in mains=========\n"
        pprint(queryLnks)

        self.tearDownBrowser()

    """
    Function to setup the Browser
    """
    def setUpBrowser(self):
        # Set the web browser parameters to not show gui ( aka headless)
        # Ref - https://github.com/cgoldberg/xvfbwrapper    
        self.vdisplay = Xvfb(width=1280, height=720)
        self.vdisplay.start()

        self.driver = webdriver.Firefox()

    """
    Function to close the Browser
    """
    def tearDownBrowser(self):
        # Stop the browser & close the display
        self.driver.quit()
        self.vdisplay.stop()

    """
    Function to collect the Urls in a given page
    """
    def collectUrls(self):

        
        urlItems = []

        # The XPATH Location identifiers to make it configurable

        ## The XPATH ID of the element for which the the page load waits before processing other requests
        ec_XPATH = "//div/div[@class='discussion-list-entry-body']/div[@class='secondary-row']/a/span"

        qText_XPATH = "//div[@class='discussion-list-entry-body']"
        qURL_XPATH = ".//a[@class='discussion-list-entry-title text-accent placeholder']"

        # nxtPageBtn_XPATH = "//div[@class='clearfix p']/li[@class='paginate_button next']/a"

        # The time to wait for the webpage to laod in seconds
        pageLoadWaitTime = 10
        # Lets be nice and crawl only limited pages
        crawlPgLimit = 2
       
        # self.driver.get(self.urlMetadata['s3']['url'])
        self.driver.get("https://acloud.guru/forums/all/s3")
        
        time.sleep(pageLoadWaitTime)       
        
        while self.urlMetadata["s3"]["pgCrawled"] < crawlPgLimit:
            try:
    
                # Check if the page has the necessary elements before we start scraping
                
                print self.driver.find_elements_by_xpath(ec_XPATH)

                #element_present = WebDriverWait(self.driver, pageLoadWaitTime).until(EC.text_to_be_present_in_element_value((By.XPATH, ec_XPATH), "ago"))
                element_present = WebDriverWait(self.driver, pageLoadWaitTime).until(EC.presence_of_all_elements_located((By.XPATH, ec_XPATH)))

                # print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                # print element_present
                # print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

                # Find all the question div tags and iterate in for loop for the link reference
                qText_divs = self.driver.find_elements_by_xpath(qText_XPATH)
        
                for qText in qText_divs:

                    print "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    print qText.get_attribute('outerHTML') 
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
                    
                    
                    qUrlList = qText.find_elements_by_xpath(qURL_XPATH)
        
                    for qUrl in qUrlList:
                        urlItems.append(qUrl.get_attribute('href'))
                  
            except:
                print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                print "           THE PAGE DID NOT LOAD PROPERLY         "
                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                
    
            finally:
                print "all done"

                print self.driver.find_element_by_link_text('Next').get_attribute('outerHTML')
                
                self.urlMetadata["s3"]["pgCrawled"] += 1
                # self.driver.find_element_by_xpath(nxtPageBtn_XPATH).click()
                # self.driver.find_element_by_link_text('Next').click()
                #pdb.set_trace()
                print "\n~~~~~~~~~ Increment\n"
                print self.urlMetadata["s3"]["pgCrawled"]
                print "\n~~~~~~~~~ Incremented\n"
        
        return urlItems

    """
    Function to load Next Page
    """
    def loadNextPage(self):
        print("Function to be written")

class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)