# -*- coding: utf-8 -*-
import scrapy
import json

class kuralItem(scrapy.Item):
    KuralPaal       = scrapy.Field()
    Athigaram       = scrapy.Field()
    KuralNo         = scrapy.Field()
    Kural           = scrapy.Field()
    KuralExpln1     = scrapy.Field()
    KuralExpln2     = scrapy.Field()

class getKuralSpdier(scrapy.Spider):
    name = "getKural"
    allowed_domains = ["dinamalar.com"]

    # start_urls = ( 'http://www.dinamalar.com/kural_detail.asp?kural_no=1')
    start_urls = ['http://www.dinamalar.com/kural_detail.asp?kural_no=%d' %(n) for n in range(1201,1331)]

    def parse(self, response):

        xpathDict = {}

        xpathDict['paal']               = "//div[@class='breadcrumb']/a[@class='nbgblue']/text()"
        xpathDict['athigaram']          = "//div[@class='col1']/div/div[@class='epapt clsKrlhead']/text()"
        xpathDict['kuralNo']            = "//div[@class='knowd']/text()"
        xpathDict['kural']              = "//div[@id='selText']/p/text()"
        xpathDict['kuralExp1']          = "//div[@class='cls100_p']/div[6]/p/text()"
        xpathDict['kuralExp2']          = "//div[@class='cls100_p']/div[8]/p/text()"

        kural = kuralItem()

        kural['KuralPaal']      = u''.join( response.xpath( xpathDict['paal'] ).extract() ).encode('utf-8')
        kural['Athigaram']      = ( u''.join( response.xpath( xpathDict['athigaram'] ).extract() ) ).split(":")[1].encode('utf-8')
        kural['KuralNo']        = ( u''.join( response.xpath( xpathDict['kuralNo'] ).extract() ) ).split(":")[1].split(")")[0].strip().encode('utf-8')
        kural['Kural']          = u''.join( response.xpath( xpathDict['kural'] ).extract() ).encode('utf-8').replace('\n', ' ').replace('\r', '')
        kural['KuralExpln1']    = u''.join( response.xpath( xpathDict['kuralExp1'] ).extract() ).encode('utf-8')
        kural['KuralExpln2']    = u''.join( response.xpath( xpathDict['kuralExp2'] ).extract() ).encode('utf-8')

        yield kural
