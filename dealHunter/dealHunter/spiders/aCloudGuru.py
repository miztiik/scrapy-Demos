#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from scrapy.item import Item, Field

# from scrapy.http import FormRequest
# from scrapy import log
# from scrapy.selector import HtmlXPathSelector
 
# import pdb

from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field

from selenium import webdriver
from pyvirtualdisplay import Display
from xvfbwrapper import Xvfb
from pprint import pprint

import time

class msgBoardScraper(Spider):
    name = "msgBoardScraper"
    allowed_domains = [ "acloud.guru" ]

    def __init__(self, category=None, *args, **kwargs):
        
        super(msgBoardScraper, self).__init__(*args, **kwargs)    

        # self.start_urls = [ "https://acloud.guru/forums/all/s3" ]
        self.start_urls = [ "https://acloud.guru/forums/all/rds" ]

    def parse(self, response):

        self.setUpBrowser()

        question_Urls = []
        question_Urls = self.collectUrls(response)

        print "\n===========Printing in mains=========\n"
        pprint(question_Urls)
        print "===========\n"

        self.tearDownBrowser()

    """
    Function to setup the Browser
    """
    def setUpBrowser(self):
        # Xvfb -br -nolisten tcp -screen 0 1024x768x24 :1025

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
    def collectUrls(self,response):
        
        urlItems = []

        # The XPATH Location identifiers to make it configurable
        qText_XPATH = "//div[@class='discussion-list-entry-body']"
        qURL_XPATH = ".//a[@class='discussion-list-entry-title text-accent placeholder']"
                                   
        # The time to wait for the webpage to laod in seconds
        pageLoadWaitTime = 45

        self.driver.implicitly_wait(pageLoadWaitTime) 
        self.driver.get(response.url)

        # self.driver.wait_for_page_to_load("45000")
        time.sleep(pageLoadWaitTime)
        
        # self.driver.find_element_by_id('login').click()

        try:

            # Example CSS href selection
            # div = self.driver.find_element_by_class_name('someclass')
            # div.find_element_by_css_selector('a').get_attribute('href')
    
            # self.driver.find_element_by_css_selector('.someclass a').get_attribute('href')
            qText_divs = self.driver.find_elements_by_xpath(qText_XPATH)
    
            for qText in qText_divs:
    
                # set for debugging, You can use 's' to step, 'n' to follow next line
                # pdb.set_trace()
    
                print qText.get_attribute('outerHTML') 
    
                
                qUrlList = qText.find_elements_by_xpath(qURL_XPATH)
    
                for qUrl in qUrlList:
                    urlItems.append(qUrl.get_attribute('href'))

        # with wait_for_page_load(self.driver):
        #    self.driver.find_element_by_link_text('my link').click()
                
        except:
            print "Could not find any Topics"
            

        finally:
            print "all done"
            return urlItems

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