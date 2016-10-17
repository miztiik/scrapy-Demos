import scrapy
import json

class printerItem(scrapy.Item):
    Brand = scrapy.Field()
    Name = scrapy.Field()
    Price = scrapy.Field()
    PrinterUrl = scrapy.Field()

class getBhpPrinterCatalogue (scrapy.Spider):
    name = "getBhpPrintercatalogueSpider"
    allowed_domains = ["bhphotovideo.com"]
    
    # Pass Scrapy Spider a list of URLs to crawl via .txt file
    # http://stackoverflow.com/questions/17307718/pass-scrapy-spider-a-list-of-urls-to-crawl-via-txt-file
    # Pass through strip to remove any trailing newline characters
    def __init__(self, filename=None):
        if filename:
            self.outputFilename = filename
            with open(filename, 'r') as f:
                self.start_urls = [url.strip() for url in f.readlines()]

    start_urls = ["https://www.bhphotovideo.com/c/search?ipp=100&atclk=Duplex_Automatic&ci=1109&Ns=p_REVIEWS%7c1&N=4042754067+235+4289301245+4166371334+4166995306"]

    def parse(self, response):
        # https://www.bhphotovideo.com/c/search?ipp=100&atclk=Duplex_Automatic&ci=1109&Ns=p_REVIEWS%7c1&N=4042754067+235+4289301245+4166371334+4166995306
        catalog = response.xpath('//div[@class="items full-width list-view elevn c2"]/div[@data-selenium="itemDetail"]')
        # catalog = catalog('.//div[@data-selenium="itemDetail"]')

        printers = printerItem()
        
        # Iterate through the printers to collect information about each printer
        for printerProduct in catalog:
            # Lets collect the brand, product name and price
            # The 'dot' at the beginning of the xpath ensures that we search within our 'printerProduct' context
            printers['Brand'] = printerProduct.xpath('.//span[@itemprop="brand"]/text()').extract()
            printers['Name'] = printerProduct.xpath('.//span[@itemprop="name"]/text()').extract()
            
            printers['PrinterUrl'] = printerProduct.xpath('.//h3[@data-selenium="itemHeading"]/a/@href').extract()
  
            # metaData = json.loads(printerProduct.xpath('.//@data-itemdata').extract())
            metaDataStr = ''.join(printerProduct.css('div[data-itemdata*=price]::attr(data-itemdata)').extract())
            metaData = json.loads(metaDataStr)
            printers['Price'] = metaData['price']
            # Return the value
            yield printers
        