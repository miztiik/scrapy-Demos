import scrapy
import json

class getBhpPrinterCatalogueJson (scrapy.Spider):
    name = "getBhpPrintercatalogueSpiderJson"
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

    # "https://www.bhphotovideo.com/c/search?atclk=Resolution_1080p&ci=2116&294546233+35+4292342911&N=4294546233+35+4292342911+4126688793"

    def parse(self, response):
        
        # Setup the list to hold all the printer data
        printers = []
        # https://www.bhphotovideo.com/c/search?ipp=100&atclk=Duplex_Automatic&ci=1109&Ns=p_REVIEWS%7c1&N=4042754067+235+4289301245+4166371334+4166995306
        catalog = response.xpath('//div[@class="items full-width list-view elevn c2"]/div[@data-selenium="itemDetail"]')
        # catalog = catalog('.//div[@data-selenium="itemDetail"]')
      
        # Iterate through the printers to collect information about each printer
        for printerProduct in catalog:

            printerData = {}

            # Lets collect the brand, product name and price
            # The 'dot' at the beginning of the xpath ensures that we search within our 'printerProduct' context
            printerData['Brand'] = ''.join( printerProduct.xpath('.//span[@itemprop="brand"]/text()').extract() )
            printerData['Name'] = ' '.join( printerProduct.xpath('.//span[@itemprop="name"]/text()').extract() )
            
            printerData['PrinterUrl'] = ''.join( printerProduct.xpath('.//h3[@data-selenium="itemHeading"]/a/@href').extract() )
            printerData['PrinterImgUrl'] = ''.join( printerProduct.xpath('.//img[@data-selenium="imgLoad"]/@src').extract() )
            
            # metaData = json.loads(printerProduct.xpath('.//@data-itemdata').extract())
            metaDataStr = ''.join(printerProduct.css('div[data-itemdata*=price]::attr(data-itemdata)').extract())
            metaData = json.loads(metaDataStr)
            printerData['Price'] = metaData['price']
            
            # Add the Printer data to the printer list
            printers.append(printerData)

        # Lets dump everything to the file
        self.writeToFile(printers)
        # Return the value
        return
    
    # Method to write the JSON to file, 
    # The outputFilename(Global) is initialized in the beginning and matching with the urlList filename
    def writeToFile(self, jsonData):
        # with open('%s.json' % self.outputFilename, 'a') as f:
        with open('q1w2.json', 'a') as f:
            f.write(json.dumps(jsonData) + "\n")
        return

        

        
