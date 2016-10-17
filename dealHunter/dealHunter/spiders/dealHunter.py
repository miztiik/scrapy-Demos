# -*- coding: utf-8 -*-
import scrapy


class dealHuntingSplashSpider(scrapy.Spider):
    name = "dealHuntingSplashSpider"
    # allowed_domains = ["koovs.com"]
    # start_urls = ("http://www.koovs.com/only-onlall-stripe-ls-shirt-59554.html?from=category-651&skuid=236376")

    allowed_domains = ["acloud.guru"]
    start_urls = ("https://acloud.guru/forums/all/s3",)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            })

    def parse(self, response):
        #for option in response.css("div.select-size select.sizeOptions option")[1:]:
        # for option in response.xpath(".//div[@class='discussion-list-entry-body']/a/@href"):
        for option in response.xpath(".//div[@class='discussion-list-entry-body']"):
            # print option.xpath("text()").extract()
            print option.extract()
