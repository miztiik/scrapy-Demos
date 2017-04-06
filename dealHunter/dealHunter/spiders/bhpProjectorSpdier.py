# -*- coding: utf-8 -*-
import scrapy, json
import pdb, datetime

class projectorItem(scrapy.Item):
    Brand           = scrapy.Field()
    Name            = scrapy.Field()
    Price           = scrapy.Field()
    Uri             = scrapy.Field()
    ImageUri        = scrapy.Field()
    TimeStamp       = scrapy.Field()

class bhpProjectorSpdier(scrapy.Spider):
    name = "bhpProjectorSpdier"
    allowed_domains = ["bhphotovideo.com"]
    # start_urls = ( 'https://www.amazon.com/gp/search/ref=sr_nr_p_n_feature_seven_br_4?fst=as%3Aoff&rh=n%3A172282%2Cn%3A%21493964%2Cn%3A300334%2Cp_n_feature_browse-bin%3A2358237011%2Cp_n_feature_ten_browse-bin%3A11601827011%2Cp_n_feature_eleven_browse-bin%3A2057590011%2Cp_n_feature_seven_browse-bin%3A11028023011&bbn=300334&ie=UTF8&qid=1478519032&rnid=11028015011',)
    start_urls = ( 'https://www.bhphotovideo.com/c/search?atclk=Brand_Epson&ci=2116&N=4294546233+4292342915+4292342911+4291461369',)

    def parse(self, response):

        xpathDict = {}

        xpathDict['resultSet']          = "//div[@class='items full-width list-view elevn c2']/div[@data-selenium='itemDetail']"
        xpathDict['itemBrand']          = ".//span[@itemprop='brand']/text()"
        xpathDict['itemName']           = ".//span[@itemprop='name']/text()"
        xpathDict['itemUri']            = ".//h3[@data-selenium='itemHeading']/a/@href"
        xpathDict['itemImgUri']         = ".//img[@data-selenium='imgLoad']/@src"
        xpathDict['itemPrice']          = "@data-itemdata"


        itemLst = response.xpath( xpathDict['resultSet'] )

        if itemLst:
            projectors = projectorItem()
            for itemIndex,item in enumerate(itemLst):
                print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                print "  BEGIN PROCESSING OF ITEM : {0}".format( itemIndex )
                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"                
                try:
                    # Joining all the lists and avoiding the usage of index to avoid "index out of range" error when finding nothing
                    projectors['Brand']             = ''.join( item.xpath( xpathDict['itemBrand'] ).extract() )
                    projectors['Name']              = ''.join( item.xpath( xpathDict['itemName'] ).extract() )
                    projectors['Uri']               = ''.join( item.xpath( xpathDict['itemUri'] ).extract() )
                    projectors['ImageUri']          = ''.join( item.xpath( xpathDict['itemImgUri'] ).extract() )

                    findPriceStr = ''.join ( item.xpath( xpathDict['itemPrice'] ).extract() )
                    findPrice = json.loads( findPriceStr )
                    projectors['Price']             = findPrice['price']

                    projectors['TimeStamp']         = str(datetime.datetime.now())
    
                    yield projectors
    
                    print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    print "  SUCCESSFULLY PROCESSED PAGE : {0}, STARTING NEXT.".format( itemIndex )
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

                except:
                    print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    print "  ERROR PROCESSING URI : {0}".format( projectors['Uri'] )
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                    #pdb.set_trace()
                    pass