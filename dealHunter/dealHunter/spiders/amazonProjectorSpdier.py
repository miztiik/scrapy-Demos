# -*- coding: utf-8 -*-
import scrapy
import pdb, datetime

class projectorItem(scrapy.Item):
    Brand           = scrapy.Field()
    Name            = scrapy.Field()
    Price           = scrapy.Field()
    Uri             = scrapy.Field()
    ImageUri        = scrapy.Field()
    Ratings         = scrapy.Field()
    CountOfRatings  = scrapy.Field()
    TimeStamp       = scrapy.Field()

class amazonProjectorSpdier(scrapy.Spider):
    name = "amazonProjectorSpdier"

    allowed_domains = ["amazon.com"]
    # start_urls = ( 'http://www.amazon.com/',)
    # start_urls = ( 'https://www.amazon.com/gp/search/ref=sr_nr_p_n_feature_seven_br_4?fst=as%3Aoff&rh=n%3A172282%2Cn%3A%21493964%2Cn%3A300334%2Cp_n_feature_browse-bin%3A2358237011%2Cp_n_feature_ten_browse-bin%3A11601827011%2Cp_n_feature_eleven_browse-bin%3A2057590011%2Cp_n_feature_seven_browse-bin%3A11028023011&bbn=300334&ie=UTF8&qid=1478519032&rnid=11028015011',)
    start_urls = ( 'https://www.amazon.com/s/ref=sr_nr_p_89_1?fst=as%3Aoff&rh=n%3A172282%2Cn%3A%21493964%2Cn%3A300334%2Cp_n_feature_eleven_browse-bin%3A2057590011%2Cp_n_condition-type%3A2224371011%2Cp_n_feature_ten_browse-bin%3A11601827011%2Cp_89%3AEpson&bbn=300334&sort=review-rank&ie=UTF8&qid=1478541006&rnid=2528832011',)

    def parse(self, response):

        xpathDict = {}

        xpathDict['resultSet']          = "//li[@class='s-result-item celwidget']"
        xpathDict['itemBrand']          = ".//div[@class='a-row a-spacing-small']/div/span[@class='a-size-small a-color-secondary'][2]/text()"
        xpathDict['itemName']           = ".//h2/text()"
        xpathDict['itemUri']            = ".//div[@class='a-row a-spacing-small']/a/@href"
        xpathDict['itemImgUri']         = ".//a[@class='a-link-normal a-text-normal']/img/@src"
        xpathDict['itemPrice']          = ".//span[contains(@class, 'a-size-base a-color-price')]/text()"
        xpathDict['itemRating']         = ".//a/i/span[@class='a-icon-alt']/text()"
        xpathDict['itemcntOfRatings']   = ".//div[@class='a-column a-span5 a-span-last']/div[@class='a-row a-spacing-mini']/a[@class='a-size-small a-link-normal a-text-normal']/text()"

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

                    findPrice = item.xpath( xpathDict['itemPrice'] ).extract()
                    
                    # Find price (sometimes does not exists) and picks up new and old offers, so lets pick only the best offer
                    if len(findPrice) > 0:
                        findPrice = ''.join ( findPrice[0] )    
                        findPrice = findPrice.replace( '$' , '' )
                        findPrice = findPrice.replace( ',' , '' )

                    projectors['Price']             = findPrice 

                    # Split the rating to get the first string, which shows how much the product is rated out of 5 (say 4.5)
                    findRating = ''.join ( item.xpath( xpathDict['itemRating'] ).extract() )
                    findRating = findRating.split(' ')[0]    
                   
                    projectors['Ratings']           = findRating
                    projectors['CountOfRatings']    = ''.join ( item.xpath( xpathDict['itemcntOfRatings'] ).extract() )
                    projectors['TimeStamp']         = str(datetime.datetime.now())
    
                    yield projectors
    
                    print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    print "  SUCCESSFULLY PROCESSED, STARTING NEXT. "
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

                except:
                    print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    print "  ERROR PROCESSING URI : {0}".format( projectors['Uri'] )
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                    # pdb.set_trace()
                    pass