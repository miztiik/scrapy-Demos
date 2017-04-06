# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
import os.path, pdb, datetime, json
from datetime import datetime, date, time

class EdxItem(scrapy.Item):
    postData    = scrapy.Field()

class awsForumsEdxSpider (scrapy.Spider):
    name = "awsForumsEdxSpider"
    allowed_domains = ["forums.aws.amazon.com"]

    xpathDict = {}

    xpathDict['lnks']           = "//div[@class='jive-table']/table/tbody/tr/td/a"
    xpathDict['lnkText']        = ".//@href"
    xpathDict['title']          = "//span[@class='jive-subject']/text()"
    xpathDict['content']        = "//div[@class='jive-message-body']/div"
    xpathDict['question']       = ".//text()"

    
    # Create the List of URLs to crawl
    # EC2
    start_urls = ['https://forums.aws.amazon.com/forumfilter.jspa?forumID=30&filter=answered&start=%d' %(n) for n in range(0,150,25)]
    # S3
    # start_urls = ['https://forums.aws.amazon.com/forumfilter.jspa?forumID=24&filter=answered&start=%d' %(n) for n in range(0,150,25)]
    # VPC
    # start_urls = ['https://forums.aws.amazon.com/forumfilter.jspa?forumID=58&filter=answered&start=%d' %(n) for n in range(0,150,25)]

    # awsForumUrls['sa-pro-new']   = { 'awsTag' : 'sa-pro-new','sourceUrl' : 'https://acloud.guru/forums/aws-certified-solutions-architect-associate/newest?p=1' ,'crawled': 'False', 'pgCrawled' : 0, 'crawlPgLimit' : '10', 'pageLoadWaitTime' : '25'  }

    def parse(self, response):
        # Extract the URLs to the post titles from the HTML Content
        for url in response.xpath( self.xpathDict['lnks'] ):
            qaUri = ( "https://forums.aws.amazon.com/" + url.xpath( self.xpathDict['lnkText'])[0].extract() ).encode('utf-8')
            yield scrapy.Request( qaUri , callback = self.lnkDataExtractor )

    # Lets parse the scraped items
    def lnkDataExtractor(self, response):

        qaDataDict = {}
        # Question & Answer - Scraping
        # All content is in P tags,
        qaData = response.xpath( self.xpathDict['content'] )

        # Add the problem statement
        #pdb.set_trace()
        qaDataDict['Title'] = ''.join( response.xpath( self.xpathDict['title'] )[1].extract() ).encode('utf-8')
        qaDataDict['Question'] = ' '.join( qaData[0].xpath( self.xpathDict['question'] ).extract() ).encode('utf-8')

        # Collect the answers
        allAnswers = {}
        # Pop the question element match
        del qaData[0]
        for ansIndex, ans in enumerate( qaData, 1 ):
            answerTxt = []
            para = ''.join( ans.xpath('.//text()').extract() ).encode('utf-8')

            para = ' '.join( para.split() )

            para.replace( "’" , "'"  )
            para.replace( "“" , "'"  )
            para.replace( "”" , "'"  )
            para.replace( "—" , "-"  )
            para.replace( "–" , "-"  )
            para.replace( "•" , "-"  )
            para.replace( "*" , "-"  )
            para.replace( "\"", "'"  )
            para.replace( "\\", "\\\\")
            para.replace( "%" , "\%" )
            para.replace( "&" , "and" )

            answerTxt.append( para )
            allAnswers['usr-{0}'.format(ansIndex)] = answerTxt
        qaDataDict['Answers'] = allAnswers


        # Strip special characters that break LaTEX
        qaDataDict['Title']     = ' '.join( qaDataDict['Title'].split() )
        qaDataDict['Title']     = qaDataDict['Title'].replace( "_" , " "  )

        qaDataDict['Question']  = ' '.join( qaDataDict['Question'].split() )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "‘" , "'"  )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "’" , "'"  )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "“" , "'"  )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "”" , "'"  )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "—" , "-"  )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "–" , "-"  )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "•" , "-"  )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "*" , "-"  )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "&" , "and" )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "%" , "\%" )
        qaDataDict['Question']  = qaDataDict['Question'].replace( "\"", "'"  )

        qaDataDict['awsTag']        = 'EC2'
        qaDataDict['crawled']       = True
        qaDataDict['dateScraped']   = date.today().strftime("%Y-%m-%d") + "-" + datetime.now().strftime('%H-%M')
        qaDataDict['sourceUri']     = response.url
                
        # print "\n\n-=-=-=-=-=-=-=-=-=-=-=-=-"
        # print qaDataDict
        # print "\n\n-=-=-=-=-=-=-=-=-=-=-=-=-"

        self.writeToFile(qaDataDict)
        # Return the JSON to be writtent to file
        yield qaDataDict

    # Method to write the XML to file, 
    def writeToFile(self, qaDataDict):

        dateScraped = date.today().strftime("%Y-%m-%d") + "-" + datetime.now().strftime('%H-%M')

        outputDir = os.path.abspath(__file__ + "/../../../outputs")
        outputFileName = '{0}-AWS-EC2-Discussions.json'.format( dateScraped )
        outputFileLoc = os.path.join( outputDir, "EC2", outputFileName )

        with open( outputFileLoc , 'a') as f:
            json.dump( qaDataDict, f, sort_keys=True)
        return
