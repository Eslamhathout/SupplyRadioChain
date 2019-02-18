# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import CravlingItem

import re


class CountrySpider(CrawlSpider):
    name = 'Transport_Topics'

    allowed_domains = ['ttnews.com']
    start_urls = ['http://www.ttnews.com/index.aspx']

    rules = (
        Rule(LinkExtractor(allow='',
                           restrict_xpaths=(
                               '//*[@id="storyofday_dgStory"]/tr/td/a[2]',
                               '//*[@id="Newsbrief_dgshowdata"]/tr[1]/td/p/a',
                               '//*[@id="Newsbrief_dgshowdata"]/tr[2]/td/p/a',
                           )),
             callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        i = CravlingItem()
        i['title'] = " ".join(response.xpath('//*[@id="lblHeadline"]/text()').extract()) or " "
        
        i['text'] = " "
	bb= response.xpath('//*[@id="storycolumn"]/p').extract()
	photo_container_name=response.xpath('//*[@id="sodphotocontainer"]/span/text()').extract()[0].strip()
	for m in range (0, len(bb)):
		if re.search(r'permission is prohibited', re.sub(r'<((style)|(script)).*?</\1>(?s)|<[^>]*?>|\n|\t|\r', '', bb[m])):
			continue
		else:
			i['text'] += re.sub(r'<((style)|(script)).*?</\1>(?s)|<[^>]*?>|\n|\t|\r', '', bb[m])
	
	i['text'] = re.sub(photo_container_name, photo_container_name+' ', i['text'])
	i['text'] = re.sub(photo_container_name+' '+photo_container_name, photo_container_name, i['text'])

	i['text'] = re.sub(r' Inc. ', '  ', i['text'])
	i['text'] = re.sub(r' DOT ', ' Department of Transport ', i['text'])
	i['text'] = re.sub(r' Penn ', ' Pennsylvania ', i['text'])

	i['text'] = re.sub(r'\s\s+', ' ', i['text'])
	firstparagraph = re.search("^.*?\.",i['text'])
	i['headline'] = firstparagraph.group(0) or " "
	i['text'] = re.sub(i['headline'], ' ', i['text'])
	i['url'] = response.url
        i['image'] = response.xpath('//*[@id="sodphoto"]/@src').extract()[0] or " "
        i['author'] = " ".join(
            response.xpath('//*[@id="lblByline"]/text()').extract()).strip() or " "
	i['spider'] =self.name
        return i

# .1\xa02\xa0Next
# .1\xa02\xa03\xa04\xa0Next
# 

#remove (CAPITAL_LETTERS)
