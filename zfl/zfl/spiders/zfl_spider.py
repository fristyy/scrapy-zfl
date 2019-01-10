import scrapy
from zfl.items import ZflItem

class zfl(scrapy.Spider):

	name = 'zflspider'
	allowed_domains = ['952lls.com'，'zhaofuli.com']
	start_urls = ['https://952lls.com/MiiTao/']
	
	def parse(self, response):
		hreflist = response.xpath('//h2//@href').extract()
		for href in hreflist:
			href = response.urljoin(href)
			yield scrapy.Request(href, callback=self.content)
			
		next_url = response.xpath('//li[@class="next-page"]/a/@href').extract_first()
		if next_url is not None:
			yield response.follow(next_url, callback = self.parse)
	
		
	def content(self, response): 
		item = ZflItem()	
		title = response.xpath('//h1/text()').extract_first()
		item['title']=title
		item['imgurl']=response.xpath('//p/img/@src').extract()
		yield item	
		next_url = response.xpath('//li[@class="next-page"]/a/@href').extract_first()
		if next_url is not None:
			next_url = response.urljoin(next_url)
			yield response.follow(next_url, callback=self.content)
		
		
			
		
