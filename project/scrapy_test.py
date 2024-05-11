
import scrapy


class GITSpider(scrapy.Spider):
    name = "scrapy_hh"
    start_url = ["https://api.hh.ru/employers", ]

    def parse(self, response):

        for items in response.xpath('items'):
            yield items.get()


nu = GITSpider()
print(nu.parse(response))
