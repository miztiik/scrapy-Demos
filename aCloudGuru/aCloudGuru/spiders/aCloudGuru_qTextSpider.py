#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb, json

import os.path
from datetime import datetime, date, time

# Imports for virtual display
from xvfbwrapper import Xvfb
from pprint import pprint

# Imports for virtual browser  & wait conditions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

# Imports for Scrapy spider
from scrapy.spiders import Spider

class aCloudGuru_qTextSpider(Spider):
    name = "aCloudGuru_qTextSpider"
    allowed_domains = [ "acloud.guru" ]

    def __init__(self, srcLnksJson=None):
        self.srcLnksJson = srcLnksJson
        self.start_urls = [ "http://www.google.co.in" ]

    def parse(self,response):

        self.setUpBrowser()

        if self.srcLnksJson:
            inputDir = os.path.abspath( __file__ + "/../../../")
            inputFileLoc = os.path.join( inputDir, "LnksToScrape" , self.srcLnksJson )
            with open( inputFileLoc , 'r' ) as f:
                uriData = json.load(f)
        else:

            print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            print "   Source Json file not mentioned, continuing with defaults, usage is as below"
            print "\n   scrapy crawl " + self.name + " -a srcLnksJson=<filename> "
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            
            uriData = { 'awsTag' : 'new' ,
                        "sourceUrl" : "https://acloud.guru/forums/aws-certified-solutions-architect-associate/newest?p=1", 
                        'uri' : ['https://acloud.guru/forums/aws-certified-solutions-architect-associate/discussion/-KgK9udGFWruTCDWVtxG/ec2_-_the_backbone_of_aws_--_e'] ,
                        'crawled': 'False',
                        'pgCrawled' : '0' ,
                        'pageLoadWaitTime' : '60'
                      }


        self.collectQueryText( uriData )

        self.tearDownBrowser()

    """
    Function to setup the Browser
    """
    def setUpBrowser(self):
        # Set the web browser parameters to not show gui ( aka headless )
        # Ref - https://github.com/cgoldberg/xvfbwrapper    
        
        # Disable below two lines to view the browser in action
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
        # self.vdisplay.stop()

    """
    Function to collect the Urls in a given page
    """
    def collectQueryText(self,uriDict):

        xpathDict = {}

        ## The XPATH ID of the element for which the the page load waits before processing other requests
        xpathDict['pgLoadConfirmElement']   = "//div[@class='discussion-card']/div[@class='discussion-card-title clearfix loaded']/h2"
        xpathDict['qText']                  = "//div[@id='questionDetailArea']/div[@class='gu-editor-view markdown-text']/p"
        xpathDict['qAnswer']                = "//div[@id='answerDetailArea']/div[@class='gu-editor-view markdown-text']"
        xpathDict['qTopic']                 = "//span[@class='ui-select-match']/span/span[@class='ui-select-match-item btn btn-default btn-xs']/span/span"
     

        self.driver.set_page_load_timeout( int(uriDict['pageLoadWaitTime']) )

        for lnkIndex,lnk in enumerate( uriDict['uri'] ):
            dataDump = {}
            dataDump['sourceUrl'] = lnk
            
            # Split the link from the end to get the title and use only the second part[1]
            dataDump['Title'] = lnk.rsplit("/",1)[1]

            # time.sleep( int( uriDict['pageLoadWaitTime']) )
    
            try:
                self.driver.get( lnk )

                element_present_check_1 = WebDriverWait( self.driver, int( uriDict['pageLoadWaitTime'] ) ).until( EC.presence_of_element_located( ( By.XPATH, xpathDict['pgLoadConfirmElement'] ) ) )
                qTexts      = self.driver.find_elements_by_xpath( xpathDict['qText']  )
                qAnswers    = self.driver.find_elements_by_xpath( xpathDict['qAnswer'])
                qTopics     = self.driver.find_elements_by_xpath( xpathDict['qTopic'] )
    
                # Collect the Question Text
                questionTxt = []
                for para in qTexts:
                    questionTxt.append( para.text )
                dataDump['Question'] = questionTxt
                
                # Collect the answers
                allAnswers = {}
                for ansIndex, ans in enumerate(qAnswers, 1):
                    answerTxt = []
                    ansPara = ans.find_elements_by_xpath( './/p' )
                    for para in ansPara:
                        answerTxt.append( para.text )
                    allAnswers['usr-{0}'.format(ansIndex)] = answerTxt
                dataDump['Answers'] = allAnswers
    
                # Collect if any tags are there
                questionTags = []
                for qTag in qTopics:
                    # print qTag.get_attribute('innerHTML')
                    # print qTag.text
                    questionTags.append( qTag.text )
                dataDump['Tags'] = questionTags


                dataDump['awsTag'] = uriDict['awsTag']
                # dataDump['pgCrawled'] = str( int(uriDict['pgCrawled']) + 1)
                dataDump['pgCrawled'] = "1"
                dataDump['crawled'] = "True"
                # dataDump['dateScraped'] = date.today().strftime("%Y-%m-%d") + "-" + datetime.now().strftime('%H-%M')
                dataDump['dateScraped'] = date.today().strftime("%Y-%m-%d")
                dataDump['pageLoadWaitTime'] = uriDict['pageLoadWaitTime']
    
                print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                print "  SUCCESSFULLY SCRAPPED : {0} of {1}, DUMPING DATA".format( lnkIndex , len(uriDict['uri']))
                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    
                self.writeToFile( dataDump )
    
            except TimeoutException:
                self.driver.execute_script("window.stop();")
                print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                print " TIMEOUT exceptions, THE PAGE DID NOT LOAD PROPERLY         "
                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

        return None

    def writeToFile(self, dataDump):
        outputDir = os.path.abspath(__file__ + "/../../../")
        outputFileName = '{0}-acloudguru-{1}.json'.format( dataDump['dateScraped'] , dataDump['awsTag'] )
        outputFileLoc = os.path.join( outputDir, "output" , outputFileName )

        with open( outputFileLoc , 'a') as f:
            json.dump(dataDump, f, indent=4,sort_keys=True)


# def main():
#     aCloudGuru_qTextSpider()
# 
# if __name__ == "__main__":
#     main()
