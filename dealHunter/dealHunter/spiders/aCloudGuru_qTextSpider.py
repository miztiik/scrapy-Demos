#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb, time

# Imports for Scrapy
from scrapy.spiders import Spider
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


import json

class aCloudGuru_qTextSpider(Spider):
    name = "aCloudGuru_qTextSpider"
    allowed_domains = [ "acloud.guru" ]

    def __init__(self):
        self.start_urls = [ "http://www.google.co.in" ]

    def parse(self, response):

        self.setUpBrowser()

        uriData = {}

        uriData['s3']   = { 'awsTag' : 's3' , 'sourceUrl' : 'https://acloud.guru/course/aws-certified-solutions-architect-professional/discuss/-KPOrhtqq52941y0Iy6A/choose-2-answers-vpc' ,  'crawled': 'False', 'pgCrawled' : 0 , 'pageLoadWaitTime' : 60 }
        uriData['elb']  = { 'awsTag' : 'elb' , 'sourceUrl' : 'https://acloud.guru/course/aws-certified-solutions-architect-professional/discuss/-KAmC01FWYI1WnCgpWaT/elb-design-patterns' ,  'crawled': 'False', 'pgCrawled' : 0 , 'pageLoadWaitTime' : 60 }

        dataDump = {}

        for key in uriData.iterkeys():
            # dataDump = self.collectQueryText(uriData['s3'])
            # self.writeToFile(dataDump)
            self.writeToFile( self.collectQueryText( uriData[key] ) )

        # dataDump = self.collectQueryText(uriData['elb'])

        self.tearDownBrowser()

    """
    Function to setup the Browser
    """
    def setUpBrowser(self):
        # Set the web browser parameters to not show gui ( aka headless )
        # Ref - https://github.com/cgoldberg/xvfbwrapper    
        
        # self.vdisplay = Xvfb(width=1280, height=720)
        # self.vdisplay.start()

        self.driver = webdriver.Firefox()

    """
    Function to close the Browser
    """
    def tearDownBrowser(self):
        # Stop the browser & close the display

        # Although github says quit works, it throws me an error
        # Ref - https://github.com/SeleniumHQ/selenium/issues/1469
        self.driver.quit()
        # self.vdisplay.stop()

    """
    Function to collect the Urls in a given page
    """
    def collectQueryText(self,uriDict):
        # The time to wait for the webpage to laod in seconds
        

        ## The XPATH ID of the element for which the the page load waits before processing other requests
        ec_XPATH        = "//div[@class='card discussion-card']/div[@class='discussion-card-title loaded']/h2"
        qText_XPATH     = "//div[@id='questionDetailArea']/div[@class='gu-editor-view markdown-text']/p"
        qAnswer_XPATH   = "//div[@id='answerDetailArea']/div[@class='gu-editor-view markdown-text']"
        qTopic_XPATH    = "//div[@class='w-full ui-select-container ui-select-multiple ui-select-bootstrap dropdown form-control ng-valid']/div/span[@class='ui-select-match']/span"
     

        self.driver.set_page_load_timeout(uriDict['pageLoadWaitTime'])
        self.driver.get(uriDict['sourceUrl'])

        # time.sleep(uriDict['pageLoadWaitTime'])

        try:
            # pdb.set_trace()
            # element_present_check_1 = WebDriverWait(self.driver, uriDict['pageLoadWaitTime']).until(EC.presence_of_all_elements_located((By.XPATH, ec_XPATH)))
            element_present_check_1 = WebDriverWait(self.driver, uriDict['pageLoadWaitTime']).until(EC.presence_of_element_located((By.XPATH, ec_XPATH)))
            qTexts = self.driver.find_elements_by_xpath(qText_XPATH)
            qAnswers = self.driver.find_elements_by_xpath(qAnswer_XPATH)
            qTopics = self.driver.find_elements_by_xpath(qTopic_XPATH)

            
            questionTxt = []
            for para in qTexts:
                questionTxt.append( para.text )
            uriDict['Question'] = questionTxt
            
            allAnswers = {}

            for index, ans in enumerate(qAnswers, 1):
                answerTxt = []
                ansPara = ans.find_elements_by_xpath('.//p')
                for para in ansPara:
                    answerTxt.append( para.text )
                allAnswers['usr-{0}'.format(index)] = answerTxt
            uriDict['Answers'] = allAnswers

            questionTags = []
            for qTag in qTopics:
                # print qTag.get_attribute('innerHTML')
                # print qTag.text
                questionTags.append( qTag.text )
            uriDict['Tags'] = questionTags

            uriDict['pgCrawled'] = str( uriDict['pgCrawled'] + 1)
            uriDict['crawled'] = "True"

        except TimeoutException:
            self.driver.execute_script("window.stop();")
            print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            print "           THE PAGE DID NOT LOAD PROPERLY         "
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

        return uriDict

    def writeToFile(self, dataDump):
        with open('acloudguru-{0}-{1}.json'.format( dataDump['awsTag'] , dataDump['Tags'][0] ), 'w') as f:
            json.dump(dataDump, f, indent=4,sort_keys=True)