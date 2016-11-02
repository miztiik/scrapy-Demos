#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb

# Imports for Scrapy spider
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field

# Imports for virtual display
from xvfbwrapper import Xvfb
from pprint import pprint

# Imports for virtual browser  & wait conditions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.remote_connection import LOGGER
# LOGGER.setLevel(logging.WARNING)

# Imports for hovering & clicking
from selenium.webdriver.common.action_chains import ActionChains

import time, httplib, json

# Imports for AWS Interaction
import boto3

class aCloudGuru_qUrlCollectorSpider(Spider):
    name = "aCloudGuru_qUrlCollectorSpider"
    allowed_domains = [ "acloud.guru" ]

    def __init__(self):
        self.start_urls = [ "http://www.google.co.in" ]

    def parse(self, response):

        self.setUpBrowser()

        dataDump = {}

        aCloudTopicUrls = {}

        aCloudTopicUrls['s3']  = { 'awsTag' : 's3' ,  'sourceUrl' : 'https://acloud.guru/forums/all/s3' , 'crawled': 'False', 'pgCrawled' : 0, 'crawlPgLimit' : '5' }
        aCloudTopicUrls['rds'] = { 'awsTag' : 'rds' , 'sourceUrl' : 'https://acloud.guru/forums/all/rds' ,'crawled': 'False', 'pgCrawled' : 0, 'crawlPgLimit' : '5' }
        aCloudTopicUrls['elb'] = { 'awsTag' : 'elb' , 'sourceUrl' : 'https://acloud.guru/forums/all/elb' ,'crawled': 'False', 'pgCrawled' : 0, 'crawlPgLimit' : '5' }
        aCloudTopicUrls['ec2'] = { 'awsTag' : 'ec2' , 'sourceUrl' : 'https://acloud.guru/forums/all/ec2' ,'crawled': 'False', 'pgCrawled' : 0, 'crawlPgLimit' : '5' }
        aCloudTopicUrls['vpc'] = { 'awsTag' : 'vpc' , 'sourceUrl' : 'https://acloud.guru/forums/all/vpc' ,'crawled': 'False', 'pgCrawled' : 0, 'crawlPgLimit' : '5' }
        aCloudTopicUrls['sns'] = { 'awsTag' : 'sns' , 'sourceUrl' : 'https://acloud.guru/forums/all/sns' ,'crawled': 'False', 'pgCrawled' : 0, 'crawlPgLimit' : '5' }
        aCloudTopicUrls['sqs'] = { 'awsTag' : 'sqs' , 'sourceUrl' : 'https://acloud.guru/forums/all/sqs' ,'crawled': 'False', 'pgCrawled' : 0, 'crawlPgLimit' : '5' }
        aCloudTopicUrls['sa-pro'] = { 'awsTag' : 'sa-pro' , 'sourceUrl' : 'https://acloud.guru/forums/aws-certified-solutions-architect-professional/all' ,'crawled': 'False', 'pgCrawled' : 0, 'crawlPgLimit' : '30' }

        # Lets be nice and crawl only limited pages
        try:
            dataDump = self.collectUrls(aCloudTopicUrls['sa-pro'])

            self.writeToFile(dataDump)
    
            # print "\n===========Printing in mains=========\n"
            # pprint(dataDump)
        except:
            print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            print "            Unable to get grab links              "
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                
        self.tearDownBrowser()

    """
    Function to setup the Browser
    """
    def setUpBrowser(self):
        # Set the web browser parameters to not show gui ( aka headless )
        # Ref - https://github.com/cgoldberg/xvfbwrapper    
        
        self.vdisplay = Xvfb(width=1280, height=720)
        self.vdisplay.start()

        self.driver = webdriver.Firefox()

    """
    Function to close the Browser
    """
    def tearDownBrowser(self):
        # Stop the browser & close the display

        # Although github says quit works, it throws me an error
        # Ref - https://github.com/SeleniumHQ/selenium/issues/1469
        self.driver.quit()
        self.vdisplay.stop()

    """
    Function to collect the Urls in a given page
    """
    def collectUrls(self,urlMetadata):
        urlItems = []

        # The XPATH Location identifiers to make it configurable

        ## The XPATH ID of the element for which the the page load waits before processing other requests
        ec_XPATH        = "//div/div[@class='discussion-list-entry-body']/div[@class='secondary-row']/a/span"
        qText_XPATH     = "//div[@class='discussion-list-entry-body']"
        qURL_XPATH      = ".//a[@class='discussion-list-entry-title text-accent placeholder']"
        qPopular_XPATH  = "//ul[@class='nav nav-tabs']/li[@heading='Most Popular']/a"
        # nxtPageBtn_XPATH = "//div[@class='clearfix p']/li[@class='paginate_button next']/a"

        # The time to wait for the webpage to laod in seconds
        pageLoadWaitTime = 30

        self.driver.set_page_load_timeout(pageLoadWaitTime)
        self.driver.get(urlMetadata['sourceUrl'])
        
        for crawlCount in range(int(urlMetadata['crawlPgLimit'])):
            try:
                # Check if the page has the necessary elements before we start scraping
                element_present_check_1 = WebDriverWait(self.driver, pageLoadWaitTime).until(EC.presence_of_all_elements_located((By.XPATH, ec_XPATH)))
                # element_present_check_2 = WebDriverWait(self.driver, pageLoadWaitTime).until(EC.text_to_be_present_in_element_value((By.XPATH, ec_XPATH), "ago"))
                
                # Move to the most popular questions Tab
                qPopularBtn = self.driver.find_element_by_xpath(qPopular_XPATH)
                self.driver.execute_script('arguments[0].click();', qPopularBtn)

                time.sleep(pageLoadWaitTime)

                # Find all the question div tags and iterate in for loop for the link reference
                qText_divs = self.driver.find_elements_by_xpath(qText_XPATH)
        
                for qText in qText_divs:
                    
                    qUrlList = qText.find_elements_by_xpath(qURL_XPATH)
        
                    for qUrl in qUrlList:
                        urlItems.append(qUrl.get_attribute('href'))

                urlMetadata['pgCrawled'] += 1

                print "\n\n\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                print "\t  All done in page : {0}, Lets go to page : {1}".format( (urlMetadata['pgCrawled'] - 1) , urlMetadata['pgCrawled'])
                print "\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
            
            except TimeoutException:
                self.driver.execute_script("window.stop();")
                print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                print "           THE PAGE DID NOT LOAD PROPERLY         "
                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

            except:
                print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                print "           THE PAGE DID NOT LOAD PROPERLY         "
                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                
            finally:
                crawlCount += 1
                nextBtn = self.driver.find_element_by_link_text('Next')
               
                # Wont work because of bug - https://github.com/SeleniumHQ/selenium/issues/2285
                # hover_over_nextBtn = self.driver.find_element_by_link_text('Next')
                # hover = ActionChains(self.driver).move_to_element(hover_over_nextBtn)
                # hover.perform()

                try:
                    # Asynchronous execution
                    # self.driver.execute_async_script('arguments[0].click();', nextBtn)
                    self.driver.execute_script('arguments[0].click();', nextBtn)
                except httplib.BadStatusLine:
                    print "\n\n\t\tERROR : FAILED - To click on 'Next' button to navigate to next page\n"
                    # pass
                    break

        # Unique the list
        urlItemsSet = set(urlItems)
        
        # Prepare data to be dumpted to file
        urlMetadata['pgCrawled'] = str( urlMetadata['pgCrawled'] )
        urlMetadata['uri'] = list(urlItemsSet)
        urlMetadata['crawled'] = 'True'
        urlMetadata['pageLoadWaitTime'] = pageLoadWaitTime
        return urlMetadata

    def writeToFile(self, dataDump):
        # pdb.set_trace()
        # dataDumpJson = json.dumps(dataDump)
        # with open('1acloudguru-%s.json' % dataDump['awsTag'], 'w') as f:
        #     f.write("%s" % dataDumpJson)

        with open('acloudguru-%s.json' % dataDump['awsTag'], 'w') as f:
            json.dump(dataDump, f, indent=4,sort_keys=True)
        

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