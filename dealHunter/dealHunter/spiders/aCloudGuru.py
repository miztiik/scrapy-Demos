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
# from pyvirtualdisplay import Display
from xvfbwrapper import Xvfb

import time

class dealHuntingSeleniumSpider(Spider):
    name = "dealHuntingSeleniumSpider"
    allowed_domains = [ "acloud.guru" ]

    def __init__(self, category=None, *args, **kwargs):

        # Xvfb -br -nolisten tcp -screen 0 1024x768x24 :1025

        # Set the web browser parameters to not show gui ( aka headless)
        # Ref - https://github.com/cgoldberg/xvfbwrapper    
        self.vdisplay = Xvfb(width=1280, height=720)
        self.vdisplay.start()

        self.driver = webdriver.Firefox()
        # self.driver.implicitly_wait(3)
        
        super(dealHuntingSpiderSelenium, self).__init__(*args, **kwargs)    

        self.start_urls = [ "https://acloud.guru/forums/all/s3" ]

    def parse(self, response):
        self.driver.get(response.url)
        
        time.sleep(45)
        
        items = []
        
        qText_XPATH = "//div[@class='discussion-list-entry-body']"
        qURL_XPATH = ".//a[@class='discussion-list-entry-title text-accent placeholder']"

        ## Example CSS href selection
        # div = self.driver.find_element_by_class_name('someclass')
        # div.find_element_by_css_selector('a').get_attribute('href')

        # self.driver.find_element_by_css_selector('.someclass a').get_attribute('href')

        qText_divs = self.driver.find_elements_by_xpath(qText_XPATH)

        for qText in qText_divs:

            # set for debugging, You can use 's' to step, 'n' to follow next line
            # pdb.set_trace()

            # print qText.get_attribute('outerHTML') 

            qURL_XPATH = ".//a[@class='discussion-list-entry-title text-accent placeholder']"
            qUrlList = qText.find_elements_by_xpath(qURL_XPATH)

            for qUrl in qUrlList:
                items.append(qUrl.get_attribute('href'))

        # Stop the browser & close the display
        self.driver.quit()
        self.vdisplay.stop()
        
        # return items